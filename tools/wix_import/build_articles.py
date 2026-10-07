"""Import single Wix posts (any number of languages) as /articles/<slug>/ pages. Text is copied verbatim."""
import re, json, html, os, sys, subprocess, urllib.parse
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_kawthar as G
from gen_kawthar import S, PFX, LANGS, ROOT, SITE, esc, num, is_arabic_quote, head, crumbs, breadcrumb_ld, ORG, template, VIDEO_JS, hreflangs

SP = G.SP


def clip(t, n=155):
    t = re.sub(r'\s+', ' ', t).strip()
    if len(t) <= n: return t
    return t[:n].rsplit(' ', 1)[0].rstrip('،,.;:') + '…'
DROP_TAGS = {'latest', 'previous', 'youtube blogs', 'Latest', 'Previous', 'YouTube Blogs', 'تازه ها', 'الأحدث', 'السابق'}


class P2(HTMLParser):
    """Wix post -> ordered blocks: h*, p, li (body list), video(id), img(url), tag (footer list)."""
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.blocks = []; s.cur = None; s.inart = False; s.foot = False; s.seen_title = False; s.lidepth = 0

    def handle_starttag(s, tag, a):
        a = dict(a)
        if tag == 'article': s.inart = True
        if not s.inart: return
        if tag == 'footer': s.foot = True
        st = a.get('style', '')
        m = re.search(r'i\.ytimg\.com/vi/([\w-]{11})', st)
        if m and not s.foot: s.blocks.append({'t': 'video', 'x': m.group(1)})
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'blockquote'):
            s.cur = {'t': tag, 'x': '', 'foot': s.foot}
            if tag.startswith('h'): s.seen_title = True
        if tag == 'img' and a.get('src') and s.seen_title and not s.foot and 'wixstatic.com/media' in a['src']:
            s.blocks.append({'t': 'img', 'x': a['src'], 'alt': a.get('alt', '')})
        if tag == 'br' and s.cur is not None: s.cur['x'] += '\n'

    def handle_endtag(s, tag):
        if tag == 'article': s.inart = False
        if s.cur and tag == s.cur['t']:
            s.cur['x'] = re.sub(r'[ \t]+', ' ', s.cur['x']).strip()
            if s.cur['x']: s.blocks.append(s.cur)
            s.cur = None

    def handle_data(s, d):
        if s.inart and s.cur is not None: s.cur['x'] += d


def load_post(path):
    raw = open(path, encoding='utf-8', errors='replace').read()
    assert 'Checking Your Request' not in raw[:5000], path
    ld = None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            d = json.loads(m.group(1))
            if isinstance(d, dict) and d.get('@type') == 'BlogPosting': ld = d; break
        except Exception: pass
    p = P2(); p.feed(raw)
    og = re.search(r'property="og:image" content="([^"]+)"', raw)
    blocks = p.blocks
    hero_video = None
    tags = [b['x'] for b in blocks if b['t'] == 'li' and b['foot'] and b['x'] not in DROP_TAGS]
    blocks = [b for b in blocks if not (b['t'] == 'li' and b['foot'])]
    # Wix puts "Updated: Sep 27" (and sometimes the video) above the title; neither belongs to the text.
    while blocks and (re.match(r'^(Updated|تم التحديث|به‌روزرسانی|تازہ کاری)\b.*', blocks[0]['x']) and len(blocks[0]['x']) < 40 and blocks[0]['t'] == 'p'
                      or blocks[0]['t'] == 'video'):
        if blocks[0]['t'] == 'video': hero_video = blocks[0]['x']
        blocks = blocks[1:]
    k = 0
    while k < len(blocks) and blocks[k]['t'].startswith('h'): k += 1
    heads = blocks[:k]
    ttl = html.unescape(ld['headline']).strip() if ld else ''
    if heads and heads[0]['t'] in ('h1', 'h2') and (ttl[:20] in heads[0]['x'] or heads[0]['x'][:20] in ttl):
        heads = heads[1:]          # the in-body title repeats the page title
        # a second h2 right after is a subtitle: keep it as a lead line
    return dict(title=html.unescape(ld['headline']).strip() if ld else blocks[0]['x'],
                desc=html.unescape(ld.get('description', '')).strip() if ld else '',
                published=(ld or {}).get('datePublished', '')[:10], modified=(ld or {}).get('dateModified', '')[:10],
                heads=heads, hero_video=hero_video, body=blocks[k:], tags=tags, og=og.group(1).split('/v1/')[0] if og else None, raw=raw)


