import re, json, html, sys, os, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse import parse

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
SP = HERE + 'work/'
KW = SP + 'kw/'
ROOT = os.path.abspath(HERE + '../../') + '/'
SITE = 'https://article.misbah-inc.com'
LANGS = ['en', 'ar', 'fa', 'ur']
PFX = {'en': '', 'ar': '/ar', 'fa': '/fa', 'ur': '/ur'}
VIDEO = {('en', 1): '2YZn6Gq7ULs', ('fa', 1): 'mOcejB8zlps', ('ur', 1): 'QVezA6ZIeT0', ('ar', 1): 'DyrUBNLp3B8',
         ('en', 2): '9BZatISuH0w', ('fa', 2): 'UZ37Yly9Vhk', ('ur', 2): '_ASmFk6Q4f8', ('ar', 2): 'PGNH5oFbmn8'}
SLUG = 'al-kawthar'

S = {
 'en': dict(brand='Misbah Inc.', home='Home', articles='Articles', all='All Articles', series='The Series of Al-Kawthar',
            series_short='Al-Kawthar Series', chip='Series', tag='Series', read_in='Read in', read_in_aria='Read this article in another language',
            watch='Watch the video', play='Play video', sources='Sources', prev='Previous part', next='Next part',
            read='Read', view_series='View the series', parts='Parts', min='~{n} min read', part='Part {n}',
            crumb_aria='Breadcrumb', new_series='New series', more_in='More in this series', og_locale='en_US',
            video_open='Watch on YouTube', digits='0123456789'),
 'ar': dict(brand='مؤسسة مصباح', home='الرئيسية', articles='المقالات', all='جميع المقالات', series='سلسلة مباحث الكوثر',
            series_short='سلسلة مباحث الكوثر', chip='سلسلة', tag='سلسلة', read_in='اقرأ بـ', read_in_aria='اقرأ هذه المقالة بلغة أخرى',
            watch='شاهد الفيديو', play='تشغيل الفيديو', sources='المصادر', prev='القسم السابق', next='القسم التالي',
            read='اقرأ', view_series='عرض السلسلة', parts='الأقسام', min='~{n} دقيقة قراءة', part='القسم {n}',
            crumb_aria='مسار التنقل', new_series='سلسلة جديدة', more_in='المزيد من هذه السلسلة', og_locale='ar_AR',
            video_open='شاهد على يوتيوب', digits='٠١٢٣٤٥٦٧٨٩'),
 'fa': dict(brand='مصباح انک.', home='صفحه اصلی', articles='مقالات', all='همه مقالات', series='سلسله مباحث کوثر',
            series_short='سلسله مباحث کوثر', chip='سلسله', tag='سلسله', read_in='بخوانید به', read_in_aria='این مقاله را به زبان دیگری بخوانید',
            watch='تماشای ویدیو', play='پخش ویدیو', sources='منابع', prev='بخش قبلی', next='بخش بعدی',
            read='بخوانید', view_series='مشاهده سلسله', parts='بخش‌ها', min='~{n} دقیقه مطالعه', part='بخش {n}',
            crumb_aria='مسیر ناوبری', new_series='سلسله جدید', more_in='بیشتر از این سلسله', og_locale='fa_IR',
            video_open='تماشا در یوتیوب', digits='۰۱۲۳۴۵۶۷۸۹'),
 'ur': dict(brand='مصباح انک.', home='صفحہ اول', articles='مضامین', all='تمام مضامین', series='سلسلۂ مباحثِ کوثر',
            series_short='سلسلۂ مباحثِ کوثر', chip='سلسلہ', tag='سلسلہ', read_in='پڑھیں', read_in_aria='یہ مضمون دوسری زبان میں پڑھیں',
            watch='ویڈیو دیکھیں', play='ویڈیو چلائیں', sources='مآخذ', prev='گزشتہ حصہ', next='اگلا حصہ',
            read='پڑھیں', view_series='سلسلہ دیکھیں', parts='حصے', min='~{n} منٹ مطالعہ', part='حصہ {n}',
            crumb_aria='نیویگیشن راستہ', new_series='نیا سلسلہ', more_in='اس سلسلے کے مزید حصے', og_locale='ur_PK',
            video_open='یوٹیوب پر دیکھیں', digits='۰۱۲۳۴۵۶۷۸۹'),
}
ENDASH = ' — '
WIX_TAGS = {'Latest', 'تازه ها', 'الأحدث', 'تازه‌ها'}


def esc(s):
    return html.escape(s, quote=False)


