"""Sermon of Muttaqin (Khutbat al-Muttaqin): series page + parts 1-14, English only.

Source: the channel's YouTube videos; the text of each part is the video's own description
(see muttaqin_content.py). Re-runnable. Afterwards: build_sitemap.py, build_taxo.py, build_home_topics.py,
check_site.py (see README).
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
import muttaqin_content as MC
from PIL import Image, ImageDraw, ImageFont

SER = 'khutbat-al-muttaqin'
NAME = 'Sermon of Muttaqin'
LANG = 'en'
SERIES_DATE = '2026-10-06'          # newest part; moves the series to the top of the articles index
SERIES_DESC = ('A series on the Sermon of Muttaqin (Khutbat al-Muttaqin) by Imam Ali (p): the characteristics of the '
               'God-conscious, one at a time, with stories from the Ahl al-Bayt (p).')
DESC = {
 1: "Part 1 of the Sermon of Muttaqin: the God-conscious speak rightly and beautifully. Imam Ali's reply to Hammām, and Lady Fiḍḍah, who spoke only in Qur'an.",
 2: "Part 2 of the Sermon of Muttaqin: the God-conscious live by moderation in dress and conduct, as in the story of Salmān al-Fārsī, governor of Madāʾin.",
 3: "Part 3 of the Sermon of Muttaqin: the God-conscious walk with humility. Mālik al-Ashtar's patience with the shopkeeper who insulted him in Kūfah.",
 4: "Part 4 of the Sermon of Muttaqin: the God-conscious lower their gaze from what Allah forbade, and the story of the seminary student who became Mir Damad.",
 5: "Part 5 of the Sermon of Muttaqin: the God-conscious devote their hearing to beneficial knowledge, with accounts of Allamah Majlisi, the Gateway to the Imams.",
 6: "Part 6 of the Sermon of Muttaqin: the God-conscious stay the same in hardship and in ease, as Abu Dharr showed when he refused Uthman's two hundred dinars.",
 7: "Part 7 of the Sermon of Muttaqin: the God-conscious long to meet their Lord, and the story of Ali ibn Mahziyar's longing to meet Imam al-Mahdi (ajtf).",
 8: "Part 8 of the Sermon of Muttaqin: the Creator is so great in their souls that all else seems small, and Prophet Ibrahim (p) hearing the attributes of Allah.",
 9: "Part 9 of the Sermon of Muttaqin: the God-conscious are people of certainty (yaqīn), and the young man who told the Prophet (p) the reality of his certainty.",
 10: "Part 10 of the Sermon of Muttaqin: the hearts of the God-conscious are filled with sorrow, from Prophet Yaʿqūb's grief to Imam al-Sajjad's weeping.",
 11: "Part 11 of the Sermon of Muttaqin: people are safe from the harm of the God-conscious, and Muslim ibn Aqīl's refusal to kill Ibn Ziyād in Hani's house.",
 12: "Part 12 of the Sermon of Muttaqin: the bodies of the God-conscious are lean and slender, and the marks of worship seen on Abu al-Fadl al-Abbas (p).",
 13: "Part 13 of the Sermon of Muttaqin: the needs of the God-conscious are few and modest, and the story of Lady Narjis (p), the Roman princess and captive.",
 14: "Part 14 of the Sermon of Muttaqin: the souls of the God-conscious are chaste, pure and guarded from sin, and the four qualities Allah praised in Jaʿfar ibn Abi Talib.",
}
SHORT = {n: v[2] for n, v in MC.PARTS.items()}
SHORT[5] = 'Hearing for Beneficial Knowledge'; SHORT[8] = 'The Creator Is Great to Them'; SHORT[6] = 'The Same in Hardship and Ease'

TP = {LANG: template(LANG)}
D = ROOT + 'images/articles/'


# ── covers ───────────────────────────────────────────────────────────────
def font(sz): return ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf', sz)


def spaced(d, xy, text, f, fill, gap):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + gap


def wrap(d, text, f, w):
    lines, cur = [], ''
    for wd in text.split():
        t = (cur + ' ' + wd).strip()
        if d.textlength(t, font=f) <= w: cur = t
        else: lines.append(cur); cur = wd
    return lines + [cur]


def cover(label, title, foot, path_stems):
    W, H = 1200, 630
    im = Image.new('RGB', (W, H))
    px = im.load()
    for y in range(H):                                   # --dark-bg → a touch lighter, top to bottom
        t = y / H; c = (int(14 + 8 * t), int(31 + 14 * t), int(14 + 10 * t))
        for x in range(W): px[x, y] = c
    d = ImageDraw.Draw(im)
    gold, cream = (201, 164, 107), (244, 236, 214)
    d.rectangle([28, 28, W - 29, H - 29], outline=(201, 164, 107), width=2)
    d.rectangle([38, 38, W - 39, H - 39], outline=(122, 98, 62), width=1)
    spaced(d, (84, 84), 'SERMON OF MUTTAQIN', font(24), gold, 5)
    d.line([(84, 128), (284, 128)], fill=gold, width=2)
    d.text((84, 150), label, font=font(46), fill=gold)
    sz = 64
    while True:
        f = font(sz); lines = wrap(d, title, f, 700)
        if len(lines) <= 3 or sz <= 44: break
        sz -= 4
    y = 232
    for ln in lines:
        d.text((84, y), ln, font=f, fill=cream); y += int(sz * 1.22)
    d.text((84, H - 104), foot, font=font(24), fill=(168, 150, 112))
    logo = Image.open(ROOT + 'assets/logo.png').convert('RGBA').resize((250, 250), Image.LANCZOS)
    im.paste(logo, (880, 190), logo)
    for stem, size in path_stems:
        out = im if size is None else im.resize(size, Image.LANCZOS)
        out.save(D + stem, 'JPEG', quality=84, progressive=True, optimize=True)


def make_covers():
    os.makedirs(D, exist_ok=True)
    for n, (vid, pub, short, yt) in MC.PARTS.items():
        s = f'{SER}-{n}-{LANG}'
        cover(f'Part {n}', yt[0].upper() + yt[1:], 'Imam Ali (p)  ·  Khutbat al-Muttaqin',
              [(f'{s}.jpg', None), (f'og-{s}.jpg', None), (f'thumb-{s}.jpg', (480, 270))])
    s = f'{SER}-cover-{LANG}'
    cover('The Series', 'The Sermon of the God-Conscious', 'Imam Ali (p)  ·  Khutbat al-Muttaqin',
          [(f'{s}.jpg', None), (f'og-{s}.jpg', None), (f'thumb-{s}.jpg', (480, 270))])


# ── body ─────────────────────────────────────────────────────────────────
def mbody(a):
    out, refs = [], a['refs']
    for k, t in a['blocks']:
        if k == 'H': out.append(f'<h3 class="art-section-title">{esc(t)}</h3>')
        elif k == 'S': out.append(f'<p class="kw-subhead">{esc(t)}</p>')
        elif k == 'A': out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{esc(t)}</span></div>')
        else: out.append('<p>' + esc(t).replace('\n', '<br>') + '</p>')
    if refs:
        out.append('<h3 class="art-section-title">References</h3>')
        out.append('<ul class="kw-sources-list">' + ''.join(f'<li>{esc(r)}</li>' for r in refs) + '</ul>')
    return out


BA.body_html = mbody


def sref(n=None): return f'/articles/{SER}/' + (f'{n}/' if n else '')


def load(n):
    vid, pub, short, yt = MC.PARTS[n]
    blocks, refs = MC.parse(n)
    title = f'{NAME}, Part {n} — {yt[0].upper() + yt[1:]}'
    return dict(title=title, desc=DESC[n], published=pub, modified=pub, heads=[], hero_video=vid, body=[{'t': 'p', 'x': t} for _, t in blocks],   # real text: page() counts words from it for the reading time
                
                tags=['Imam Ali (p)'], og='x', img=dict(w=1200, h=630, orig=(1200, 630)), blocks=blocks, refs=refs, short=short, yt=yt)


def retitle(path, n):
    """The page title tag: short, unique, ≤ ~65 characters (the h1 keeps the full YouTube title)."""
    tt = f"{NAME} {n}: {SHORT[n]} | Misbah Inc."
    assert len(tt) <= 75, (n, len(tt), tt)
    s = open(ROOT + path, encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', f'<title>{html.escape(tt, quote=False)}</title>', s, count=1, flags=re.S)
    for pat in (r'(property="og:title"\s+content=")[^"]*', r'(name="twitter:title"\s+content=")[^"]*'):
        s = re.sub(pat, lambda m: m.group(1) + html.escape(tt, quote=True), s, count=1)
    open(ROOT + path, 'w', encoding='utf-8').write(s)


def main():
    make_covers()
    CAT = json.load(open(HERE + 'catalog.json'))
    arts = {n: load(n) for n in MC.PARTS}
    for n, a in arts.items():
        sr = dict(name=NAME, href=sref(), n=n)
        if n - 1 in arts: sr['prev'] = (sref(n - 1), arts[n - 1]['title'])
        if n + 1 in arts: sr['next'] = (sref(n + 1), arts[n + 1]['title'])
        path = page(f'{SER}/{n}', LANG, a, [LANG], TP, series=sr)
        retitle(path, n)
        CAT[f'{SER}/{n}'] = dict(slug=f'{SER}/{n}', series=SER, month=3, langs=[LANG], titles={LANG: a['title']}, tags=a['tags'], tags_l={LANG: a['tags']},
                                 published=a['published'], img=True, descs={LANG: a['desc']})
    CAT[SER] = dict(slug=SER, kind='series', month=3, langs=[LANG], titles={LANG: NAME}, tags=[], tags_l={}, published=SERIES_DATE, img=True, descs={LANG: SERIES_DESC})
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    series_page(arts)
    print('built', len(arts), 'parts; title lengths', {n: len(f"{NAME} {n}: {SHORT[n]} | Misbah Inc.") for n in arts})


def series_page(arts):
    L = S[LANG]; tp = TP[LANG]
    intro = next(t for k, t in arts[1]['blocks'] if k == 'P')
    cur = f'{SITE}{sref()}'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": cur + "#webpage", "url": cur, "name": NAME, "description": SERIES_DESC, "inLanguage": LANG,
         "isPartOf": {"@id": SITE + "/#website"},
         "mainEntity": {"@type": "CreativeWorkSeries", "name": NAME, "numberOfItems": len(arts),
                        "hasPart": [{"@type": "Article", "name": a['title'], "url": SITE + sref(n), "datePublished": a['published']} for n, a in arts.items()]}},
        breadcrumb_ld(LANG, [(NAME, None)]), ORG]}
    og = f'/images/articles/og-{SER}-cover-{LANG}.jpg'
    title_tag = f'{NAME} (Khutbat al-Muttaqin) | {L["brand"]}'
    h = head(LANG, tp, title=title_tag, desc=BA.clip(SERIES_DESC, 160), parts=(), og_img=og, og_type='website', published='', ld=ld)
    hl = f'  <link rel="alternate"  hreflang="en" href="{cur}">\n  <link rel="alternate"  hreflang="x-default" href="{cur}">'
    h = re.sub(r'  <!-- Canonical \+ hreflang -->.*?(?=\n\n  <!-- Open Graph)', f'  <!-- Canonical + hreflang -->\n  <link rel="canonical"  href="{cur}">\n{hl}', h, flags=re.S)
    h = h.replace(f'content="{SITE}{PFX[LANG]}/articles/{G.SLUG}/"', f'content="{cur}"')
    cards = ''
    for n, a in sorted(arts.items()):
        cards += f'''
    <a class="kw-part-card" href="{sref(n)}">
      <img src="/images/articles/thumb-{SER}-{n}-{LANG}.jpg" alt="" width="480" height="270" loading="lazy" decoding="async">
      <div class="kw-part-body">
        <span class="kw-series-chip">Part {n}</span>
        <h2>{esc(a['yt'][0].upper() + a['yt'][1:])}</h2>
        <p>{esc(a['desc'])}</p>
        <span class="btn btn-gold">{L['read']}</span>
      </div>
    </a>'''
    main = f'''<main>

<div class="kw-banner-wrap"><div class="kw-banner"><img src="/images/articles/{SER}-cover-{LANG}.jpg" alt="{html.escape(NAME, quote=True)}" width="1200" height="630" fetchpriority="high"></div></div>
{crumbs(LANG, [(NAME, None)])}

<div class="art-page">
  <div class="art-container">

    <a href="/articles/" class="art-back">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <path d="M19 12H5M12 5l-7 7 7 7"/>
      </svg>
      {L['all']}
    </a>

    <div class="art-meta"><span class="art-tag">{L['tag']}</span></div>

    <div class="art-title-block">
      <h1 class="art-title">{esc(NAME)}</h1>
    </div>

    <p class="art-intro">{esc(intro)}</p>

    <h2 class="art-section-title">{L['parts']}</h2>
    <div class="kw-parts">{cards}
    </div>

  </div>
</div>

</main>

'''
    tail = f'\n{tp["footer"]}\n\n<script src="/assets/theme.js"></script>\n<script src="/assets/script.js"></script>\n</body>\n</html>\n'
    os.makedirs(ROOT + f'articles/{SER}', exist_ok=True)
    open(ROOT + f'articles/{SER}/index.html', 'w', encoding='utf-8').write(h + main + tail)


# ── homepage ─────────────────────────────────────────────────────────────
def home():
    """English homepage only (the series exists only in English): 'Latest series' card right after Topics."""
    path = ROOT + 'index.html'
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<!-- ═+\s*\n\s*LATEST SERIES — Sermon of Muttaqin.*?</section>\s*', '', s, flags=re.S)   # idempotent
    btns = '\n'.join(f'      <a href="{sref(n)}" class="ch-btn" role="listitem" aria-label="Part {n}">{n}</a>' for n in MC.PARTS)
    block = f'''<!-- ═══════════════════════════════════════
     LATEST SERIES — Sermon of Muttaqin (articles/{SER}/) — generated by tools/wix_import/build_muttaqin.py
════════════════════════════════════════ -->
<section class="section kw-home" id="muttaqin-series" aria-labelledby="mq-heading">
  <div class="container text-center">
    <span class="section-label">Latest series</span>
    <h2 class="section-title" id="mq-heading">{NAME}</h2>
    <div class="divider" aria-hidden="true"><span class="divider-gem">◆</span></div>

    <article class="kw-home-card">
      <a href="{sref()}" tabindex="-1" aria-hidden="true"><img src="/images/articles/{SER}-cover-{LANG}.jpg" alt="" width="1200" height="630" loading="lazy" decoding="async" style="object-fit:contain;background:#14281a"></a>
      <div class="kw-home-body">
        <span class="kw-series-chip" style="align-self:flex-start">Series</span>
        <p>The Sermon of Muttaqin (Khutbat al-Muttaqin) by Imam Ali (p) describes the God-conscious one characteristic at a time. Each part opens with its video, followed by the text and the stories behind it.</p>
        <p class="chapters-label">Choose a part</p>
        <div class="chapters-row" role="list">
{btns}
        </div>
        <a href="{sref()}" class="btn btn-gold">View the series</a>
      </div>
    </article>
  </div>
</section>

'''
    # above the Topics section (build_home_topics.py re-inserts Topics before Featured, so this order is stable)
    m = re.search(r'<!-- ═+\s*\n\s*TOPICS —', s) or re.search(r'<!-- ═+\s*\n\s*FEATURED ARTICLE', s)
    assert m, 'topics / featured banner not found'
    s = s[:m.start()] + block + s[m.start():]
    open(path, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    main()
    home()
