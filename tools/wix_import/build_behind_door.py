"""Behind That Door… (#جمادی_الاول #فاطمیه): the Fatimiyya evening posts of Jumada al-Ula 1448, as a series in four languages.

Source: the four channels, Parts 1–5 posted 26, 28, 31 Oct, 2 and 4 Nov 2026 (work/tg/behind-door-posts.json). Every part carries
the same square picture (the channels' photo post, 800×800, no text on it), so the series has one picture. Text word for word;
removed: hashtags, the 🥀▪️ dividers, the @channel footer. The "🩸<series> | n" line names the series, the line under it is the
part's heading. A 📋 line is an Arabic quotation box, the ▪️ line after it its translation; the post's line breaks are kept
(the prose is written in short lines); (1) (2) … are footnote links into the collapsible Sources list (the 📚 lines).
usage: python3 build_behind_door.py [--dry]
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
from PIL import Image, ImageFilter, ImageEnhance

LANGS4 = ['en', 'ar', 'fa', 'ur']
SLUG = 'behind-that-door'
MONTH = 5                                                          # Jumada al-Ula
D = ROOT + 'images/articles/'
POSTS = json.load(open(HERE + 'work/tg/behind-door-posts.json', encoding='utf-8'))
PIC = '/private/tmp/claude-501/-Users-mohammad-Developer-misbah-app/9308e757-88c6-47b5-b1f7-fb7f616f0215/scratchpad/tgimg/btd1-en.jpg'
# the series name as the posts write it
NAME = {'en': 'Behind That Door…', 'ar': 'خلفَ ذلك الباب…', 'fa': 'پشتِ آن در…', 'ur': 'اُس دروازے کے پیچھے…'}
SERIES_DESC = {'en': 'A Fatimiyya series from the Misbah channels in Jumada al-Ula on the sufferings of Lady Fatimah al-Zahra (p), told through the narrations.',
               'ar': 'سلسلة فاطمية من قنوات مصباح في شهر جمادى الأولى عن مصائب السيدة فاطمة الزهراء (ع)، من خلال الروايات.',
               'fa': 'مجموعه‌ای فاطمی از کانال‌های مصباح در ماه جمادی‌الاول درباره‌ی مصائب حضرت فاطمه زهرا (س)، از زبان روایات.',
               'ur': 'ماہِ جمادی الاول میں مصباح چینلز کا فاطمی سلسلہ، حضرت فاطمہ زہرا (س) کے مصائب کے بارے میں، روایات کی روشنی میں۔'}
UI = {'en': 'Sources', 'ar': 'المصادر', 'fa': 'منابع', 'ur': 'حوالہ جات'}
DIV = re.compile(r'^[\s▪️🥀━➖─\-–—_•·✦]*$')
FOOT = re.compile(r'\((\d+)\)|\(([۰-۹٠-٩]+)\)')
DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
ESC = lambda t: html.escape(t, quote=False)


def parse(text):
    """-> (heading, blocks, sources); blocks: ('q', arabic) | ('t', translation) | ('p', [lines])"""
    heading, blocks, sources = '', [], []
    lines = [l.strip() for l in text.split('\n')]
    i = 0
    while i < len(lines) and not lines[i].startswith('🩸'): i += 1
    i += 1                                                         # the "🩸<series> | n" line
    while i < len(lines) and not lines[i]: i += 1
    if i < len(lines): heading = lines[i]; i += 1
    buf = []
    def flush():
        nonlocal buf
        if buf: blocks.append(('p', buf)); buf = []
    for l in lines[i:]:
        if not l or DIV.match(l): flush(); continue
        if l.startswith(('#', '@')): continue
        if l.startswith('📚'):
            flush()
            m = re.match(r'^📚\s*\(([\d۰-۹٠-٩]+)\)\s*(.*)$', l)
            if m: sources.append([int(m.group(1).translate(DIGITS)), m.group(2)])
            elif sources: sources[-1][1] += ' ' + l.lstrip('📚 ')
            continue
        if l.startswith('📋'): flush(); blocks.append(('q', l.lstrip('📋 ').strip())); continue
        if l.startswith('▪️') or l.startswith('▪'): flush(); blocks.append(('t', re.sub(r'^[▪️\s]+', '', l))); continue
        buf.append(l)
    flush()
    return heading, blocks, sources


def sup(t):
    return FOOT.sub(lambda m: (lambda n: f'<sup class="bio-ref"><a href="#src-0-{n}">[{n}]</a></sup>')((m.group(1) or m.group(2)).translate(DIGITS)), ESC(t))


def body(a):
    out = []
    for k, t in a['blocks']:
        if k == 'q': out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{sup(t)}</span></div>')
        elif k == 't': out.append(f'<p class="art-quote-tr">{sup(t)}</p>')
        else: out.append('<p>' + '<br>'.join(sup(x) for x in t) + '</p>')
    if a['sources']:
        lis = ''.join(f'<li id="src-0-{n}" value="{n}">{ESC(t)}</li>' for n, t in a['sources'])
        out.append(f'<div class="bio-sources"><button type="button" class="bio-sources-btn" aria-expanded="false" aria-controls="bio-src-body"><span>{UI[a["lang"]]}</span><span class="bio-sources-chevron" aria-hidden="true">▾</span></button>'
                   f'<div class="bio-sources-body" id="bio-src-body"><div class="bio-src-group"><ol>{lis}</ol></div></div></div>')
    return ['<div class="bio-ch">'] + out + ['</div>']


BA.body_html = body


def pictures(n, im):
    for l in LANGS4:
        im.save(D + f'{SLUG}-{n}-{l}.jpg', 'JPEG', quality=84, progressive=True, optimize=True)
        for stem, (W, H) in ((f'og-{SLUG}-{n}-{l}.jpg', (1200, 630)), (f'thumb-{SLUG}-{n}-{l}.jpg', (480, 270))):
            bg = im.resize((W, round(W * im.height / im.width)), Image.LANCZOS)
            y = (bg.height - H) // 2
            bg = ImageEnhance.Brightness(bg.crop((0, y, W, y + H)).filter(ImageFilter.GaussianBlur(H / 22))).enhance(0.45)
            fg = im.resize((round(H * im.width / im.height), H), Image.LANCZOS)
            bg.paste(fg, ((W - fg.width) // 2, 0)); bg.save(D + stem, 'JPEG', quality=82, progressive=True, optimize=True)


def build():
    import build_mourning as M
    CAT = json.load(open(HERE + 'catalog.json'))
    TP = {l: template(l) for l in LANGS4}
    keep = ROOT + f'images/{SLUG}.jpg'
    if os.path.exists(PIC): Image.open(PIC).save(keep, quality=90)
    im = Image.open(keep).convert('RGB')
    arts = {}
    for n, posts in POSTS.items():
        n = int(n)
        pictures(n, im)
        for l in LANGS4:
            heading, blocks, sources = parse(posts[l]['text'])
            first = ' '.join(' '.join(t) for k, t in blocks if k == 'p')[:400]
            date = posts[l]['date'][:10]
            arts[(l, n)] = dict(lang=l, title=heading, desc=BA.clip(re.sub(r'\s+', ' ', first), 160), published=date, modified=date,
                                heads=[{'t': 'p', 'x': S[l]['part'].format(n=num(n, l))}], hero_video=None,
                                body=[{'t': 'p', 'x': t if isinstance(t, str) else ' '.join(t)} for k, t in blocks],
                                tags=[], og='x', img=dict(w=im.width, h=im.height, orig=im.size), blocks=blocks, sources=sources)
    nums = sorted({n for (_, n) in arts})
    for (l, n), a in arts.items():
        href = lambda k=None, lg=l: f"{PFX[lg]}/articles/{SLUG}/" + (f'{k}/' if k else '')
        sr = dict(name=NAME[l], href=href(), n=n)
        if (l, n - 1) in arts: sr['prev'] = (href(n - 1), arts[(l, n - 1)]['title'])
        if (l, n + 1) in arts: sr['next'] = (href(n + 1), arts[(l, n + 1)]['title'])
        BA.page(f'{SLUG}/{n}', l, a, LANGS4, TP, series=sr)
        CAT[f'{SLUG}/{n}'] = dict(slug=f'{SLUG}/{n}', series=SLUG, month=MONTH, langs=LANGS4, titles={ll: arts[(ll, n)]['title'] for ll in LANGS4},
                                  tags=[], tags_l={ll: [] for ll in LANGS4}, published=max(arts[(ll, n)]['published'] for ll in LANGS4), img=True,
                                  descs={ll: arts[(ll, n)]['desc'] for ll in LANGS4})
    M.SER, M.NAME, M.series_desc, M.TP = SLUG, NAME, (lambda lang: SERIES_DESC[lang]), TP
    for l in LANGS4:
        M.series_page(l, {(l, n): arts[(l, n)] for n in nums}, LANGS4)
    CAT[SLUG] = dict(slug=SLUG, kind='series', month=MONTH, langs=LANGS4, titles=NAME, tags=[], tags_l={},
                     published=max(a['published'] for a in arts.values()), img=True, descs=SERIES_DESC)
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    print('built', len(arts))


if __name__ == '__main__':
    if '--dry' in sys.argv:
        for n, posts in POSTS.items():
            for l in LANGS4:
                h, blocks, sources = parse(posts[l]['text'])
                print(n, l, repr(h[:40]), ''.join(k for k, _ in blocks), [s[0] for s in sources])
    else: build()
