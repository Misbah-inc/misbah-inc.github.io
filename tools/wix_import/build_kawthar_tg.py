"""Kawthar of the Qur'an — the weekly Telegram episodes after Part 2 (Parts 3, 4, 5 so far), appended to the existing al-kawthar series.

Parts 1–2 were built earlier from the Wix import (build_kawthar.py) and are left alone, except that Part 2 gets a "next" link and the series
page gets the new cards. Source: the channels' posts (work/tg/kawthar-new.json; Part 3 English also has its Resources message merged),
text word for word; removed: hashtags, ✦━✦ dividers, the @channel footer and the emoji that open each paragraph. Each post's own portrait picture is the
banner (the channels' preview is 450×800, enlarged). Arabic text lines are quotation boxes with their translation under them; everything after
"Resources:" / "Sources:" is the collapsible Sources list. Part 4 has no ... Urdu Part 5 does not exist yet (the page set follows the posts).
usage: python3 build_kawthar_tg.py
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
from PIL import Image, ImageFilter, ImageEnhance

LANGS4 = ['en', 'ar', 'fa', 'ur']
SER = 'al-kawthar'
D = ROOT + 'images/articles/'
P = json.load(open(HERE + 'work/tg/kawthar-new.json', encoding='utf-8'))
ORD = {'en': {3: 'Part 3', 4: 'Part 4', 5: 'Part 5'}, 'ar': {3: 'القسم الثالث', 4: 'القسم الرابع', 5: 'القسم الخامس'},
       'fa': {3: 'بخش سوم', 4: 'بخش چهارم', 5: 'بخش پنجم'}, 'ur': {3: 'حصہ سوم', 4: 'حصہ چہارم', 5: 'حصہ پنجم'}}
UI = {'en': 'Sources', 'ar': 'المصادر', 'fa': 'منابع', 'ur': 'حوالہ جات'}
DIV = re.compile(r'^[\s━▪️🥀➖─\-–—_•·✦❁🌸]*$')
EMO = '🌸📖🖋💡📜✨🍏🌿🔹🏰❤️👑🕊📚💫🌹🔸▪️⚜️🔲'
FATIMA = re.compile(r'Lady Fatima al-Zahra|السيدة فاطمة الزهراء|حضرت فاطمه زهرا|حضرت فاطمہ زہرا|فاطمة الزهراء|Fatima al-Zahra')
PARTLINE = re.compile(r'^(Part|الجزء|القسم|بخش|قسمت|حصہ|حصه)\s*[\d٠-٩۰-۹]*\s*(الأول|الثاني|الثالث|الرابع|الخامس|اول|دوم|سوم|چهارم|چہارم|پنجم)?$')
ZAHRA = re.compile(r'الزهراء|الزَّهْرَاء|زهرا|زہرا|Zahra'); RIDA = re.compile(r'الرضا|رضا|Ridha|Rida')
ARL = re.compile(r'[ء-يٮ-ە]'); LAT = re.compile(r'[A-Za-z]')
ESC = lambda t: html.escape(t, quote=False)


def arabic(t): return len(ARL.findall(t)) >= 6 and len(LAT.findall(t)) < 3


def parse(text, lang):
    title, blocks, sources, in_src = '', [], [], False
    ls = text.split('\n'); cut = None                      # a mid-text "@channel" line followed by more text: what follows is the sources
    for i, l in enumerate(ls):
        if l.strip().startswith('@') and any(x.strip() and not x.strip().startswith('@') for x in ls[i + 1:]): cut = i; break
    mid_sources = []
    if cut is not None:
        mid_sources = [re.sub(r'^[📚•\s]+', '', x).strip() for x in ls[cut + 1:] if x.strip() and not x.strip().startswith(('@', '#')) and not DIV.match(x.strip()) and not re.match(r'^[📚\s]*(Resources|Sources|المصادر|مصادر|منابع|مآخذ|حوالہ جات)\s*:?\s*$', x.strip())]
        text = '\n'.join(ls[:cut])
    paras = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
    first = True
    for para in paras:
        lines = [l.strip() for l in para.split('\n') if l.strip() and not l.strip().startswith(('#', '@')) and not DIV.match(l.strip())]
        if not lines: continue
        if first:
            first = False
            rest = [re.sub(r'^[\s' + EMO + r']+|[\s🌸]+$', '', l) for l in lines]
            rest = [l for l in rest if l and not PARTLINE.match(l) and 'Kawthar of the Qur' not in l and 'کوثر القرآن' not in l and 'كَوْثَر' not in l[:12] and not (ZAHRA.search(l) and not RIDA.search(l))]
            if len(rest) >= 1 and lines and not any(x.startswith(('📖', '🖋')) for x in lines): title = ' '.join(rest)
            continue
        for l in lines:
            t = re.sub(r'^[\s' + EMO + r']+', '', l).strip()
            if re.match(r'^(Resources|Sources|المصادر|مصادر|منابع|مآخذ|حوالہ جات|حوالے)\s*:?\s*$', t): in_src = True; continue
            if in_src: sources.append(re.sub(r'^[•📚📗\s]+', '', t)); continue
            if not t: continue
            prev = blocks[-1][0] if blocks else ''
            if l.startswith('📜') and arabic(t.strip('«»')): blocks.append(('A', t.strip('«»').strip()))
            elif l.startswith('📜'): blocks.append(('Q' if prev == 'A' else 'P', t))
            elif prev == 'A' and lang != 'ar' and t[:1] in '“"«': blocks.append(('Q', t.strip('“”"«»')))
            else: blocks.append(('P', t))
    return title, blocks, (sources + mid_sources)


def body(a):
    out = []
    for k, t in a['blocks']:
        if k == 'A': out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{ESC(t)}</span></div>')
        elif k == 'Q': out.append(f'<blockquote class="art-quote">{ESC(t)}</blockquote>')
        else: out.append(f'<p>{ESC(t)}</p>')
    if a['sources']:
        lis = ''.join(f'<li>{ESC(t)}</li>' for t in a['sources'])
        out.append(f'<div class="bio-sources"><button type="button" class="bio-sources-btn" aria-expanded="false" aria-controls="bio-src-body"><span>{UI[a["lang"]]}</span><span class="bio-sources-chevron" aria-hidden="true">▾</span></button>'
                   f'<div class="bio-sources-body" id="bio-src-body"><div class="bio-src-group"><ul class="kw-sources-list">{lis}</ul></div></div></div>')
    return ['<div class="bio-ch">'] + out + ['</div>']


BA.body_html = body


def pictures(n, src):
    im = Image.open(src).convert('RGB').resize((720, 1280), Image.LANCZOS)
    for l in LANGS4:
        fs = f'{SER}-part-{n}-{l}'
        im.save(D + f'{fs}.jpg', 'JPEG', quality=82, progressive=True, optimize=True)
        for stem, (W, H) in ((f'og-{fs}.jpg', (1200, 630)), (f'thumb-{fs}.jpg', (480, 270))):
            bg = im.resize((W, round(W * im.height / im.width)), Image.LANCZOS)
            y = (bg.height - H) // 2
            bg = ImageEnhance.Brightness(bg.crop((0, y, W, y + H)).filter(ImageFilter.GaussianBlur(H / 22))).enhance(0.45)
            fg = im.resize((round(H * im.width / im.height), H), Image.LANCZOS)
            bg.paste(fg, ((W - fg.width) // 2, 0)); bg.save(D + stem, 'JPEG', quality=82, progressive=True, optimize=True)
    return im.size


def existing(lang, part):
    path = ROOT + f"{PFX[lang].lstrip('/')}{'/' if PFX[lang] else ''}articles/{SER}/part-{part}/index.html"
    s = open(path, encoding='utf-8').read()
    return path, s, html.unescape(re.search(r'<h1 class="art-title">(.*?)</h1>', s, re.S).group(1)).strip()


def build():
    CAT = json.load(open(HERE + 'catalog.json'))
    TP = {l: template(l) for l in LANGS4}
    arts = {}
    for n, posts in P.items():
        n = int(n)
        src = f'/private/tmp/claude-501/-Users-mohammad-Developer-misbah-app/9308e757-88c6-47b5-b1f7-fb7f616f0215/scratchpad/tgimg/kw{n}-en.jpg'
        keep = ROOT + f'images/kawthar-part-{n}.jpg'
        if os.path.exists(src): Image.open(src).save(keep, quality=90)
        size = pictures(n, keep)
        for l, p in posts.items():
            title, blocks, sources = parse(p['text'], l)
            heading = f"{S[l]['series']} — {ORD[l][n]}"
            first = ' '.join(t for k, t in blocks if k == 'P')[:400]
            arts[(l, n)] = dict(lang=l, title=heading, subtitle=title, desc=BA.clip(re.sub(r'\s+', ' ', first), 160), published=p['date'][:10], modified=p['date'][:10],
                                heads=[{'t': 'p', 'x': ORD[l][n]}], hero_video=None, body=[{'t': 'p', 'x': t} for k, t in blocks], tags=[], og='x',
                                img=dict(w=size[0], h=size[1], orig=size), blocks=([('H', title)] if title else []) + blocks, sources=sources)
    # fix: the sub-title block is a heading
    for a in arts.values():
        a['blocks'] = [(('P', t) if k == 'H' else (k, t)) for k, t in a['blocks']]
    avail = lambda n: [l for l in LANGS4 if (l, n) in arts]
    nums = sorted({n for (_, n) in arts})
    for (l, n), a in sorted(arts.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        href = lambda p, lg=l: f"{PFX[lg]}/articles/{SER}/part-{p}/"
        sr = dict(name=S[l]['series'], href=f"{PFX[l]}/articles/{SER}/", n=n)
        before = [k for k in nums if k < n and (l, k) in arts]; after = [k for k in nums if k > n and (l, k) in arts]
        sr['prev'] = (href(max(before)), arts[(l, max(before))]['title']) if before else (href(2), existing(l, 2)[2])
        if after: sr['next'] = (href(min(after)), arts[(l, min(after))]['title'])
        BA.page(f'{SER}/part-{n}', l, a, avail(n), TP, series=sr)
        CAT[f'{SER}/part-{n}'] = dict(CAT.get(f'{SER}/part-{n}', {'langs': []}), slug=f'{SER}/part-{n}', series=SER, month=0, langs=avail(n),
                                      titles={ll: arts[(ll, n)]['title'] for ll in avail(n)}, tags=[], tags_l={ll: [] for ll in avail(n)},
                                      published=max(arts[(ll, n)]['published'] for ll in avail(n)), img=True, descs={ll: arts[(ll, n)]['desc'] for ll in avail(n)})
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    patch_existing(arts, nums)
    print({n: avail(n) for n in nums})


def patch_existing(arts, nums):
    """Part 2 gets a 'next' link; the series page gets the new cards and structured data (idempotent)."""
    for l in LANGS4:
        L = S[l]
        path, s, _ = existing(l, 2)
        mine = [k for k in nums if (l, k) in arts]
        if mine and 'rel="next"' not in s:
            a = arts[(l, mine[0])]
            nxt = f'<a class="next" href="{PFX[l]}/articles/{SER}/part-{mine[0]}/" rel="next"><small>{L["next"]} {"←" if l != "en" else "→"}</small><strong>{ESC(a["title"])}</strong></a>'
            s = re.sub(r'(<nav class="kw-partnav"[^>]*>)(.*?)(</nav>)', lambda m: m.group(1) + m.group(2) + nxt + m.group(3), s, count=1, flags=re.S)
            open(path, 'w', encoding='utf-8').write(s)
        sp = ROOT + f"{PFX[l].lstrip('/')}{'/' if PFX[l] else ''}articles/{SER}/index.html"
        s = open(sp, encoding='utf-8').read()
        s = re.sub(r'\s*<a class="kw-part-card" href="[^"]*/part-[3-9]/">.*?</a>', '', s, flags=re.S)           # idempotent
        cards = ''
        for k in mine:
            a = arts[(l, k)]
            cards += f'''
    <a class="kw-part-card" href="{PFX[l]}/articles/{SER}/part-{k}/">
      <img src="/images/articles/thumb-{SER}-part-{k}-{l}.jpg" alt="{html.escape(a['title'], quote=True)}" width="480" height="270" loading="lazy" decoding="async">
      <div class="kw-part-body">
        <span class="kw-series-chip">{ORD[l][k]}</span>
        <h2>{ESC(a['subtitle'] or a['title'])}</h2>
        <p>{ESC(a['desc'])}</p>
        <span class="btn btn-gold">{L['read']}</span>
      </div>
    </a>'''
        i = s.rindex('</a>', 0, s.index('</main>'))
        s = s[:i + 4] + cards + s[i + 4:]
        m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
        ld = json.loads(m.group(2))
        for node in ld['@graph']:
            if node.get('@type') == 'CollectionPage':
                parts = [x for x in node['mainEntity']['hasPart'] if '/part-1/' in x['url'] or '/part-2/' in x['url']]
                parts += [{'@type': 'Article', 'name': arts[(l, k)]['title'], 'url': f"{SITE}{PFX[l]}/articles/{SER}/part-{k}/", 'datePublished': arts[(l, k)]['published']} for k in mine]
                node['mainEntity']['hasPart'] = parts; node['mainEntity']['numberOfItems'] = len(parts)
        s = s[:m.start(2)] + json.dumps(ld, ensure_ascii=False) + s[m.end(2):]
        open(sp, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    if '--dry' in sys.argv:
        for n, posts in P.items():
            for l, p in posts.items():
                title, blocks, sources = parse(p['text'], l)
                print(n, l, repr(title[:50]), ''.join(k for k, _ in blocks), len(sources))
    else: build()