def num(n, lang):
    return ''.join(S[lang]['digits'][int(c)] for c in str(n))


def tashkeel_ratio(t):
    letters = len(re.findall(r'[ء-يٱ-ۓ]', t))
    marks = len(re.findall(r'[ً-ْٰ]', t))
    alpha = len(re.findall(r'[A-Za-zء-يٱ-ۓپچژگکی]', t))
    return (marks / letters if letters else 0, letters / alpha if alpha else 0)


PERSIANISH = re.compile(r'[\u067E\u0686\u0698\u06AF\u06A9\u06CC\u0679\u0688\u0691\u06BA\u06C1\u06BE\u06D2\u06F0-\u06F9]')


def is_arabic_quote(t):
    """Arabic verse/hadith line: diacritised, and free of the letters only Persian/Urdu use."""
    if len(t) > 420 or PERSIANISH.search(t):
        return False
    tr, ar = tashkeel_ratio(re.sub(r'[^\w\s\u064B-\u0652\u0670]', ' ', t))
    return ar > 0.85 and tr >= 0.30


# ── feed descriptions (verbatim from the published posts) ────────────────
def feed_desc():
    s = open(SP + 'feed.xml', encoding='utf-8').read()
    out = {}
    for it in re.findall(r'<item>.*?</item>', s, re.S):
        link = urllib.parse.unquote(re.search(r'<link>(.*?)</link>', it).group(1))
        d = re.search(r'<description><!\[CDATA\[(.*?)\]\]>', it, re.S).group(1).strip()
        m = re.search(r'misbah-inc\.com/(ar|fa|ur)/', link)
        lang = m.group(1) if m else 'en'
        if not re.search(r'kawthar|کوثر|الكوثر', link, re.I):
            continue
        part = 2 if re.search(r'part-2|دوم|الثاني', link) else 1
        out[(lang, part)] = d
    return out


def feed_titles():
    s = open(SP + 'feed.xml', encoding='utf-8').read()
    out = {}
    for it in re.findall(r'<item>.*?</item>', s, re.S):
        link = urllib.parse.unquote(re.search(r'<link>(.*?)</link>', it).group(1))
        t = re.search(r'<title><!\[CDATA\[(.*?)\]\]>', it, re.S).group(1).strip()
        m = re.search(r'misbah-inc\.com/(ar|fa|ur)/', link)
        lang = m.group(1) if m else 'en'
        if not re.search(r'kawthar|کوثر|الكوثر', link, re.I):
            continue
        out[(lang, 2 if re.search(r'part-2|دوم|الثاني', link) else 1)] = t
    return out


# ── article model ────────────────────────────────────────────────────────
def load(lang, part):
    f = f'{KW}{lang}{part}.html'
    raw = open(f, encoding='utf-8').read()
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S).group(1))
    blocks = parse(f)
    # tags: trailing list-ul + li
    tags = []
    i = len(blocks)
    while i > 0 and blocks[i - 1]['t'] == 'li':
        i -= 1
    tags = [b['x'] for b in blocks[i:] if b['x'] not in WIX_TAGS]
    blocks = blocks[:i]
    while blocks and blocks[-1]['t'].startswith('list'):
        blocks.pop()
    # head: leading headings
    k = 0
    while k < len(blocks) and blocks[k]['t'].startswith('h'):
        k += 1
    heads = [b['x'] for b in blocks[:k]]
    body = blocks[k:]
    # sources
    src_i = None
    for n, b in enumerate(body):
        if re.match(r'^(📚\s*)?Sources:?$', b['x']) or re.match(r'^ـ+\s*(المصادر|منابع|مآخذ)\s*ـ+$', b['x']):
            src_i = n
    if src_i is None:
        src_i = len(body) - 2  # part 2 in ar/fa/ur: last two paragraphs are the references, no heading
    sources = [b['x'] for b in body[src_i + 1:] if not b['t'].startswith('list')] if re.match(r'^(📚\s*)?Sources:?$|^ـ', body[src_i]['x']) else [b['x'] for b in body[src_i:]]
    body = body[:src_i]
    title = heads[0] if heads else ''
    return dict(lang=lang, part=part, title=title, heads=heads, body=[b for b in body if not b['t'].startswith('list')],
                sources=sources, tags=tags, published=ld['datePublished'][:10], raw_ld=ld)


def para_html(t):
    return '<p>' + esc(t).replace('\n', '<br>') + '</p>'


