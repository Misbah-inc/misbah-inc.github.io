import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
for l, v in {'en': 'Article', 'ar': 'مقالة', 'fa': 'مقاله', 'ur': 'مضمون'}.items(): S[l]['article'] = v
TP = {l: template(l) for l in LANGS}
alts = json.load(open(SP + 'alts.json'))
CAT = json.load(open(HERE + 'catalog.json')) if os.path.exists(HERE + 'catalog.json') else {}

def run(spec):
    """spec: dict(slug, wix=<english wix slug>, month=<1-12 or None>)"""
    slug, wix = spec['slug'], spec['wix']
    files = {'en': SP + 'posts/' + wix[:80] + '.html'}
    for l in ('ar', 'fa', 'ur'):
        f = SP + f'posts2/{wix[:60]}-{l}.html'
        if l in alts.get(wix, {}) and os.path.exists(f): files[l] = f
    arts = {l: load_post(f) for l, f in files.items()}
    avail = [l for l in LANGS if l in arts]
    info = {}
    arts['en']['img'] = make_image(arts['en'], slug, 'en')
    for l, a in sorted(arts.items(), key=lambda kv: kv[0] != 'en'):
        a['img'] = make_image(a, slug, l)
        if not a['img'] and arts['en'].get('img'):      # this language's post has no cover: reuse the English one
            import shutil
            d = ROOT + 'images/articles/'
            for pre in ('', 'og-'): shutil.copy(f'{d}{pre}{slug}-en.jpg', f'{d}{pre}{slug}-{l}.jpg')
            a['img'] = dict(arts['en']['img'])
        info[l] = page(slug, l, a, avail, TP)
    CAT[slug] = dict(slug=slug, month=spec.get('month'), langs=avail, titles={l: a['title'] for l, a in arts.items()},
                     tags=arts['en']['tags'], tags_l={l: a['tags'] for l, a in arts.items()}, published=arts['en']['published'], img=bool(arts['en']['img']),
                     descs={l: a['desc'] for l, a in arts.items()})
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    print(slug, avail, {l: (len(a['body']), a['img'] and a['img']['orig']) for l, a in arts.items()})

if __name__ == '__main__':
    specs = json.load(open(sys.argv[1]))
    for s in specs: run(s)
