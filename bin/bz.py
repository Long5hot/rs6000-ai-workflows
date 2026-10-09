#!/usr/bin/env python3
"""Fetch the useful parts of a GCC Bugzilla PR, compactly, via curl + jq.

  bz.py 123055                  summary fields + trimmed comments + attachment list
  bz.py 123055 -c 0,3           only comments 0 and 3
  bz.py 123055 -c 3 --full      comment 3 untrimmed
  bz.py 123055 -a 61234         save attachment 61234 to <framework>/work/pr123055/

Bugs listed in the main bug's see_also field are printed after it, in order,
as context (not recursively).  --no-see-also turns that off.

Read-only.  People (reporter, assignee, cc) and other noise are never fetched.
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys

REST = 'https://gcc.gnu.org/bugzilla/rest/bug'

BUG_FIELDS = ('id,summary,status,resolution,component,version,target_milestone,'
              'keywords,priority,severity,cf_gcctarget,cf_gcchost,'
              'cf_known_to_work,cf_known_to_fail,depends_on,blocks,see_also,'
              'dupe_of,creation_time,last_change_time')
BUG_JQ = '.bugs[0]'
COMMENTS_JQ = ('[.bugs[].comments[] | {n: .count, by: (.creator | split("@")[0]),'
               ' on: .creation_time[0:10], att: .attachment_id, text}]')
ATTACH_JQ = ('[.bugs[][] | select(.is_obsolete == 0) |'
             ' {id, name: .file_name, size, patch: .is_patch, about: .summary}]')


def fetch(url, jq_filter):
    """curl URL | jq FILTER, returning the parsed result."""
    curl = subprocess.run(['curl', '-sS', '--max-time', '60', url],
                          capture_output=True)
    if curl.returncode != 0 and not curl.stdout:
        sys.exit('bz.py: curl failed: ' + curl.stderr.decode(errors='replace').strip())
    try:
        err = json.loads(curl.stdout)
        if isinstance(err, dict) and err.get('error'):
            sys.exit('bz.py: Bugzilla: ' + str(err.get('message')))
    except ValueError:
        sys.exit('bz.py: unexpected reply from Bugzilla')
    jq = subprocess.run(['jq', '-c', jq_filter], input=curl.stdout, capture_output=True)
    if jq.returncode != 0:
        sys.exit('bz.py: jq failed: ' + jq.stderr.decode(errors='replace').strip())
    return json.loads(jq.stdout)


def squeeze_commit(lines):
    """Reduce a commit-bot comment to commit id, subject and ChangeLog lines."""
    out = []
    branch = re.search(r'The (\S+) branch has been updated', lines[0])
    url = next((l for l in lines if 'gcc.gnu.org/g:' in l), '')
    rev = next((l for l in lines if l.startswith('commit r')), '')
    head = 'commit ' + (rev[7:] if rev else url.rsplit('g:', 1)[-1])
    if branch:
        head += ' on ' + branch.group(1)
    out.append(head)
    body = lines[lines.index(rev) + 1:] if rev else lines
    body = [l for l in body if l.strip()
            and not l.startswith(('Author:', 'Date:', 'https://'))]
    if body:
        out.append(body[0].strip())
    out += [l.strip() for l in body[1:] if l.lstrip().startswith(('* ', 'PR '))]
    return out


def trim(text, full, max_lines, max_cols):
    lines = text.replace('\r', '').split('\n')
    if full:
        return lines
    if re.match(r'The \S+ branch has been updated by', lines[0]):
        return squeeze_commit(lines)
    out, blank = [], False
    for l in lines:
        l = l.rstrip()
        if l.startswith('>'):                       # quoted reply text
            continue
        if re.match(r'Created attachment \d+$', l):   # already in the header
            continue
        m = re.match(r'\(In reply to .* from comment #(\d+)\)', l)
        if m:
            l = '(re c%s)' % m.group(1)
        if not l:
            if blank or not out:
                continue
            blank = True
        else:
            blank = False
        if len(l) > max_cols:
            l = l[:max_cols] + ' [+%d chars]' % (len(l) - max_cols)
        out.append(l)
    while out and not out[-1]:
        out.pop()
    if len(out) > max_lines:
        keep_tail = max_lines // 5
        cut = len(out) - max_lines
        out = (out[:max_lines - keep_tail] + ['[... %d lines cut ...]' % cut]
               + out[-keep_tail:])
    return out


def show_bug(b):
    state = b['status'] + (' ' + b['resolution'] if b['resolution'] else '')
    print('PR %s | %s | %s | %s %s' % (b['id'], b['component'], state,
                                       b['priority'], b['severity']))
    print('Summary: ' + b['summary'])
    rows = [('Keywords', ', '.join(b['keywords'])),
            ('Target', b['cf_gcctarget']), ('Host', b['cf_gcchost']),
            ('Version', b['version']),
            ('Milestone', '' if b['target_milestone'] == '---' else b['target_milestone']),
            ('Known to work', b['cf_known_to_work']),
            ('Known to fail', b['cf_known_to_fail']),
            ('Depends on', ' '.join(map(str, b['depends_on']))),
            ('Blocks', ' '.join(map(str, b['blocks']))),
            ('Duplicate of', str(b['dupe_of'] or '')),
            ('See also', ' '.join(b['see_also']))]
    for k, v in rows:
        if v:
            print('%s: %s' % (k, v))
    print('Opened %s, last change %s' % (b['creation_time'][:10],
                                         b['last_change_time'][:10]))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('bug', help='PR number (a trailing "/" or "PR" prefix is accepted)')
    ap.add_argument('-c', '--comments', help='comma separated comment numbers')
    ap.add_argument('--full', action='store_true', help='do not trim comment text')
    ap.add_argument('--max-lines', type=int, default=60, help='per comment (default 60)')
    ap.add_argument('--max-cols', type=int, default=300, help='per line (default 300)')
    ap.add_argument('--budget', type=int, default=12000,
                    help='total characters of comment text; older middle comments '
                    'are reduced to one line beyond it (default 12000, 0 = no limit)')
    ap.add_argument('--related-budget', type=int, default=5000,
                    help='comment budget for each see_also bug (default 5000)')
    ap.add_argument('--no-see-also', action='store_true',
                    help='do not fetch the bugs listed in see_also')
    ap.add_argument('-a', '--attachment', help='attachment id to save')
    ap.add_argument('-o', '--out', help='directory for --attachment')
    args = ap.parse_args()

    m = re.search(r'\d+', args.bug)
    if not m:
        sys.exit('bz.py: no PR number in %r' % args.bug)
    bug = m.group(0)

    if args.attachment:
        att = fetch('%s/attachment/%s' % (REST, args.attachment),
                    '.attachments[] | {name: .file_name, data}')
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        out = args.out or os.path.join(here, 'work', 'pr' + bug)
        os.makedirs(out, exist_ok=True)
        path = os.path.join(out, os.path.basename(att['name']) or 'attachment')
        data = base64.b64decode(att['data'])
        with open(path, 'wb') as f:
            f.write(data)
        print('saved %s (%d bytes)' % (path, len(data)))
        return

    want = None
    if args.comments:
        want = {int(x) for x in args.comments.split(',')}
    see_also = show(bug, args, want, args.budget)

    # Related bugs named in see_also: context only, the main bug stays BUG.
    related = []
    for url in see_also:
        m = re.match(r'https?://gcc\.gnu\.org/bugzilla/show_bug\.cgi\?id=(\d+)$', url)
        if m and m.group(1) != bug and m.group(1) not in related:
            related.append(m.group(1))
    if want is None and related and not args.no_see_also:
        print('\n' + '=' * 70)
        print('PR %s has see_also bugs that give more context. The main bug is still'
              ' PR %s;\nread the related bugs below, in this order: %s.'
              % (bug, bug, ', then '.join(related)))
        for i, r in enumerate(related, 1):
            print('\n' + '=' * 70)
            print('RELATED %d of %d (context for PR %s)' % (i, len(related), bug))
            show(r, args, None, args.related_budget)


def show(bug, args, want, budget):
    """Print one bug; return its see_also list."""
    see_also = []
    if want is None:
        b = fetch('%s/%s?include_fields=%s' % (REST, bug, BUG_FIELDS), BUG_JQ)
        see_also = b['see_also']
        show_bug(b)
        atts = fetch('%s/%s/attachment?exclude_fields=data' % (REST, bug), ATTACH_JQ)
        for a in atts:
            print('Attachment %s: %s (%d bytes%s) %s' % (
                a['id'], a['name'], a['size'], ', patch' if a['patch'] else '',
                a['about']))

    items = []
    for c in fetch('%s/%s/comment' % (REST, bug), COMMENTS_JQ):
        if want is not None and c['n'] not in want:
            continue
        lines = trim(c['text'], args.full, args.max_lines, args.max_cols)
        if lines:
            items.append((c, lines))

    # Within the budget keep comment 0, then the newest comments; the rest
    # become one line each so the model can ask for them with -c.
    keep = set(range(len(items)))
    if want is None and budget:
        size = [sum(len(l) + 1 for l in lines) for _, lines in items]
        keep, used = {0}, size[0] if size else 0
        for i in range(len(items) - 1, 0, -1):
            if used + size[i] > budget:
                break
            keep.add(i)
            used += size[i]

    short = 0
    for i, (c, lines) in enumerate(items):
        att = ' [attachment %s]' % c['att'] if c['att'] else ''
        head = 'c%d %s %s%s' % (c['n'], c['on'], c['by'], att)
        if i in keep:
            print('\n--- ' + head)
            print('\n'.join(lines))
        else:
            if not short:
                print('\n--- shortened to one line each; full text: bz.py %s -c N' % bug)
            short += 1
            first = next((l for l in lines if l
                          and not re.match(r'\(re c|(Hi|Hello|Thanks)\b', l)), '')
            print('%s: %s' % (head, first[:110]))
    return see_also


if __name__ == '__main__':
    main()
