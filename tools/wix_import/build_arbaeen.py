"""The Recognition of Arbaeen: series page + parts 1-2 (English). Replaces the two stand-alone articles
recognition-of-arbaeen-part-1/-2 (same Wix posts, same text) so they read as one series, like Morning & Evening Mourning.

Needs the cached Wix posts in work/ (see README). Re-runnable. Afterwards: build_sitemap.py, build_taxo.py, check_site.py.
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
import build_mourning as M

SER = 'recognition-of-arbaeen'
NAME = 'The Recognition of Arbaeen'
DESC = ("A two-part series on the recognition (ma'rifah) of Arbaeen, the visit to Imam Hussain (p): the reward of the pilgrim's steps, "
        "and the blessing of intellect on the path of Imam Hussain (p).")
CHAPTERS = [(1, 'the-recognition-of-arbaeen-part-one', 'recognition-of-arbaeen-part-1'), (2, 'the-recognition-of-arabeen-part-two', 'recognition-of-arbaeen-part-2')]
LANG = 'en'
TP = {LANG: template(LANG)}


def prime_cache(n, old):
    """The covers/body images were fetched under the old slugs; give the cached downloads their new names so nothing is re-downloaded."""
    os.makedirs(SP + f'body_{SER}', exist_ok=True)
    for src, dst in ((SP + f'img_{old}_en.bin', SP + f'img_{SER}-{n}_en.bin'),
                     (SP + f'body_{old}_en-1.bin', SP + f'body_{SER}/{n}_en-1.bin'), (SP + f'body_{old}_en-2.bin', SP + f'body_{SER}/{n}_en-2.bin')):
        if os.path.exists(src) and not os.path.exists(dst): shutil.copy(src, dst)


def main():
    CAT = json.load(open(HERE + 'catalog.json'))
    arts = {}
    for n, wix, old in CHAPTERS:
        prime_cache(n, old)
        a = load_post(SP + 'posts/' + wix[:80] + '.html')
        a['img'] = make_image(a, f'{SER}/{n}', LANG)
        arts[n] = a
        CAT.pop(old, None)
    for n, a in arts.items():
        sr = dict(name=NAME, href=f'/articles/{SER}/', n=n)
        if n - 1 in arts: sr['prev'] = (f'/articles/{SER}/{n - 1}/', arts[n - 1]['title'])
        if n + 1 in arts: sr['next'] = (f'/articles/{SER}/{n + 1}/', arts[n + 1]['title'])
        page(f'{SER}/{n}', LANG, a, [LANG], TP, series=sr)
        CAT[f'{SER}/{n}'] = dict(slug=f'{SER}/{n}', series=SER, month=2, langs=[LANG], titles={LANG: a['title']}, tags=a['tags'], tags_l={LANG: a['tags']},
                                 published=a['published'], img=bool(a['img']), descs={LANG: a['desc']})
    CAT[SER] = dict(slug=SER, kind='series', month=2, langs=[LANG], titles={LANG: NAME}, tags=[], tags_l={}, published=max(a['published'] for a in arts.values()), img=True, descs={LANG: DESC})
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    # the series page reuses build_mourning's layout
    M.SER, M.NAME, M.series_desc = SER, {LANG: NAME}, (lambda lang: DESC)
    M.TP = TP
    # card labels: "Part One"/"Part Two" chip and the post's own title (series_page would otherwise read the in-body headings)
    cards = {(LANG, n): dict(arts[n], heads=[{'t': 'p', 'x': f'Part {w}'}]) for (n, _, _), w in zip(CHAPTERS, ('One', 'Two'))}
    M.series_page(LANG, cards, [LANG])
    print('built', {n: (len(a['body']), a['img'] and a['img']['orig']) for n, a in arts.items()})


if __name__ == '__main__':
    main()