def body_html(a):
    out = []
    lst = []

    def flush():
        if lst:
            out.append('<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in lst) + '</ul>'); lst.clear()

    def one(t, tag):
        if re.fullmatch(r'[✦❖━─\s]+', t):
            out.append('<div class="art-divider">' + esc(t) + '</div>')
        elif tag.startswith('h'):
            out.append(f'<h3 class="art-section-title">{esc(t)}</h3>')
        elif is_arabic_quote(t):
            out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{esc(t)}</span></div>')
        else:
            out.append('<p>' + esc(t).replace('\n', '<br>') + '</p>')

    for b in a['body']:
        t = b['t']
        if t == 'li':
            lst.append(b['x']); continue
        flush()
        if t == 'video':
            out.append(('VIDEO', b['x']))
        elif t == 'img':
            out.append(('IMG', b))
        else:
            lines = [x.strip() for x in b['x'].split('\n') if x.strip()]
            if len(lines) > 1 and any(is_arabic_quote(x) for x in lines):
                for x in lines: one(x, t)
            else:
                one(b['x'], t)
    flush()
    return out


def lead_html(a):
    out = []
    for b in a['heads']:
        t = b['x']
        if re.search(r'بسم', t): out.append(f'<p class="kw-bismillah" lang="ar" dir="rtl">{esc(t)}</p>')
        elif is_arabic_quote(t): out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{esc(t)}</span></div>')
        else: out.append(f'<p class="kw-subhead">{esc(t)}</p>')
    return ''.join(out)


def video_block(lang, vid, title):
    L = S[lang]
    return f'''<div class="kw-video">
      <span class="kw-video-label">{L['watch']}</span>
      <div class="kw-video-frame" data-video="{vid}">
        <button type="button" aria-label="{L['play']}: {html.escape(title, quote=True)}" style="background-image:url('https://i.ytimg.com/vi/{vid}/hqdefault.jpg')">
          <span class="kw-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
        </button>
      </div>
      <noscript><p><a href="https://www.youtube.com/watch?v={vid}" rel="noopener">{L['video_open']}</a></p></noscript>
    </div>'''


def make_image(a, slug, lang):
    """Download the post's cover, write images/articles/<slug>-<lang>.jpg (<=1400w) and a 1200x630 social crop."""
    from PIL import Image
    if not a['og']: return None
    d = ROOT + 'images/articles/'; os.makedirs(d, exist_ok=True)
    tmp = SP + f'img_{slug}_{lang}.bin'
    if not os.path.exists(tmp):
        subprocess.run(['curl', '-sL', '-A', 'Mozilla/5.0', '-o', tmp, a['og']], timeout=120)
    try:
        im = Image.open(tmp).convert('RGB')
    except Exception:
        return None
    w, h = im.size
    big = im if w <= 1400 else im.resize((1400, round(1400 * h / w)), Image.LANCZOS)
    big.save(f'{d}{slug}-{lang}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    s = max(1200 / w, 630 / h); r = im.resize((max(1200, round(w * s)), max(630, round(h * s))), Image.LANCZOS)
    x = (r.width - 1200) // 2; y = (r.height - 630) // 2
    r.crop((x, y, x + 1200, y + 630)).save(f'{d}og-{slug}-{lang}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    return dict(w=big.size[0], h=big.size[1], orig=(w, h))


def localize_img(url, slug, n):
    """Copy an image used inside an article off Wix's CDN: images/articles/<slug>/<n>.jpg (<=1200 w). Returns (path, w, h) or None."""
    from PIL import Image
    base = url.split('/v1/')[0]
    tmp = SP + f'body_{slug}_{n}.bin'
    if not os.path.exists(tmp):
        subprocess.run(['curl', '-sL', '-A', 'Mozilla/5.0', '-o', tmp, base], timeout=120)
    try:
        im = Image.open(tmp).convert('RGB')
    except Exception:
        return None
    w, h = im.size
    if w > 1200: im = im.resize((1200, round(1200 * h / w)), Image.LANCZOS)
    d = ROOT + f'images/articles/{slug}/'; os.makedirs(d, exist_ok=True)
    im.save(f'{d}{n}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    return f'/images/articles/{slug}/{n}.jpg', im.size[0], im.size[1]


def aurl(lang, slug):
    return f'{SITE}{PFX[lang]}/articles/{slug}/'


def page(slug, lang, a, langs_avail, TP, month_key=None, meta_title=None):
    L = S[lang]; tp = TP[lang]
    cur = aurl(lang, slug)
    words = len(' '.join(b['x'] for b in a['body'] if 'x' in b and isinstance(b['x'], str)).split())
    mins = max(1, round(words / 180))
    title_tag = f"{a['title'][:80]} | {L['brand']}"
    if len(title_tag) > 70: title_tag = f"{clip(a['title'], 56)} | {L['brand']}"
    desc = clip(a['desc'] or next((b['x'] for b in a['body'] if b['t'] == 'p' and len(b['x']) > 60), a['title']), 160)
    img = a.get('img')  # dict or None
    og_img = f'/images/articles/og-{slug}-{lang}.jpg' if img else '/images/articles/og-fallback.jpg'

    def alt_urls(lg): return aurl(lg, slug)
    hl = ''.join(f'  <link rel="alternate"  hreflang="{l}" href="{alt_urls(l)}">\n' for l in langs_avail)
    xdef = f'  <link rel="alternate"  hreflang="x-default" href="{alt_urls("en" if "en" in langs_avail else langs_avail[0])}">\n'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": cur + "#article", "headline": a['title'], "description": desc,
         "image": SITE + og_img, "url": cur, "inLanguage": lang, "datePublished": a['published'], "dateModified": a['modified'] or a['published'],
         "author": {"@id": SITE + "/#organization"}, "publisher": {"@id": SITE + "/#organization"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": cur}, "keywords": a['tags']},
        breadcrumb_ld(lang, [(a['title'], None)]), ORG]}
    vids = ([a['hero_video']] if a.get('hero_video') else []) + [b['x'] for b in a['body'] if b['t'] == 'video']
    if vids:
        ld['@graph'][0]['video'] = {"@type": "VideoObject", "name": a['title'], "description": desc,
                                    "thumbnailUrl": f"https://i.ytimg.com/vi/{vids[0]}/hqdefault.jpg", "uploadDate": a['published'],
                                    "embedUrl": f"https://www.youtube.com/embed/{vids[0]}", "inLanguage": lang}
    extra = (f'  <meta property="article:published_time" content="{a["published"]}T00:00:00+00:00">\n'
             f'  <meta property="article:author" content="Misbah Inc.">\n' +
             ''.join(f'  <meta property="article:tag" content="{html.escape(t, quote=True)}">\n' for t in a['tags']))
    h = head(lang, tp, title=title_tag, desc=desc, parts=(), og_img=og_img, og_type='article', published=a['published'], ld=ld, extra_meta=extra)
    # head() built canonical/hreflang for the kawthar slug; swap in this article's own
    h = re.sub(r'  <!-- Canonical \+ hreflang -->.*?(?=\n\n  <!-- Open Graph)',
               f'  <!-- Canonical + hreflang -->\n  <link rel="canonical"  href="{cur}">\n{hl}{xdef}'.rstrip('\n'), h, flags=re.S)
    h = h.replace(f'content="{SITE}{PFX[lang]}/articles/{G.SLUG}/"', f'content="{cur}"')
    # body
    parts = []
    nimg = 0
    for it in body_html(a):
        if isinstance(it, tuple):
            if it[0] == 'VIDEO': parts.append(video_block(lang, it[1], a['title']))
            else:
                nimg += 1
                loc = localize_img(it[1]['x'], slug, f'{lang}-{nimg}')
                if loc:
                    parts.append(f'<figure class="art-fig"><img src="{loc[0]}" alt="{html.escape(it[1].get("alt","") or a["title"], quote=True)}" width="{loc[1]}" height="{loc[2]}" loading="lazy" decoding="async"></figure>')
        else: parts.append(it)
    body = '\n        '.join(parts)
    banner = ''
    if img:
        ratio = img['w'] / img['h']
        cls = 'kw-banner' if ratio >= 1.4 else 'kw-banner kw-banner--tall'
        small = f' style="max-width:{img["w"]}px"' if img['w'] < 1000 else ''
        banner = f'''<div class="kw-banner-wrap">
  <div class="{cls}"{small}>
    <img src="/images/articles/{slug}-{lang}.jpg" alt="{html.escape(a['title'], quote=True)}" width="{img['w']}" height="{img['h']}" fetchpriority="high">
  </div>
</div>
'''
    names = {'en': 'English', 'ar': 'العربية', 'fa': 'فارسی', 'ur': 'اردو'}
    sw = ''
    if len(langs_avail) > 1:
        links = ''
        for l in langs_avail:
            cls = ' class="active"' if l == lang else ''
            links += f'\n      <a href="{PFX[l]}/articles/{slug}/" hreflang="{l}"{cls}>{names[l]}</a>'
        sw = f'''<div class="art-lang-sw-inline" aria-label="{L['read_in_aria']}">
      <span class="lsw-label">{L['read_in']}</span>{links}
    </div>'''
    tags = '<ul class="kw-tags">' + ''.join(f'<li>{esc(t)}</li>' for t in a['tags']) + '</ul>' if a['tags'] else ''
    back = '<path d="M5 12h14M12 5l7 7-7 7"/>' if lang != 'en' else '<path d="M19 12H5M12 5l-7 7 7 7"/>'
    main = f'''<main>

{banner}{crumbs(lang, [(a['title'], None)])}

<div class="art-page">
  <div class="art-container">

    <a href="{PFX[lang]}/articles/" class="art-back">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        {back}
      </svg>
      {L['all']}
    </a>

    <div class="art-meta">
      <span class="art-tag">{L['article']}</span>
      <span class="art-reading">{L['min'].format(n=num(mins, lang))}</span>
    </div>

    <div class="art-title-block">
      <h1 class="art-title">{esc(a['title'])}</h1>
    </div>

    {sw}

    <div class="kw-lead-headings">{lead_html(a)}</div>

    {video_block(lang, a['hero_video'], a['title']) if a.get('hero_video') else ''}

    <section class="art-part">
      <div class="art-body">

        {body}

      </div>
    </section>

    <div class="art-divider">❖ &nbsp; ❖ &nbsp; ❖</div>

    {tags}

  </div>
</div>

</main>

'''
    tail = f'''
{tp['footer']}

<script src="/assets/theme.js"></script>
<script src="/assets/script.js"></script>
{VIDEO_JS}
</body>
</html>
'''
    path = f'{PFX[lang].lstrip("/")}{"/" if PFX[lang] else ""}articles/{slug}/index.html'
    full = ROOT + path
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(h + main + tail)
    return path
