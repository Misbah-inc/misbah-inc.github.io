"""Booklet PDFs (misbah-inc.com/book*) -> article series. English only.

Usage: python3 build_booklets.py <dir with <pdf id>.pdf files> [id ...]
Source list and mapping: BOOKS below (ids are the Wix file ids, 9d042c_<32 hex>). Re-runnable per booklet.
Text comes from the PDF's text layer unchanged; Arabic lines are crops of the page (see booklet_extract.py).
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
import build_mourning as M
import booklet_extract as BX
from PIL import Image, ImageFilter, ImageEnhance

LANG = 'en'
TP = {LANG: template(LANG)}
D = ROOT + 'images/articles/'
PDF_URL = 'https://www.misbah-inc.com/_files/ugd/%s.pdf'
SERIES = {
 'muharram-safar-booklets': dict(name='Muharram & Safar Booklets', month=1,
     desc='Illustrated booklets for Muharram and Safar: the nights of Ashura, the family of Imam Hussain (p), mourning and Arbaeen, from Misbah Inc.'),
 'ramadan-booklets': dict(name='Ramadan Booklets', month=9,
     desc='Ramadan booklets from Misbah Inc.: ziyarat and reflections for the month of Ramadan.'),
 'ghadir-booklets': dict(name='Ghadir Booklets', month=12,
     desc='Illustrated Ghadir booklets: stories of the Prophet (p) and Imam Ali (p), from the first call at Dhul-Ashira to the day of Ghadir Khumm, from Misbah Inc.'),
}
# (series, n, title, Wix file id).  Titles are the ones on misbah-inc.com/book-*; order = the Wix page.
# Arabic lines are always kept as cropped images (the PDF text layer scrambles Arabic); clean Arabic text can replace them later.
# Not built (needs a decision): Treasures of the Family of Muhammad (599 pp), School of Umm al-Banin full book (108 pp, 4f5c0040), Ramadan Workbook (91 MB),
# three image-only Ramadan PDFs (no text layer), Ziyarat of Lady Fatima (2-page Arabic-only, 965e8e1c).
BOOKS = [
 ('muharram-safar-booklets', 1, 'The Night of Loyalty', '9d042c_cacda01c10514a52a205ca1ccae961f6'),
 ('muharram-safar-booklets', 2, 'The Night of Repentance', '9d042c_d46a7ace923e49b2993d765679839004'),
 ('muharram-safar-booklets', 3, 'The Night of Reunion', '9d042c_18a40dbecf204d8981dd5913f6c521f5'),
 ('muharram-safar-booklets', 4, 'The Night of the Witness', '9d042c_0513873e8dcd4d349438ccad2a715a02'),
 ('muharram-safar-booklets', 5, 'The Night of Patience', '9d042c_d514cce5dd6e4ba98472adab2dc4a2e3'),
 ('muharram-safar-booklets', 6, 'The Night of Longing', '9d042c_5953684c1ef14428b3427a519886e0fd'),
 ('muharram-safar-booklets', 7, 'The Night of Labbayk', '9d042c_bc31c6da921c4326ba2cc6e15a758063'),
 ('muharram-safar-booklets', 8, 'The Night of Perfection', '9d042c_e49aee20898443f982d3a02a22674a9e'),
 ('muharram-safar-booklets', 9, 'Heartfelt Writings for Star of the Hearts, Lady Ruqayyah (PBUH)', '9d042c_093d1e7c2ffd4a8185dbf1e74325cbad'),
 ('muharram-safar-booklets', 10, 'Ziyārat Nāḥiyah al-Muqaddasah', '9d042c_39e39f9832d84559b1f6bce6f2d32072'),
 ('muharram-safar-booklets', 11, 'The Reality of Weeping for Hussain (PBUH)', '9d042c_34411530e46b4f1fbe1a124a37b35e1d'),
 ('muharram-safar-booklets', 12, 'Ziarat and the Virtues of Imam Ali ibn al-Hussain (PBUH) in the Hadith of the Tablet', '9d042c_d85d954a724a4dcb99b4f555a86f0493'),
 ('muharram-safar-booklets', 13, 'Shared Traits of Hazrat Ali Akbar and Lady Ruqayyah (PBUT)', '9d042c_017c1a1d668842378f51a89ccdecb704'),
 ('muharram-safar-booklets', 14, 'Sermon of Imam al-Hasan (PBUH) on the Peace Treaty', '9d042c_3b27a2e9256546a4952ff8309fb6c0c2'),
 ('muharram-safar-booklets', 15, 'Ziarat Lady Ummul Banin (p)', '9d042c_9ffb931fcd9346d789b80865c4539cd6'),
 ('muharram-safar-booklets', 16, 'The School of the Lady of Baqi, Bibi Umm al-Banin (SA) — Summary', '9d042c_5375ec4a1d4b4340ba0fc3fe37ac3d18'),
 ('muharram-safar-booklets', 17, 'The Final Lament of Reyḥānat al-Ḥusayn, Ruqayyah al-Murtaqa (PBUH)', '9d042c_83ed330b2de14140b89fb8712cedc1a7'),
 ('muharram-safar-booklets', 18, 'Walking Path of Hussain (AS)', '9d042c_18ce5baa8d6148eb80cbf3383d7e3918'),
 ('ghadir-booklets', 1, 'The Sun', '9d042c_c0a00132abc54e20bf509f9b0a1137f8'),
 ('ghadir-booklets', 2, 'The Successor', '9d042c_13894ad4e6754993ab72be1cd655b492'),
 ('ghadir-booklets', 3, 'Wali', '9d042c_4d8c3f7b0b734cbba5fba313a63ddac7'),
 ('ghadir-booklets', 4, 'The Conqueror', '9d042c_45922db9944447bfa2b949a8ac8a691e'),
 ('ghadir-booklets', 5, 'The Uncle', '9d042c_556691d48b6248e98957945e99fa2450'),
 ('ghadir-booklets', 6, 'Sermon of Mufakhirah', '9d042c_1378569b6a234701b7fa41700f891459'),
 ('ghadir-booklets', 7, 'Excerpt from Ziyārat of Ghadīriyya by Imam al-Hādi (PBUH)', '9d042c_43bc622ce8534e5db3fe6b2d95095dae'),
 ('ghadir-booklets', 8, 'Ziyārat of Hazrat Ali Akbar (pbuh)', '9d042c_ea80a569d4894eacb08224b65782c288'),
 ('ghadir-booklets', 9, 'Spring of Love', '9d042c_42c53d9d54d249e0bd67265afe1453db'),
 ('ramadan-booklets', 1, 'Ziyārat of Hazrat Khadija (pbuh)', '9d042c_87972fd4152248ff9eb39d1665daa3be'),
]
BANNER_W = 720


def letterbox(im, W, H):
    bg = im.resize((W, round(W * im.height / im.width)), Image.LANCZOS)
    y = max(0, (bg.height - H) // 2)
    bg = ImageEnhance.Brightness(bg.crop((0, y, W, y + H)).filter(ImageFilter.GaussianBlur(H / 22))).enhance(0.45)
    fg = im.resize((round(H * im.width / im.height), H), Image.LANCZOS)
    bg.paste(fg, ((W - fg.width) // 2, 0))
    return bg


def save_jpg(im, path, q=82, limit=200_000):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    while True:
        im.save(path, 'JPEG', quality=q, progressive=True, optimize=True)
        if os.path.getsize(path) <= limit or q <= 60: return
        q -= 4


def rbody(a):
    out = []
    for it in a['items']:
        if it[0] == 'P':
            out.append('<p>' + esc(it[1]).replace('\\n', '<br>') + '</p>')
        elif it[0] == 'AR':
            out.append(f'<figure class="art-fig"><img src="{it[1]}" alt="Arabic text quoted in the booklet" lang="ar" width="{it[2]}" height="{it[3]}" loading="lazy" decoding="async"></figure>')
        else:
            out.append(f'<figure class="art-fig"><img src="{it[1]}" alt="{html.escape(a["title"], quote=True)} — illustration" width="{it[2]}" height="{it[3]}" loading="lazy" decoding="async"></figure>')
    out.append(f'<p class="kw-subhead"><a href="{a["pdf"]}" rel="noopener">Download the original PDF (English)</a></p>')
    return out


BA.body_html = rbody


def build_one(pdfdir, ser, n, title, fid):
    S_ = SERIES[ser]
    r = BX.extract(f'{pdfdir}/{fid}.pdf')
    slug = f'{ser}/{n}'; fs = f'{ser}-{n}'
    items, k = [], 0
    p1 = r['pages'][0]
    p1_is_cover = sum(len(t[1]) for t in p1 if t[0] == 'P') < 150 and not any(t[0] == 'AR' for t in p1)   # a title page, not a 2-page ziyarat that starts at once
    for pi, page_items in enumerate(r['pages']):
        if pi == 0 and p1_is_cover: continue                  # page 1 = the cover (title + subtitle)
        for it in page_items:
            if it[0] == 'P': items.append(('P', it[1]))
            else:
                k += 1
                rel = f'/images/articles/{ser}/{n}/{pi + 1}-{k}.jpg'
                os.makedirs(os.path.dirname(ROOT + rel[1:]), exist_ok=True)
                open(ROOT + rel[1:], 'wb').write(it[1])
                items.append((it[0], rel, it[2], it[3]))
    cover_txt = [it[1] for it in r['pages'][0] if it[0] == 'P'] if p1_is_cover else []
    # the cover's lines after the title are the subtitle ("The Companions of Hussain – The Seventy-Two Souls"); covers without a text title have none
    norm = lambda t: re.sub(r'[^a-z]', '', t.lower())
    sub = ' '.join(cover_txt[1:]).strip() if cover_txt and norm(cover_txt[0])[:8] == norm(title)[:8] and len(cover_txt) > 1 else ''
    text = ' '.join(t[1] for t in items if t[0] == 'P')
    first = next((t[1] for t in items if t[0] == 'P' and len(t[1]) > 40), text)
    desc = BA.clip(f'{title}: {sub}. {first}' if sub else f'{title}. {first}', 160)
    cd = (r['meta'].get('creationDate') or '')[2:10]
    pub = f'{cd[:4]}-{cd[4:6]}-{cd[6:8]}' if len(cd) == 8 else '2025-06-26'
    # covers: page 1 as a portrait banner; OG + thumb letterboxed on a blurred copy
    cov = r['cover']
    ban = cov.resize((BANNER_W, round(BANNER_W * cov.height / cov.width)), Image.LANCZOS)
    save_jpg(ban, D + f'{fs}-{LANG}.jpg')
    save_jpg(letterbox(cov, 1200, 630), D + f'og-{fs}-{LANG}.jpg')
    save_jpg(letterbox(cov, 480, 270), D + f'thumb-{fs}-{LANG}.jpg', 82, 60_000)
    a = dict(title=title, desc=desc, published=pub, modified=pub, heads=([{'t': 'blockquote', 'x': sub}] if sub else []), hero_video=None,
             body=[{'t': 'p', 'x': t[1]} for t in items if t[0] == 'P'], tags=['Booklet'], og='x', items=items, pdf=PDF_URL % fid,
             img=dict(w=ban.width, h=ban.height, orig=cov.size), n=n)
    return slug, a


def retitle(path, title, series_name):
    """<title> = "<booklet> — <series> | Misbah Inc." (titles like "The Sun" are meaningless alone), at most ~70 characters."""
    tail = f' — {series_name} | Misbah Inc.'
    if len(title) + len(tail) <= 70: tt = title + tail
    else: tt = (title if len(title) <= 56 else BA.clip(title, 56)) + ' | Misbah Inc.'
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{html.escape(tt, quote=False)}</title>', s, count=1, flags=re.S)
    for pat in (r'(property="og:title"\s+content=")[^"]*', r'(name="twitter:title"\s+content=")[^"]*'):
        s = re.sub(pat, lambda m: m.group(1) + html.escape(tt, quote=True), s, count=1)
    open(path, 'w', encoding='utf-8').write(s)


def main():
    pdfdir = sys.argv[1]; only = set(sys.argv[2:])
    CAT = json.load(open(HERE + 'catalog.json'))
    built = {}
    for ser, n, title, fid in BOOKS:
        if only and fid not in only and fid[7:15] not in only: continue
        if not os.path.exists(f'{pdfdir}/{fid}.pdf'): print('missing pdf', fid); continue
        slug, a = build_one(pdfdir, ser, n, title, fid)
        built.setdefault(ser, {})[n] = a
    for ser, chs in built.items():
        S_ = SERIES[ser]
        allc = {n: a for n, a in chs.items()}
        for n, a in chs.items():
            sr = dict(name=S_['name'], href=f'/articles/{ser}/', n=n)
            if n - 1 in allc: sr['prev'] = (f'/articles/{ser}/{n - 1}/', allc[n - 1]['title'])
            if n + 1 in allc: sr['next'] = (f'/articles/{ser}/{n + 1}/', allc[n + 1]['title'])
            path = page(f'{ser}/{n}', LANG, a, [LANG], TP, series=sr)
            retitle(ROOT + path, a['title'], S_['name'])
            CAT[f'{ser}/{n}'] = dict(slug=f'{ser}/{n}', series=ser, month=S_['month'], langs=[LANG], titles={LANG: a['title']}, tags=a['tags'], tags_l={LANG: a['tags']},
                                     published=a['published'], img=True, descs={LANG: a['desc']})
        CAT[ser] = dict(slug=ser, kind='series', month=S_['month'], langs=[LANG], titles={LANG: S_['name']}, tags=[], tags_l={}, published=max(a['published'] for a in chs.values()),
                        img=True, descs={LANG: S_['desc']})
        M.SER, M.NAME, M.series_desc, M.TP = ser, {LANG: S_['name']}, (lambda lang, d=S_['desc']: d), TP
        M.series_page(LANG, {(LANG, n): dict(a, heads=[{'t': 'p', 'x': f'Booklet {n}'}]) for n, a in chs.items()}, [LANG])
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    print('built', {s: sorted(c) for s, c in built.items()})


if __name__ == '__main__':
    main()
