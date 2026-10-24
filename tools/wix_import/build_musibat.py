"""Musibat al-Zahra (#مصیبة_الزهراء #فاطمیه): the Friday posts of the Fatimiyya season, as a series in four languages.

Source: the four channels, one post each Friday (2, 9, 16, 23 Oct 2026) with its square picture (work/tg/musibat-posts.json; the
pictures are the channels' photo posts, 800×800). Text word for word; removed: hashtags, the 🥀▪️ and ━━━ dividers, the @channel footer.
The post's title line (🏴 TITLE 🏴) is the page heading; each ⚜️ / ✨ « … » line is a quotation box; the (1) (2) … after sentences are
footnote links into the collapsible Sources list (the post's 📚 block). usage: python3 build_musibat.py
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
from PIL import Image, ImageFilter, ImageEnhance

LANGS4 = ['en', 'ar', 'fa', 'ur']
SLUG = 'musibat-al-zahra'
D = ROOT + 'images/articles/'
POSTS = json.load(open(HERE + 'work/tg/musibat-posts.json', encoding='utf-8'))
DATES = {'1': '2026-10-02', '2': '2026-10-09', '3': '2026-10-16', '4': '2026-10-23'}
NAME = {'en': 'The Calamity of Lady Zahra (p)', 'ar': 'مصيبة الزهراء (ع)', 'fa': 'مصیبة الزهراء (س)', 'ur': 'مصیبة الزهراء (س)'}
SERIES_DESC = {'en': 'Weekly Friday reflections of the Misbah channel in the days of Fatimiyya on the calamity of Lady Fatimah al-Zahra (p).',
               'ar': 'تأمّلات أسبوعية (كل جمعة) من قناة مصباح في الأيام الفاطمية حول مصيبة السيدة فاطمة الزهراء (ع).',
               'fa': 'نوشتارهای هفتگی (هر جمعه) کانال مصباح در ایام فاطمیه درباره‌ی مصیبت حضرت فاطمه زهرا (س).',
               'ur': 'ایامِ فاطمیہ میں مصباح چینل کی ہفتہ وار (ہر جمعہ) تحریریں، حضرت فاطمہ زہرا (س) کی مصیبت کے بارے میں۔'}
UI = {'en': 'Sources', 'ar': 'المصادر', 'fa': 'منابع', 'ur': 'حوالہ جات'}
DIV = re.compile(r'^[\s━▪️🥀➖─\-–—_•·✦❁🌸]*$')
FOOT = re.compile(r'\((\d+)\)')
ESC = lambda t: html.escape(t, quote=False)


def parse(text):
    title, blocks, sources, in_src = '', [], [], False
    for para in re.split(r'\n\s*\n', text):
        lines = [l.strip() for l in para.split('\n') if l.strip() and not l.strip().startswith(('#', '@', '🥀 @')) and not DIV.match(l.strip())]
        if not lines: continue
        if lines[0].startswith('📚'):
            in_src = True; lines = lines[1:]
        if in_src:
            for l in lines:
                m = re.match(r'^\((\d+)\)\s*(.*)$', l)
                if m: sources.append([int(m.group(1)), m.group(2)])
                elif sources: sources[-1][1] += ' ' + l
            continue
        l0 = lines[0]
        if not title and l0.startswith('🏴') and l0.rstrip().endswith('🏴'):
            title = l0.strip('🏴 ').strip(); lines = lines[1:]
            if not lines: continue; 
        if lines[0][:1] in ('⚜', '✨') or lines[0].startswith(('⚜️', '✨')):
            quote = [re.sub(r'^[⚜️✨\s️]+', '', l) for l in lines]
            blocks.append(('q', quote)); continue
        blocks.append(('p', ' '.join(re.sub(r'^[🔲▪✔➖🖊🏴⚜✨️\s]+', '', l) for l in lines)))
    return title, blocks, sources


def sup(t): return FOOT.sub(lambda m: f'<sup class="bio-ref"><a href="#src-0-{m.group(1)}">[{m.group(1)}]</a></sup>', ESC(t))


def body(a):
    out = []
    for k, t in a['blocks']:
        if k == 'q':
            main = [x for x in t if not x.startswith(('—', '–'))]; ref = [x for x in t if x.startswith(('—', '–'))]
            out.append('<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">' + '<br>'.join(sup(x) for x in main) + '</span>'
                       + ''.join(f'<span class="quran-ref">{ESC(x)}</span>' for x in ref) + '</div>')
        else: out.append(f'<p>{sup(t)}</p>')
    if a['sources']:
        lis = ''.join(f'<li id="src-0-{n}" value="{n}">{ESC(t)}</li>' for n, t in a['sources'])
        out.append(f'<div class="bio-sources"><button type="button" class="bio-sources-btn" aria-expanded="false" aria-controls="bio-src-body"><span>{UI[a["lang"]]}</span><span class="bio-sources-chevron" aria-hidden="true">▾</span></button>'
                   f'<div class="bio-sources-body" id="bio-src-body"><div class="bio-src-group"><ol>{lis}</ol></div></div></div>')
    return ['<div class="bio-ch">'] + out + ['</div>']


BA.body_html = body


def pictures(n, src):
    im = Image.open(src).convert('RGB')
    for l in LANGS4:
        im.save(D + f'{SLUG}-{n}-{l}.jpg', 'JPEG', quality=84, progressive=True, optimize=True)
        for stem, (W, H) in ((f'og-{SLUG}-{n}-{l}.jpg', (1200, 630)), (f'thumb-{SLUG}-{n}-{l}.jpg', (480, 270))):
            bg = im.resize((W, round(W * im.height / im.width)), Image.LANCZOS)
            y = (bg.height - H) // 2
            bg = ImageEnhance.Brightness(bg.crop((0, y, W, y + H)).filter(ImageFilter.GaussianBlur(H / 22))).enhance(0.45)
            fg = im.resize((round(H * im.width / im.height), H), Image.LANCZOS)
            bg.paste(fg, ((W - fg.width) // 2, 0)); bg.save(D + stem, 'JPEG', quality=82, progressive=True, optimize=True)
    return im.size


def build():
    import build_mourning as M
    CAT = json.load(open(HERE + 'catalog.json'))
    TP = {l: template(l) for l in LANGS4}
    arts, sizes = {}, {}
    for n, posts in POSTS.items():
        src = f'/private/tmp/claude-501/-Users-mohammad-Developer-misbah-app/9308e757-88c6-47b5-b1f7-fb7f616f0215/scratchpad/tgimg/mz{n}-en.jpg'
        keep = ROOT + f'images/musibat-al-zahra-{n}.jpg'
        if os.path.exists(src): Image.open(src).save(keep, quality=90)
        sizes[n] = pictures(n, keep)
        for l in LANGS4:
            title, blocks, sources = parse(posts[l]['text'])
            if l == 'en': title = title.title().replace("'S", "'s")
            first = ' '.join(t for k, t in blocks if k == 'p')[:400]
            arts[(l, int(n))] = dict(lang=l, title=title, desc=BA.clip(re.sub(r'\s+', ' ', first), 160), published=DATES[n], modified=DATES[n],
                                     heads=[{'t': 'p', 'x': S[l]['part'].format(n=num(int(n), l))}], hero_video=None, body=[{'t': 'p', 'x': t if isinstance(t, str) else ' '.join(t)} for k, t in blocks],
                                     tags=[], og='x', img=dict(w=sizes[n][0], h=sizes[n][1], orig=sizes[n]), blocks=blocks, sources=sources)
    for (l, n), a in arts.items():
        href = lambda k=None, lg=l: f"{PFX[lg]}/articles/{SLUG}/" + (f'{k}/' if k else '')
        sr = dict(name=NAME[l], href=href(), n=n)
        if (l, n - 1) in arts: sr['prev'] = (href(n - 1), arts[(l, n - 1)]['title'])
        if (l, n + 1) in arts: sr['next'] = (href(n + 1), arts[(l, n + 1)]['title'])
        BA.page(f'{SLUG}/{n}', l, a, LANGS4, TP, series=sr)
        CAT[f'{SLUG}/{n}'] = dict(slug=f'{SLUG}/{n}', series=SLUG, month=5, langs=LANGS4, titles={ll: arts[(ll, n)]['title'] for ll in LANGS4},
                                  tags=[], tags_l={ll: [] for ll in LANGS4}, published=DATES[str(n)], img=True, descs={ll: arts[(ll, n)]['desc'] for ll in LANGS4})
    M.SER, M.NAME, M.series_desc, M.TP = SLUG, NAME, (lambda lang: SERIES_DESC[lang]), TP
    for l in LANGS4:
        M.series_page(l, {(l, n): arts[(l, n)] for n in range(1, 5)}, LANGS4)
    CAT[SLUG] = dict(slug=SLUG, kind='series', month=5, langs=LANGS4, titles=NAME, tags=[], tags_l={}, published=max(DATES.values()), img=True, descs=SERIES_DESC)
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    print('built', len(arts))


if __name__ == '__main__':
    if '--dry' in sys.argv:
        for n, posts in POSTS.items():
            for l in LANGS4:
                title, blocks, sources = parse(posts[l]['text'])
                print(n, l, repr(title[:40]), ''.join(k for k, _ in blocks), [s[0] for s in sources])
    else: build()
