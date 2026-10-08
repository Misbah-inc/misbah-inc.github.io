"""Writes work/arabic-review.html: every Arabic crop used in the booklet pages, with the English around it, for a human check."""
import re, glob, html, base64, os
ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..') + '/'
os.chdir(ROOT)
SER = {'muharram-safar-booklets': 'Muharram & Safar Booklets', 'ghadir-booklets': 'Ghadir Booklets', 'ramadan-booklets': 'Ramadan Booklets'}
# already reviewed and published in the first batch (muharram 1-9, ghadir 1-5): skipped unless --all
REVIEWED = {('muharram-safar-booklets', str(n)) for n in range(1, 10)} | {('ghadir-booklets', str(n)) for n in range(1, 6)}
import sys
ALL = '--all' in sys.argv
files = sorted(glob.glob('articles/*-booklets/[0-9]*/index.html'), key=lambda x: (x.split('/')[1], int(x.split('/')[2])))
txt = lambda x: html.unescape(re.sub(r'<[^>]+>', '', x)).strip()
sections, n_img = [], 0
for f in files:
    ser, num = f.split('/')[1], f.split('/')[2]
    if not ALL and (ser, num) in REVIEWED: continue
    t = open(f, encoding='utf-8').read()
    title = html.unescape(re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S).group(1))
    b = re.search(r'<div class="art-body">(.*?)</section>', t, re.S).group(1)
    items = re.findall(r'(<p>.*?</p>|<figure class="art-fig">.*?</figure>)', b, re.S)
    cards = []
    for i, it in enumerate(items):
        if 'lang="ar"' not in it: continue
        src = re.search(r'src="([^"]+)"', it).group(1)
        prev = next((txt(items[j]) for j in range(i - 1, -1, -1) if items[j].startswith('<p>')), '')
        nxt = next((txt(items[j]) for j in range(i + 1, len(items)) if items[j].startswith('<p>')), '')
        cards.append((os.path.basename(src).split('-')[0], base64.b64encode(open(src[1:], 'rb').read()).decode(), prev, nxt))
    if cards: sections.append((ser, num, title, cards)); n_img += len(cards)
css = 'body{font-family:system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;background:#f6f3ec;color:#222}h1{font-size:1.5rem}h2{margin-top:2.5rem;border-bottom:2px solid #c9a46b;padding-bottom:.3rem;font-size:1.15rem}.c{background:#fff;border:1px solid #ddd;border-radius:10px;padding:.8rem;margin:1rem 0}.c img{max-width:100%;background:#111;border-radius:6px;display:block;margin:.4rem auto}.m{font-size:.8rem;color:#777}.t{font-size:.9rem;color:#444;margin:.3rem 0}.n{border-top:1px dashed #ccc;margin-top:.6rem;padding-top:.4rem;font-size:.8rem;color:#999}'
out = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Arabic crops for review</title><style>{css}</style></head><body>',
       f'<h1>Arabic lines kept as pictures — for review</h1><p>{n_img} images from {len(sections)} booklets. Each is cut from the booklet PDF page exactly as it appears (the PDF\'s Arabic text layer is scrambled, so it cannot be copied as text). Please check each one is complete, readable and not cut off. The English around it is shown for context.</p>']
for ser, num, title, cards in sections:
    out.append(f'<h2>{html.escape(SER[ser])} · {num} · {html.escape(title)} <span class="m">(/articles/{ser}/{num}/)</span></h2>')
    for pg, data, prev, nxt in cards:
        out.append(f'<div class="c"><div class="m">PDF page {pg}</div><div class="t">before: {html.escape(prev[:160])}</div><img src="data:image/jpeg;base64,{data}" alt="Arabic crop"><div class="t">after: {html.escape(nxt[:160])}</div><div class="n">Notes: ______________________</div></div>')
out.append('</body></html>')
os.makedirs('tools/wix_import/work', exist_ok=True)
open('tools/wix_import/work/arabic-review.html', 'w', encoding='utf-8').write('\n'.join(out))
print(n_img, 'images,', len(sections), 'booklets,', os.path.getsize('tools/wix_import/work/arabic-review.html') // 1024, 'KB')
