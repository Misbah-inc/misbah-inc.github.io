"""Morning & Evening Mourning: series page + chapters 1-10 (English; chapters 1-2 also Arabic)."""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA

for l, v in {'en': 'Article', 'ar': 'مقالة', 'fa': 'مقاله', 'ur': 'مضمون'}.items(): S[l]['article'] = v
TP = {l: template(l) for l in LANGS}
SER = 'morning-and-evening-mourning'
NAME = {'en': 'Morning & Evening Mourning', 'ar': 'العزاء صباحاً ومساءً'}   # fa/ur: no chapters exist on Wix, so no pages
CHAPTERS = [(1, 'morning-and-evening-mourning'), (2, 'morning-and-evening-mourning-1'), (3, 'copy-of-morning-and-evening-mourning-chapter-three'),
            (4, 'morning-and-evening-mourning-chapter-four'), (5, 'morning-and-evening-mourning-chapter-five'), (6, 'copy-of-morning-and-evening-mourning-chapter-six'),
            (7, 'morning-and-evening-mourning-chapter-seven'), (8, 'morning-and-evening-mourning-chapter-eight'),
            (9, 'copy-of-morning-and-evening-mourning-chapter-nine'), (10, 'morning-and-evening-mourning-chapter-ten')]
ORDW = {'en': ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']}
alts = json.load(open(SP + 'alts.json'))
CAT = json.load(open(HERE + 'catalog.json'))


def series_desc(lang):
    """The site's own one-line description of the series, from the homepage's mourning section."""
    f = ROOT + ('index.html' if lang == 'en' else f'{lang}/index.html')
    t = open(f, encoding='utf-8').read()
    m = re.search(r'<p class="mourning-desc">\s*(.*?)\s*</p>', t, re.S)
    return html.unescape(re.sub(r'\s+', ' ', m.group(1))) if m else ''


def load_chapter(n, wix, lang):
    f = SP + ('posts/' + wix[:80] + '.html' if lang == 'en' else f'posts2/{wix[:60]}-{lang}.html')
    if not os.path.exists(f): return None
    a = load_post(f)
    if lang != 'en':
        # the Arabic post is titled only with the series name; add the chapter label from its first line so titles stay unique
        lab = a['heads'][0]['x'] if a['heads'] else ''
        if lab and lab not in a['title']: a['title'] = f"{a['title']} — {lab}"
    return a


def sref(lang, n=None):
    return f"{PFX[lang]}/articles/{SER}/" + (f'{n}/' if n else '')


def main():
    arts = {}   # (lang, n) -> post
    for n, wix in CHAPTERS:
        for lang in ('en', 'ar'):
            if lang == 'ar' and 'ar' not in alts.get(wix, {}): continue
            a = load_chapter(n, wix, lang)
            if a: arts[(lang, n)] = a
    # covers (reuse English when a language has none)
    for (lang, n), a in sorted(arts.items(), key=lambda kv: kv[0][0] != 'en'):
        slug = f'{SER}/{n}'
        a['img'] = make_image(a, slug, lang)
        if not a['img'] and arts[('en', n)].get('img'):
            import shutil
            fs = slug.replace('/', '-'); d = ROOT + 'images/articles/'
            for pre in ('', 'og-'): shutil.copy(f'{d}{pre}{fs}-en.jpg', f'{d}{pre}{fs}-{lang}.jpg')
            a['img'] = dict(arts[('en', n)]['img'])
    langs_of = {n: [l for l in LANGS if (l, n) in arts] for n, _ in CHAPTERS}
    for (lang, n), a in arts.items():
        sr = dict(name=NAME[lang], href=sref(lang), n=n)
        if (lang, n - 1) in arts: sr['prev'] = (sref(lang, n - 1), arts[(lang, n - 1)]['title'])
        if (lang, n + 1) in arts: sr['next'] = (sref(lang, n + 1), arts[(lang, n + 1)]['title'])
        page(f'{SER}/{n}', lang, a, langs_of[n], TP, series=sr)
    # catalog: chapters (hidden from the article grids) + the series itself
    for n, wix in CHAPTERS:
        CAT[f'{SER}/{n}'] = dict(slug=f'{SER}/{n}', series=SER, month=None, langs=langs_of[n], titles={l: arts[(l, n)]['title'] for l in langs_of[n]},
                                 tags=arts[('en', n)]['tags'], tags_l={l: arts[(l, n)]['tags'] for l in langs_of[n]}, published=arts[('en', n)]['published'],
                                 img=bool(arts[('en', n)]['img']), descs={l: arts[(l, n)]['desc'] for l in langs_of[n]})
    sl = [l for l in LANGS if any(k[0] == l for k in arts)]
    CAT[SER] = dict(slug=SER, kind='series', month=None, langs=sl, titles={l: NAME[l] for l in sl}, tags=[], tags_l={}, published='2026-08-09', img=True,
                    descs={l: series_desc(l) for l in sl})
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    for lang in sl: series_page(lang, arts, sl)
    print('chapters', {n: langs_of[n] for n, _ in CHAPTERS})


def series_page(lang, arts, sl):
    L = S[lang]; tp = TP[lang]
    chap = sorted(n for (l, n) in arts if l == lang)
    cur = f'{SITE}{sref(lang)}'
    desc = BA.clip(series_desc(lang), 160)
    name = NAME[lang]
    first = chap[0]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": cur + "#webpage", "url": cur, "name": name, "description": series_desc(lang), "inLanguage": lang,
         "isPartOf": {"@id": SITE + "/#website"},
         "mainEntity": {"@type": "CreativeWorkSeries", "name": name, "numberOfItems": len(chap),
                        "hasPart": [{"@type": "Article", "name": arts[(lang, n)]['title'], "url": SITE + sref(lang, n)} for n in chap]}},
        breadcrumb_ld(lang, [(name, None)]), ORG]}
    og = f'/images/articles/og-{SER}-{first}-{lang}.jpg'
    h = head(lang, tp, title=f"{name} | {L['brand']}", desc=desc, parts=(), og_img=og, og_type='website', published='', ld=ld)
    hl = ''.join(f'  <link rel="alternate"  hreflang="{l}" href="{SITE}{sref(l)}">\n' for l in sl) + f'  <link rel="alternate"  hreflang="x-default" href="{SITE}{sref("en")}">'
    h = re.sub(r'  <!-- Canonical \+ hreflang -->.*?(?=\n\n  <!-- Open Graph)', f'  <!-- Canonical + hreflang -->\n  <link rel="canonical"  href="{cur}">\n{hl}', h, flags=re.S)
    h = h.replace(f'content="{SITE}{PFX[lang]}/articles/{G.SLUG}/"', f'content="{cur}"')
    from PIL import Image, ImageOps
    cards = ''
    for n in chap:
        tdst = ROOT + f'images/articles/thumb-{SER}-{n}-{lang}.jpg'
        if not os.path.exists(tdst):
            ImageOps.fit(Image.open(ROOT + f'images/articles/{SER}-{n}-{lang}.jpg').convert('RGB'), (480, 270), method=Image.LANCZOS, centering=(0.5, 0.4)).save(tdst, 'JPEG', quality=78, progressive=True, optimize=True)
        a = arts[(lang, n)]
        fs = f'{SER}-{n}'
        desc_n = a['desc'] or next((b['x'] for b in a['body'] if b['t'] == 'p' and len(b['x']) > 60), '')
        sub = next((b['x'] for b in a['heads'] if b['t'] == 'blockquote'), '')
        cards += f'''
    <a class="kw-part-card" href="{sref(lang, n)}">
      <img src="/images/articles/thumb-{fs}-{lang}.jpg" alt="" width="480" height="270" loading="lazy" decoding="async">
      <div class="kw-part-body">
        <span class="kw-series-chip">{esc(a['heads'][0]['x']) if a['heads'] else n}</span>
        <h2>{esc(sub or a['title'])}</h2>
        <p>{esc(BA.clip(desc_n, 220))}</p>
        <span class="btn btn-gold">{UI_READ[lang]}</span>
      </div>
    </a>'''
    back = '<path d="M5 12h14M12 5l7 7-7 7"/>' if lang != 'en' else '<path d="M19 12H5M12 5l-7 7 7 7"/>'
    names = {'en': 'English', 'ar': 'العربية', 'fa': 'فارسی', 'ur': 'اردو'}
    links = ''
    for l in sl:
        cls = ' class="active"' if l == lang else ''
        links += f'\n      <a href="{sref(l)}" hreflang="{l}"{cls}>{names[l]}</a>'
    sw = f'<div class="art-lang-sw-inline" aria-label="{L["read_in_aria"]}">\n      <span class="lsw-label">{L["read_in"]}</span>{links}\n    </div>' if len(sl) > 1 else ''
    cover = f'''<div class="kw-banner-wrap"><div class="kw-banner kw-banner--tall"><img src="/images/articles/{SER}-{first}-{lang}.jpg" alt="{html.escape(name, quote=True)}" fetchpriority="high"></div></div>
'''
    main = f'''<main>

{cover}{crumbs(lang, [(name, None)])}

<div class="art-page">
  <div class="art-container">

    <a href="{PFX[lang]}/articles/" class="art-back">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        {back}
      </svg>
      {L['all']}
    </a>

    <div class="art-meta"><span class="art-tag">{L['tag']}</span></div>

    <div class="art-title-block">
      <h1 class="art-title">{esc(name)}</h1>
    </div>

    {sw}

    <p class="art-intro">{esc(series_desc(lang))}</p>

    <div class="kw-parts">{cards}
    </div>

  </div>
</div>

</main>

'''
    tail = f'\n{tp["footer"]}\n\n<script src="/assets/theme.js"></script>\n<script src="/assets/script.js"></script>\n</body>\n</html>\n'
    p = f'{PFX[lang].lstrip("/")}{"/" if PFX[lang] else ""}articles/{SER}/index.html'
    open(ROOT + p, 'w', encoding='utf-8').write(h + main + tail)


UI_READ = {'en': 'Read', 'ar': 'اقرأ', 'fa': 'بخوانید', 'ur': 'پڑھیں'}

if __name__ == '__main__':
    main()