def body_html(a):
    out = []

    def one(t, tag):
        if re.fullmatch(r'[✦❖━─\s]+', t):
            out.append('<div class="art-divider">' + esc(t) + '</div>')
        elif tag.startswith('h'):
            out.append(f'<h3 class="art-section-title">{esc(t)}</h3>')
        elif is_arabic_quote(t):
            out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{esc(t)}</span></div>')
        else:
            out.append(para_html(t))

    for b in a['body']:
        lines = [x.strip() for x in b['x'].split('\n') if x.strip()]
        if len(lines) > 1 and any(is_arabic_quote(x) for x in lines):
            for x in lines:  # an Arabic line and its translation share one Wix block: keep both, in order
                one(x, b['t'])
        else:
            one(b['x'], b['t'])
    return '\n        '.join(out)


def lead_heads_html(a):
    out = []
    for t in a['heads'][1:]:
        if re.search(r'بسم', t):
            out.append(f'<p class="kw-bismillah" lang="ar" dir="rtl">{esc(t)}</p>')
        elif is_arabic_quote(t) or re.fullmatch(r'«.*»', t):
            out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{esc(t)}</span></div>')
        else:
            out.append(f'<p class="kw-subhead">{esc(t)}</p>')
    return ''.join(out)


def sources_html(a, lang):
    items = a['sources']
    numbered = all(re.match(r'^[\d٠-٩۰-۹]+\s*[.۔\-]', x) for x in items)
    if numbered or lang != 'en' and False:
        lis = ''.join(f'<li>{esc(x)}</li>' for x in items)
        lst = f'<ul class="kw-sources-list">{lis}</ul>'
    elif len(items) == 1 or not all(len(x) < 140 for x in items):
        lis = ''.join(f'<li>{esc(x)}</li>' for x in items)
        lst = f'<ul class="kw-sources-list">{lis}</ul>'
    else:
        lis = ''.join(f'<li>{esc(x)}</li>' for x in items)
        lst = f'<ol>{lis}</ol>'
    n = num(len(items), lang)
    return f'''<div class="art-sources">
      <button class="art-sources-btn open" id="src-toggle" aria-expanded="true" aria-controls="src-body">
        <span>{S[lang]['sources']} ({n})</span>
        <span class="art-sources-chevron">▼</span>
      </button>
      <div class="art-sources-body open" id="src-body" role="region">
        {lst}
      </div>
    </div>'''


def video_html(a, lang, vid):
    L = S[lang]
    title = esc(a['title'])
    return f'''<div class="kw-video" id="video">
      <span class="kw-video-label">{L['watch']}</span>
      <div class="kw-video-frame" data-video="{vid}">
        <button type="button" aria-label="{L['play']}: {html.escape(a['title'], quote=True)}" style="background-image:url('https://i.ytimg.com/vi/{vid}/hqdefault.jpg')">
          <span class="kw-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
        </button>
      </div>
      <noscript><p><a href="https://www.youtube.com/watch?v={vid}" rel="noopener">{L['video_open']}</a></p></noscript>
    </div>'''


VIDEO_JS = '''<script>
  /* Sources accordion */
  (function () {
    var btn = document.getElementById('src-toggle'), body = document.getElementById('src-body');
    if (btn && body) btn.addEventListener('click', function () {
      var open = body.classList.toggle('open'); btn.classList.toggle('open', open); btn.setAttribute('aria-expanded', open);
    });
  })();
  /* Click-to-load video: no request goes to YouTube until the reader asks for it. */
  document.querySelectorAll('.kw-video-frame').forEach(function (f) {
    var b = f.querySelector('button');
    if (!b) return;
    b.addEventListener('click', function () {
      var i = document.createElement('iframe');
      i.src = 'https://www.youtube-nocookie.com/embed/' + f.dataset.video + '?autoplay=1&rel=0&playsinline=1';
      i.title = b.getAttribute('aria-label'); i.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      i.allowFullscreen = true; f.replaceChild(i, b); i.focus();
    });
  });
</script>'''

# ── template pieces from each language's Khadijah page ───────────────────
def template(lang):
    t = open(ROOT + PFX[lang].lstrip('/') + ('/' if PFX[lang] else '') + 'articles/rabi_al_awwal/index.html', encoding='utf-8').read()
    t = re.sub(r'(?:\.\./)+(assets|images)/', r'/\1/', t)
    style = re.search(r'  <style>.*?</style>\n', t, re.S).group(0)
    header = re.search(r'<header class="site-header">.*?</header>', t, re.S).group(0)
    footer = re.search(r'<!--[^>]*FOOTER[^>]*-->\s*<footer.*?</footer>|<footer.*?</footer>', t, re.S).group(0)
    fonts = re.search(r'  <link rel="preconnect" href="https://fonts\.googleapis\.com">.*?rel="stylesheet">\n', t, re.S).group(0)
    return dict(style=style, header=header, footer=footer, fonts=fonts)


