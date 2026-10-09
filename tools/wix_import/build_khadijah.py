"""Three Lady Khadijah series from the Misbah Telegram channels (fa @misbah110, en _en, ar _ar, ur _ur), four languages.

  lady-khadijah-poems     Poems of Lady Khadijah about the Prophet          (8 poems)
  lady-khadijah-biography Biography of Lady Khadijah al-Kubra               (4 weekly chapters)
  lady-khadijah-ziyarat   Explanation of the Ziyarat of Ummul Muminin       (4 Friday parts)

Text = the channel posts word for word (read from work/tg/scan-<lang>.json, made by tg_scan.py). Only Telegram furniture is removed:
hashtag header lines, ✦━✦ / ❁ dividers, the @channel footer, and the emoji used as bullets. A post that was split across two
messages (the second has no title) is joined to the first. Part N is the same part in every language.
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
import build_mourning as M
from PIL import Image, ImageOps

LANGS4 = ['en', 'ar', 'fa', 'ur']
MONTH = 4            # Rabi' al-Thani (the channel's own "Rabi al-Thani program"); change here to refile
NAMES = {
 'lady-khadijah-poems': {'en': 'The Poems of Lady Khadijah (p) About the Prophet (p)', 'ar': 'أشعار السيدة خديجة (ع) في النبي (ص)', 'fa': 'اشعار حضرت خدیجه (س) درباره‌ی پیامبر (ص)', 'ur': 'نبی اکرم (ص) کے بارے میں حضرت خدیجہ (س) کے اشعار'},
 'lady-khadijah-biography': {'en': 'The Biography of Lady Khadijah al-Kubra (p)', 'ar': 'سيرة السيدة خديجة الكبرى (ع)', 'fa': 'زندگی‌نامه‌ی حضرت خدیجه‌ی کبری (س)', 'ur': 'سوانحِ حیاتِ حضرت خدیجہ کبریٰ (س)'},
 'lady-khadijah-ziyarat': {'en': 'Explanation of the Ziyarat of Ummul Muminin (p)', 'ar': 'شرح زيارة السيدة أم المؤمنين (خديجة الكبرى، ع)', 'fa': 'شرح زیارت حضرت ام‌المؤمنین (س)', 'ur': 'شرحِ زیارتِ حضرت ام المومنین (س)'},
}
# main post ids, in order; part n = n-th item, the same part in every language
POSTS = {
 'lady-khadijah-poems': {'fa': [22600, 22618, 22660, 22683, 22714, 22772, 22819, 22883], 'en': [23357, 23374, 23416, 23440, 23477, 23536, 23585, 23667],
                         'ar': [153, 171, 212, 237, 267, 323, 366, 423], 'ur': [167, 185, 228, 251, 281, 345, 395, 459]},
 'lady-khadijah-biography': {'fa': [22731, 22790, 22838, 22894], 'en': [23493, 23552, 23605, 23681], 'ar': [283, 338, 383, 433], 'ur': [298, 361, 414, 469]},
 'lady-khadijah-ziyarat': {'fa': [22747, 22806, 22859, 22912], 'en': [23511, 23569, 23631, 23701], 'ar': [298, 351, 400, 449], 'ur': [314, 377, 432, 486]},
}
SERIES_TAGS = {'lady-khadijah-poems': ['lady-khadijah', 'holy-prophet'], 'lady-khadijah-biography': ['lady-khadijah'], 'lady-khadijah-ziyarat': ['lady-khadijah', 'ziyarat']}
SERIES_DESC = {
 'lady-khadijah-poems': {'en': 'Eight poems attributed to Lady Khadijah (p) in praise of the Holy Prophet (p), with their meaning, one each week.',
                         'ar': 'ثماني قصائد منسوبة إلى السيدة خديجة (ع) في مدح النبي الأكرم (ص)، مع معانيها.',
                         'fa': 'هشت شعر منسوب به حضرت خدیجه (س) در وصف پیامبر اکرم (ص)، همراه با معنا.',
                         'ur': 'حضرت خدیجہ (س) سے منسوب آٹھ اشعار نبی اکرم (ص) کی شان میں، مفہوم کے ساتھ۔'},
 'lady-khadijah-biography': {'en': 'The life of Lady Khadijah al-Kubra (p), chapter by chapter: her lineage, her family, her marriage to the Prophet (p) and her station.',
                             'ar': 'سيرة السيدة خديجة الكبرى (ع) فصلًا فصلًا: نسبها وأسرتها وزواجها من النبي (ص) ومقامها.',
                             'fa': 'زندگی‌نامه‌ی حضرت خدیجه‌ی کبری (س) فصل به فصل: نسب، خانواده، ازدواج با پیامبر (ص) و جایگاه ایشان.',
                             'ur': 'حضرت خدیجہ کبریٰ (س) کی سوانح حیات باب بہ باب: نسب، خاندان، نبی اکرم (ص) سے نکاح اور مقام۔'},
 'lady-khadijah-ziyarat': {'en': 'A weekly commentary on the Ziyarat of Lady Khadijah al-Kubra, Ummul Muminin (p), phrase by phrase.',
                           'ar': 'شرح أسبوعي لزيارة السيدة خديجة الكبرى أم المؤمنين (ع)، عبارةً عبارة.',
                           'fa': 'شرح هفتگی زیارت حضرت خدیجه‌ی کبری، ام‌المؤمنین (س)، عبارت به عبارت.',
                           'ur': 'حضرت خدیجہ کبریٰ ام المومنین (س) کی زیارت کی ہفتہ وار شرح، عبارت بہ عبارت۔'},
}
SHORT = {
 'lady-khadijah-poems': {'en': 'Poems of Lady Khadijah', 'ar': 'أشعار السيدة خديجة', 'fa': 'اشعار حضرت خدیجه', 'ur': 'اشعارِ حضرت خدیجہ'},
 'lady-khadijah-biography': {'en': 'Biography of Lady Khadijah', 'ar': 'سيرة السيدة خديجة', 'fa': 'زندگی‌نامه حضرت خدیجه', 'ur': 'سوانحِ حضرت خدیجہ'},
 'lady-khadijah-ziyarat': {'en': 'Ziyarat of Ummul Muminin', 'ar': 'زيارة أم المؤمنين', 'fa': 'زیارت ام‌المؤمنین', 'ur': 'زیارتِ ام المومنین'},
}
READ = {'en': 'Read', 'ar': 'اقرأ', 'fa': 'بخوانید', 'ur': 'پڑھیں'}
DIV = re.compile(r'^[\s✦━❁ا🌸─\-–—_•·]*$')
BULLETS = re.compile(r'^[\s🌳💫🌹✨⚜️▶️✳️●🔹🔸▪️◾️🖋🌸🕊📖🔗🔑🎭🔥✅❗️🤍🌙🔘📗📘📙📕🔷🔶❇️☑️⭐️🌟💎🌿🍃📌📍️]+')
SCAN = {l: {p['n']: p for p in json.load(open(HERE + f'work/tg/scan-{l}.json', encoding='utf-8'))} for l in LANGS4}
ARABIC = re.compile(r'[؀-ۿ]'); LATIN = re.compile(r'[A-Za-z]')


def is_tag_line(l): return bool(re.match(r'^(#\S+)(\s+#\S+)*(\s+[^#\s].*)?$', l)) and l.lstrip().startswith('#')


def clean_lines(text):
    out = []
    for l in text.split('\n'):
        s = l.strip()
        if s.startswith('@misbah'): continue
        out.append(s)
    return out


def continuation(lang, n):
    """The next message(s) that continue a split post: same day, text, no 🌸-title, hashtags (if any) only the usual header ones."""
    main = SCAN[lang][n]; res = []
    for k in range(n + 1, n + 5):
        p = SCAN[lang].get(k)
        if not p or not p['text'] or p['date'][:10] != main['date'][:10]: continue
        lines = [x for x in clean_lines(p['text']) if x and not is_tag_line(x) and not DIV.match(x)]
        if not lines or lines[0].startswith('🌸') or '🌸' in lines[0][:4]: break
        if re.search(r'#\S+', p['text']) and not set(re.findall(r'#\S+', p['text'])) <= set(re.findall(r'#\S+', main['text'])): break
        res.append(p)
        if len(res) == 1: break
    return res


def parse(texts):
    """texts: [main post text, continuation text...] -> dict(title, subs, blocks)"""
    title, subs, blocks = '', [], []
    for ti, text in enumerate(texts):
        lines = clean_lines(text)
        i = 0
        # header: hashtags, dividers, then 🌸 title 🌸 and its subtitle lines up to the next divider
        while i < len(lines) and (not lines[i] or is_tag_line(lines[i]) or DIV.match(lines[i])): i += 1
        if ti == 0 and i < len(lines) and '🌸' in lines[i]:
            title = BULLETS.sub('', lines[i]).replace('🌸', '').strip(); i += 1
            while i < len(lines) and lines[i] and not DIV.match(lines[i]):
                subs.append(re.sub(r'^[●•\s]+', '', lines[i]).strip()); i += 1
        refs = False; buf = []
        def flush():
            nonlocal buf
            if buf:
                t = ' '.join(buf).strip(); buf = []
                if t: blocks.append(('p', t))
        for l in lines[i:]:
            if DIV.match(l): flush(); refs = False; continue
            if not l: flush(); refs = False; continue
            if is_tag_line(l): continue
            if l.startswith(('📚', '📗', '📘', '📙', '📕')):
                flush(); refs = True; blocks.append(('ref', BULLETS.sub('', l[1:]).strip())); continue
            if refs:
                blocks.append(('ref', l)); continue
            raw = l; l = BULLETS.sub('', l).strip()
            if not l: continue
            if '║' in l:                                  # a verse: two Arabic hemistichs
                flush(); blocks.append(('verse', re.sub(r'\s*║\s*', '  ║  ', l))); continue
            ar, la = len(ARABIC.findall(l)), len(LATIN.findall(l))
            if l.startswith('❝') and ar > la * 2 or (ar > 8 and la == 0 and re.search(r'[ً-ْ]', l)):
                flush(); blocks.append(('ar', l)); continue
            buf.append(l); flush() if raw[:1] in '💫🌹✨⚜️▶️✳️🔹🌳●🖋' else None
        flush()
    return dict(title=title, subs=subs, blocks=blocks)


def h1_of(ser, d, lang, n):
    """Page heading from the post's own title lines (nothing is invented; a post with no title gets "<series> — Part N").
    The 🌸 title of a biography post is just the series name repeated, so there the chapter lines are the heading."""
    title, subs = d['title'], d['subs']
    if ser == 'lady-khadijah-biography':
        return ' — '.join(subs) if subs else title
    if ser == 'lady-khadijah-poems':
        label = title.split(' — ')[-1].strip() if ' — ' in title else title
        if len(label) > 60: label = ''                  # the long series-name title: the number is in the sub line
        return ' — '.join(x for x in [label, ' '.join(subs)] if x)
    # ziyarat
    if title: return f"{title} — {' '.join(subs)}" if subs else title
    return f"{NAMES[ser][lang]} — {S[lang]['part'].format(n=num(n, lang))}"


def rbody(a):
    out = []
    for k, t in a['blocks']:
        if k == 'ar': out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{esc(t)}</span></div>')
        elif k == 'verse': out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{esc(t)}</span></div>')
        elif k == 'ref': out.append(f'<p class="tg-ref">{esc(t)}</p>')
        else: out.append('<p>' + esc(t) + '</p>')
    return out


BA.body_html = rbody
SRC = ROOT + 'images/lady-khadijah-article.jpg'
D = ROOT + 'images/articles/'


def covers(ser, lang, bg):
    """One shared illustration for the series (no text on it: Arabic would need shaping); banner, og, thumb per series+language."""
    s = f'{ser}-cover-{lang}'
    im = Image.open(SRC).convert('RGB')
    ban = ImageOps.fit(im, (1200, 630), Image.LANCZOS, centering=(0.5, 0.4)); ban.save(D + f'{s}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    ban.save(D + f'og-{s}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    ban.resize((480, 270), Image.LANCZOS).save(D + f'thumb-{s}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)


def build(only=None):
    CAT = json.load(open(HERE + 'catalog.json'))
    TP = {l: template(l) for l in LANGS4}
    for ser in POSTS:
        if only and ser not in only: continue
        parsed = {}
        for lang in LANGS4:
            for n, pid in enumerate(POSTS[ser][lang], 1):
                main = SCAN[lang][pid]; cont = continuation(lang, pid)
                d = parse([main['text']] + [c['text'] for c in cont])
                d['date'] = main['date'][:10]; d['pid'] = pid; d['cont'] = [c['n'] for c in cont]
                parsed[(lang, n)] = d
        nparts = len(POSTS[ser]['en'])
        for lang in LANGS4: covers(ser, lang, None)
        arts = {}
        for (lang, n), d in parsed.items():
            h1 = h1_of(ser, d, lang, n)
            first = ''
            for kinds in (('p',), ('p', 'verse', 'ar')):
                for k, t in d['blocks']:
                    if k in kinds: first = (first + ' ' + t.replace('║', '')).strip()
                    if len(first) >= 100: break
                if len(first) >= 40: break
            desc = BA.clip(re.sub(r'\s+', ' ', first or h1), 160)
            if len(desc) < 40: desc = BA.clip(f'{h1}. {desc}', 160)
            a = dict(title=h1, desc=desc, published=d['date'], modified=d['date'], heads=[], hero_video=None, body=[{'t': 'p', 'x': t} for k, t in d['blocks']],
                     tags=[], og='x', img=dict(w=1200, h=630, orig=(1200, 630)), blocks=d['blocks'], n=n)
            arts[(lang, n)] = a
        for (lang, n), a in arts.items():
            name = NAMES[ser][lang]
            href = lambda k=None, l=lang: f"{PFX[l]}/articles/{ser}/" + (f'{k}/' if k else '')
            sr = dict(name=name, href=href(), n=n)
            if (lang, n - 1) in arts: sr['prev'] = (href(n - 1), arts[(lang, n - 1)]['title'])
            if (lang, n + 1) in arts: sr['next'] = (href(n + 1), arts[(lang, n + 1)]['title'])
            path = BA.page(f'{ser}/{n}', lang, a, LANGS4, TP, series=sr)
            retitle(ROOT + path, a['title'], SHORT[ser][lang], S[lang]['brand'])
            fix_cover(ROOT + path, ser, lang)
            CAT[f'{ser}/{n}'] = dict(slug=f'{ser}/{n}', series=ser, month=MONTH, langs=LANGS4, titles={l: arts[(l, n)]['title'] for l in LANGS4},
                                     tags=[], tags_l={l: [] for l in LANGS4}, published=max(arts[(l, n)]['published'] for l in LANGS4), img=True, descs={l: arts[(l, n)]['desc'] for l in LANGS4})
        CAT[ser] = dict(slug=ser, kind='series', month=MONTH, langs=LANGS4, titles=NAMES[ser], tags=[], tags_l={}, published=max(a['published'] for a in arts.values()), img=True, descs=SERIES_DESC[ser])
        M.SER, M.NAME, M.series_desc, M.TP = ser, NAMES[ser], (lambda lang, s=ser: SERIES_DESC[s][lang]), TP
        for lang in LANGS4:
            tmp = []                                    # series_page() looks for per-part thumbs/covers: lend it copies of the shared cover, then drop them
            import shutil
            for n in range(1, nparts + 1):
                for src, dst in ((f'thumb-{ser}-cover-{lang}.jpg', f'thumb-{ser}-{n}-{lang}.jpg'), (f'{ser}-cover-{lang}.jpg', f'{ser}-{n}-{lang}.jpg'), (f'og-{ser}-cover-{lang}.jpg', f'og-{ser}-{n}-{lang}.jpg')):
                    if not os.path.exists(D + dst): shutil.copy(D + src, D + dst); tmp.append(D + dst)
            cards = {(lang, n): dict(arts[(lang, n)], heads=[{'t': 'p', 'x': S[lang]['part'].format(n=num(n, lang))}]) for n in range(1, nparts + 1)}
            M.series_page(lang, cards, LANGS4)
            fix_cover(ROOT + f"{PFX[lang].lstrip('/')}{'/' if PFX[lang] else ''}articles/{ser}/index.html", ser, lang, series_page=True, nparts=nparts)
            for f in tmp: os.remove(f)
        print(ser, {l: [parsed[(l, n)]['cont'] for n in range(1, nparts + 1)] for l in LANGS4})
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)


def retitle(path, h1, short, brand):
    """<title> = "<heading> | <series> | <brand>", heading clipped so the whole tag stays near 70 characters."""
    tail = f' | {short} | {brand}'
    room = max(20, 70 - len(tail))
    head = h1 if len(h1) <= room else BA.clip(h1, room)
    tt = head + tail
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{html.escape(tt, quote=False)}</title>', s, count=1, flags=re.S)
    for pat in (r'(property="og:title"\s+content=")[^"]*', r'(name="twitter:title"\s+content=")[^"]*'):
        s = re.sub(pat, lambda m: m.group(1) + html.escape(tt, quote=True), s, count=1)
    open(path, 'w', encoding='utf-8').write(s)


def fix_cover(path, ser, lang, series_page=False, nparts=0):
    """Point the page's images at the series' shared cover instead of per-part files; give the series cards the shared thumb."""
    s = open(path, encoding='utf-8').read()
    cov = f'{ser}-cover-{lang}'
    s = re.sub(r'/images/articles/og-' + re.escape(ser) + r'-\d+-' + lang + r'\.jpg', f'/images/articles/og-{cov}.jpg', s)
    s = re.sub(r'/images/articles/' + re.escape(ser) + r'-\d+-' + lang + r'\.jpg', f'/images/articles/{cov}.jpg', s)
    s = re.sub(r'/images/articles/thumb-' + re.escape(ser) + r'-\d+-' + lang + r'\.jpg', f'/images/articles/thumb-{cov}.jpg', s)
    open(path, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    build(set(sys.argv[1:]) or None)
