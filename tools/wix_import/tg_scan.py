import sys, re, time, json
sys.path.insert(0, '.')
import tg_collect as T
lang = sys.argv[1]; since = sys.argv[2]; out = f'work/tg/scan-{lang}.json'
ch = T.CH[lang]; allp = {}; before = None
for _ in range(80):
    ps = T.parse(T.fetch(ch, None, before))
    if not ps: break
    for p in ps: allp[p['n']] = p
    before = min(p['n'] for p in ps)
    if min(p['date'] for p in ps)[:10] < since: break
    time.sleep(0.3)
posts = [allp[k] for k in sorted(allp) if allp[k]['date'][:10] >= since]
json.dump(posts, open(out, 'w'), ensure_ascii=False, indent=1)
print(lang, len(posts), 'posts since', since)