def url(lang, *parts):
    return SITE + PFX[lang] + '/articles/' + SLUG + '/' + ''.join(p + '/' for p in parts)


def hreflangs(*parts):
    lines = [f'  <link rel="alternate"  hreflang="{l}" href="{url(l, *parts)}">' for l in LANGS]
    lines.append(f'  <link rel="alternate"  hreflang="x-default" href="{url("en", *parts)}">')
    return '\n'.join(lines)


def lang_switch(lang, *parts):
    names = {'en': 'English', 'ar': 'العربية', 'fa': 'فارسی', 'ur': 'اردو'}
    L = S[lang]
    tail = ''.join(p + '/' for p in parts)
    links = ''
    for l in LANGS:
        cls = ' class="active"' if l == lang else ''
        links += f'\n      <a href="{PFX[l]}/articles/{SLUG}/{tail}" hreflang="{l}"{cls}>{names[l]}</a>'
    return f'''<div class="art-lang-sw-inline" aria-label="{L['read_in_aria']}">
      <span class="lsw-label">{L['read_in']}</span>{links}
    </div>'''


def head(lang, tp, *, title, desc, parts, og_img, og_type, published, ld, extra_meta=''):
    d = 'rtl' if lang != 'en' else 'ltr'
    jd = json.dumps(ld, ensure_ascii=False, indent=2)
    return f'''<!DOCTYPE html>
<html lang="{lang}" dir="{d}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{html.escape(desc, quote=True)}">

{tp['fonts']}
  <!-- Canonical + hreflang -->
  <link rel="canonical"  href="{url(lang, *parts)}">
{hreflangs(*parts)}

  <!-- Open Graph -->
  <meta property="og:type"        content="{og_type}">
  <meta property="og:url"         content="{url(lang, *parts)}">
  <meta property="og:site_name"   content="{S[lang]['brand']}">
  <meta property="og:title"       content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(desc, quote=True)}">
  <meta property="og:image"       content="{SITE}{og_img}">
  <meta property="og:image:width"  content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale"      content="{S[lang]['og_locale']}">
{extra_meta}
  <!-- Twitter Card -->
  <meta name="twitter:card"        content="summary_large_image">
  <meta name="twitter:title"       content="{html.escape(title, quote=True)}">
  <meta name="twitter:description" content="{html.escape(desc, quote=True)}">
  <meta name="twitter:image"       content="{SITE}{og_img}">

  <!-- Structured Data -->
  <script type="application/ld+json">
{jd}
  </script>

  <link rel="stylesheet" href="/assets/style.css">
{tp['style']}</head>
<body>

{tp['header']}

'''


def crumbs(lang, items):
    L = S[lang]
    sep = '›' if lang == 'en' else '‹'
    parts = [f'<a href="{PFX[lang] or "/"}{"/" if PFX[lang] else ""}">{L["home"]}</a>', f'<a href="{PFX[lang]}/articles/">{L["articles"]}</a>']
    for name, href in items:
        parts.append(f'<a href="{href}">{esc(name)}</a>' if href else f'<span>{esc(name)}</span>')
    inner = f'\n    <span>{sep}</span>\n    '.join(parts)
    return f'''<nav class="art-breadcrumb" aria-label="{L['crumb_aria']}">
  <div class="art-breadcrumb-inner">
    {inner}
  </div>
</nav>'''


def banner(lang, part, alt, eager=True):
    return f'''<div class="kw-banner-wrap">
  <div class="kw-banner">
    <img src="/images/kawthar/part{part}-{lang}.jpg" alt="{html.escape(alt, quote=True)}" width="1400" height="{483 if part == 1 else 467}"{' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'}>
  </div>
</div>'''


def breadcrumb_ld(lang, items):
    L = S[lang]
    lst = [{"@type": "ListItem", "position": 1, "name": L['home'], "item": SITE + (PFX[lang] or '') + '/'},
           {"@type": "ListItem", "position": 2, "name": L['articles'], "item": SITE + '/articles/'}]
    for n, (name, href) in enumerate(items, 3):
        e = {"@type": "ListItem", "position": n, "name": name}
        if href:
            e["item"] = SITE + href
        lst.append(e)
    return {"@type": "BreadcrumbList", "itemListElement": lst}


ORG = {"@type": "Organization", "@id": SITE + "/#organization", "name": "Misbah Inc.", "url": SITE + "/"}
