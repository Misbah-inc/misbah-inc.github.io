"""Special edition: the resemblance of Lady Zaynab (p) to Lady Khadijah (p) — a series in four languages (Part 1: 16 Oct 2026, Part 2: 17 Oct 2026).

Source: fa @misbah110 #22964, en @misbah110_en #23758, ar @misbah110_ar #499, ur @misbah110_ur #538 (work/tg/zaynab-khadijah-posts.json).
Text word for word; removed: the hashtag header, the ✦━✦ divider, the @channel footer and the emoji that open each paragraph.
The heading is the editor's own title (Farsi: «شباهت حضرت خانم زینب کبری (س) به حضرت خانم خدیجه کبری (س)»); en / ar / ur follow the wording of each language's post.
Until its pictures arrive the page uses images/og-default.jpg (logo on green): usage  python3 build_zaynab_khadijah.py [<wide image> [<square image>]]
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
from PIL import Image, ImageOps

LANGS4 = ['en', 'ar', 'fa', 'ur']
SLUG = 'resemblance-of-lady-zaynab-to-lady-khadijah'
DATE = '2026-10-16'
D = ROOT + 'images/articles/'
POSTS = json.load(open(HERE + 'work/tg/zaynab-khadijah-posts.json', encoding='utf-8'))        # part 1
PARTS = {1: dict(posts=POSTS, date='2026-10-16'),
         2: dict(posts=json.load(open(HERE + 'work/tg/zaynab-khadijah-posts-2.json', encoding='utf-8')), date='2026-10-17', image=ROOT + 'images/zaynab-khadijah-part2.jpg'),
         3: dict(posts=json.load(open(HERE + 'work/tg/zaynab-khadijah-posts-3.json', encoding='utf-8')), date='2026-10-18', image=ROOT + 'images/zaynab-khadijah-part3.jpg')}   # part 3: fa #22988, en #23780, ar #522, ur #565
_P46 = json.load(open(HERE + 'work/tg/zaynab-khadijah-posts-4-6.json', encoding='utf-8'))      # part 4: fa #22994, en #23786, ur #571 (no Arabic post); 5: fa #23023, en #23818, ar #556, ur #600; 6: fa #23043, en #23836, ar #573, ur #618
for _n, _d in ((4, '2026-10-19'), (5, '2026-10-21'), (6, '2026-10-23')):
    PARTS[_n] = dict(posts=_P46[str(_n)], date=_d, image=ROOT + f'images/zaynab-khadijah-part{_n}.jpg')   # part 2 (picture from the channels' photo post, 800x450 — the Telegram preview size): fa #22982, en #23775, ar #516, ur #556
TITLES = {'en': 'The Resemblance of Lady Zaynab al-Kubra (p) to Lady Khadijah al-Kubra (p)',
          'ar': 'شبه السيدة زينب الكبرى (ع) بالسيدة خديجة الكبرى (ع)',
          'fa': 'شباهت حضرت خانم زینب کبری (س) به حضرت خانم خدیجه کبری (س)',
          'ur': 'حضرت بی بی زینب کبریٰ (س) کی حضرت بی بی خدیجہ کبریٰ (س) سے شباہت'}
DIV = re.compile(r'^[\s✦━❁ا🌸─\-–—_•·]*$')
LEAD = re.compile(r'^[\s💫🌹🍎✨🤍]+')


def parse(text):
    blocks, refs = [], []
    for para in re.split(r'\n\s*\n', text):
        lines = [l.strip() for l in para.split('\n') if l.strip()]
        lines = [l for l in lines if not (l.startswith('#') or l.startswith('@') or DIV.match(l))]
        if not lines: continue
        if lines[0].startswith('📚'): refs.append(LEAD.sub('', lines[0][1:]).strip()); continue
        if lines[0].startswith('❝'):
            blocks.append(('Q', ' '.join(lines).strip('❝❞ ').replace('❝', '').replace('❞', '').strip())); continue
        blocks.append(('P', LEAD.sub('', ' '.join(lines))))
    return blocks, refs


def parse2(text):
    """Part 2: titles (A) / section headings (H) / sub-headings (S) / hadith in Arabic (A) / translations (Q) / sources (R) / prose (P)."""
    blocks, first = [], True
    strip = lambda t: re.sub(r'^[\s🌹🌿✨📜📚]+', '', t).strip()
    for para in re.split(r'\n\s*\n', text):
        lines = [l.strip() for l in para.split('\n') if l.strip() and not l.strip().startswith(('#', '@')) and not DIV.match(l.strip())]
        if not lines: continue
        if first:                                   # the two Arabic title lines of the post
            first = False
            blocks += [('A', strip(l).strip('«»').strip()) for l in lines]; continue
        head = lines[0]
        if head.startswith('📚'): blocks += [('R', strip(l)) for l in lines]
        elif head.startswith('📜'): blocks.append(('A', strip(' '.join(lines)).strip('«»').strip()))
        elif head.startswith('«'): blocks.append(('Q', ' '.join(lines).strip('«»').strip()))
        elif head.startswith(('🌿 «', '🌹 «', '✨')): blocks.append(('H', strip(' '.join(lines))))
        elif head.startswith('🌿'): blocks.append(('S', strip(' '.join(lines))))
        else: blocks.append(('P', strip(' '.join(lines))))
    return blocks, []


def parse3(text, lang):
    """Parts 3+ (line by line, each line opens with its own emoji): T title, H numbered heading, P prose, S sub-heading (a line ending in a colon),
    A Arabic quotation (a 📜 line or a heavily vowelled one), Q its translation (the next plain / ❝…❞ line; the Arabic page has none), R source."""
    DIAC = re.compile(r'[ً-ْٰ]'); ARL = re.compile(r'[ء-يٮ-ە]')
    vowelled = lambda t: (lambda a: a >= 6 and len(DIAC.findall(t)) / a > 0.3)(len(ARL.findall(t)))
    numbered = lambda t: re.match(r'^[0-9٠-٩۰-۹]+\s*[.\-)۔]\s*\S', t)
    EMO = '🌸🌹💫🌿📜📚💧🌙🍎✨'
    blocks = []
    for para in re.split(r'\n\s*\n', text):
        lines = [l.strip() for l in para.split('\n') if l.strip() and not l.strip().startswith(('#', '@')) and not DIV.match(l.strip())]
        for l in lines:
            emo = l[0] if l[0] in EMO else ''
            t = re.sub(r'^[\s' + EMO + r']+', '', l).replace('**', '').strip()
            quoted = t.startswith('❝')
            t = t.replace('❝', '').replace('❞', '').strip()
            if t.startswith('«') and t.endswith('»') and t.count('«') == 1: t = t[1:-1].strip()
            m = re.match(r'^«(.*?)»[\s؛;]*(.*)$', t)                      # a quoted Arabic text followed by its translation on the same line
            if not t: continue
            prev = blocks[-1][0] if blocks else ''
            if emo == '🌸':
                blocks.append(('H' if numbered(t.strip('🌸 ')) else 'T', t.strip('🌸 ')))
            elif emo == '📚': blocks.append(('R', t))
            elif emo == '💫': blocks.append(('P', t))
            elif t.endswith((':', '：')): blocks.append(('S', t))
            elif emo == '📜' and m and m.group(2): blocks += [('A', m.group(1).strip()), ('Q', m.group(2).strip())]
            elif emo == '📜' or vowelled(t): blocks.append(('A', t))
            elif emo == '🌹': blocks.append(('H', t))
            elif emo in ('💫', '🌿', '💧', '🌙', '🍎', '✨'): blocks.append(('P', t))
            elif numbered(t) and prev in ('T', ''): blocks.append(('H', t))
            elif prev == 'A' and lang != 'ar': blocks.append(('Q', t))
            else: blocks.append(('P', t))
    return blocks, []


# Editor's rewrites of a paragraph on the website (the Telegram post keeps its original wording; fa / ar / ur are my translations of the English rewrite, not yet reviewed by a native speaker): language -> [(start of the post's paragraph, [replacement paragraphs])]
OVERRIDES = {'en': [("It is narrated that when Lady Zaynab (peace be upon her) was born, Amir al-Mu'minin", [
    "It is narrated that when Lady Zaynab (peace be upon her) was born the Prophet (peace be upon him and his family) was away travelling, and the days went by with Lady Zaynab (peace be upon her) still unnamed at that time. Lady Fatima (peace be upon her) asked Imam Ali (peace be upon him) why they were waiting. He answered that this choice was not his to make: it belonged to the Prophet (peace be upon him and his family). When the Prophet (peace be upon him and his family) returned and heard the news, he did not wait a moment. He hurried straight to the house.",
    "When Amir al-Mu'minin (peace be upon him) came to the Prophet and said:"])],
 'fa': [("در روایتی آمده است: زمانی که حضرت زینب (س) متولد شد", [
    "در روایتی آمده است: زمانی که حضرت زینب (س) متولد شد، پیامبر (ص) در سفر بودند و روزها گذشت در حالی که حضرت زینب (س) در آن زمان هنوز بی‌نام بودند. حضرت فاطمه (س) از امام علی (ع) پرسیدند که چرا منتظر مانده‌اند. ایشان پاسخ دادند که این انتخاب با ایشان نیست؛ این کار از آنِ پیامبر (ص) است. هنگامی که پیامبر (ص) بازگشتند و خبر را شنیدند، لحظه‌ای درنگ نکردند و یکراست به سوی خانه شتافتند.",
    "هنگامی که حضرت امیرالمؤمنین (ع) خدمت پیامبر آمد و عرض کرد:"])],
 'ar': [("جاء في الرواية: لمّا وُلدت السيدة زينب", [
    "جاء في الرواية: لمّا وُلدت السيدة زينب (ع) كان النبي (ص) مسافراً، ومرّت الأيام والسيدة زينب (ع) ما زالت في ذلك الوقت بلا اسم. فسألت السيدة فاطمة (ع) الإمام علياً (ع) عن سبب الانتظار، فأجاب بأنّ هذا الاختيار ليس إليه، بل هو للنبي (ص). فلمّا عاد النبي (ص) وسمع الخبر لم ينتظر لحظة، بل أسرع إلى البيت مباشرة.",
    "وحين جاء أمير المؤمنين (ع) إلى النبي وقال:"])],
 'ur': [("ایک روایت میں آیا ہے: جب حضرت زینب (س) پیدا ہوئیں", [
    "ایک روایت میں آیا ہے: جب حضرت زینب (س) پیدا ہوئیں تو پیغمبر اکرم (ص) سفر پر تھے، اور دن گزرتے گئے جبکہ حضرت زینب (س) اس وقت تک بے نام تھیں۔ حضرت فاطمہ (س) نے امام علی (ع) سے پوچھا کہ کس بات کا انتظار کیا جا رہا ہے۔ انہوں نے جواب دیا کہ یہ انتخاب ان کے اختیار میں نہیں؛ یہ پیغمبر (ص) کا حق ہے۔ جب پیغمبر (ص) واپس آئے اور خبر سنی تو انہوں نے ایک لمحہ بھی انتظار نہ کیا اور سیدھے گھر کی طرف روانہ ہو گئے۔",
    "جب حضرت امیرالمؤمنین (ع) پیغمبر (ص) کی خدمت میں آئے اور عرض کیا:"])],
}


REFS_H = {'en': 'Source', 'ar': 'المصدر', 'fa': 'منبع', 'ur': 'حوالہ'}


def body(a):
    out = []
    for k, t in a['blocks']:
        if k == 'T': out.append(f'<h2 class="art-part-title">{esc(t)}</h2>')
        elif k == 'Q': out.append(f'<blockquote class="art-quote">{esc(t)}</blockquote>')
        elif k == 'H': out.append(f'<h3 class="art-section-title">{esc(t)}</h3>')
        elif k == 'S': out.append(f'<p class="kw-subhead">{esc(t)}</p>')
        elif k == 'A': out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{esc(t)}</span></div>')
        elif k == 'R': out.append(f'<p class="tg-ref">{esc(t)}</p>')
        else: out.append(f'<p>{esc(t)}</p>')
    if a['refs']:
        out.append(f'<h3 class="art-section-title">{REFS_H[a["lang"]]}</h3>')
        out.append('<ul class="kw-sources-list">' + ''.join(f'<li>{esc(r)}</li>' for r in a['refs']) + '</ul>')
    return out


BA.body_html = body


def images(wide=None, square=None):
    if wide:
        w = Image.open(wide).convert('RGB')
        ban = w.resize((1600, round(1600 * w.height / w.width)), Image.LANCZOS)
        og = ImageOps.fit(w, (1200, 630), Image.LANCZOS, centering=(0.5, 0.45))
        if square: Image.open(square).convert('RGB').resize((1000, 1000), Image.LANCZOS).save(D + f'{SLUG}-1-mobile.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    else:
        og = Image.open(ROOT + 'images/og-default.jpg').convert('RGB'); ban = og
    for l in LANGS4:
        f = f'{SLUG}-1-{l}'
        ban.save(D + f + '.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
        og.save(D + f'og-{f}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
        og.resize((480, round(480 * og.height / og.width)), Image.LANCZOS).save(D + f'thumb-{f}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    return ban.size


def mobile_banner(path, lang, part=1):
    if not os.path.exists(D + f'{SLUG}-{part}-mobile.jpg'): return
    s = open(path, encoding='utf-8').read()
    old = re.search(r'(<div class="kw-banner[^"]*"[^>]*>\s*)(<img src="/images/articles/' + SLUG + '-' + str(part) + '-' + lang + r'\.jpg"[^>]*>)', s)
    if not old or '<picture' in s: return
    pic = f'<picture><source media="(max-width: 700px)" srcset="/images/articles/{SLUG}-{part}-mobile.jpg" width="1000" height="1000">{old.group(2)}</picture>'
    open(path, 'w', encoding='utf-8').write(s.replace(old.group(0), old.group(1) + pic))


NAME = TITLES                      # the series name = the article's title
SERIES_DESC = {'en': 'A special edition of the Misbah channel on the resemblance of Lady Zaynab al-Kubra (p) to Lady Khadijah al-Kubra (p), part by part.',
               'ar': 'ملف خاص من قناة مصباح عن شبه السيدة زينب الكبرى (ع) بالسيدة خديجة الكبرى (ع)، جزءاً جزءاً.',
               'fa': 'ویژه‌نامه‌ی کانال مصباح درباره‌ی شباهت حضرت خانم زینب کبری (س) به حضرت خانم خدیجه کبری (س)، بخش به بخش.',
               'ur': 'مصباح چینل کا خصوصی شمارہ: حضرت بی بی زینب کبریٰ (س) کی حضرت بی بی خدیجہ کبریٰ (س) سے شباہت، حصہ بہ حصہ۔'}


def build(wide=None, square=None):
    import shutil
    import build_mourning as M
    size = images(wide, square)
    sizes = {1: size}
    for n, pt in PARTS.items():                      # later parts: their own picture if they have one, else the series picture
        if n == 1: continue
        if pt.get('image'):
            im = Image.open(pt['image']).convert('RGB')
            if im.width < 1600: im = im.resize((1600, round(1600 * im.height / im.width)), Image.LANCZOS)   # same banner width as Part 1 (a sharper original would be better)
            sizes[n] = im.size
            og = ImageOps.fit(im, (1200, 630), Image.LANCZOS, centering=(0.5, 0.5))
            for l in LANGS4:
                im.save(D + f'{SLUG}-{n}-{l}.jpg', 'JPEG', quality=84, progressive=True, optimize=True)
                og.save(D + f'og-{SLUG}-{n}-{l}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
                im.resize((480, round(480 * im.height / im.width)), Image.LANCZOS).save(D + f'thumb-{SLUG}-{n}-{l}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
            if os.path.exists(D + f'{SLUG}-{n}-mobile.jpg'): os.remove(D + f'{SLUG}-{n}-mobile.jpg')   # no square version: phones get the wide one
        else:
            sizes[n] = size
            for l in LANGS4:
                for stem in (f'{SLUG}', f'og-{SLUG}', f'thumb-{SLUG}'):
                    shutil.copy(D + f'{stem}-1-{l}.jpg', D + f'{stem}-{n}-{l}.jpg')
            shutil.copy(D + f'{SLUG}-1-mobile.jpg', D + f'{SLUG}-{n}-mobile.jpg')
    CAT = json.load(open(HERE + 'catalog.json'))
    TP = {l: template(l) for l in LANGS4}
    arts = {}
    avail = lambda n: [l for l in LANGS4 if l in PARTS[n]['posts']]          # a language is skipped for a part whose post does not exist (Part 4 has no Arabic post)
    for n, pt in PARTS.items():
        for l in avail(n):
            text = pt['posts'][l]['text']
            blocks, refs = parse(text) if n == 1 else (parse2(text) if n == 2 else parse3(text, l))
            for start, new in (OVERRIDES.get(l, []) if n == 1 else []):
                k = next(k for k, (kk, t) in enumerate(blocks) if t.startswith(start))
                blocks[k:k + 1] = [('P', t) for t in new]
            first = next(t for kk, t in blocks if kk == 'P')
            desc = BA.clip(re.sub(r'\s+', ' ', first), 160)
            arts[(l, n)] = dict(lang=l, title=f"{NAME[l]} — {S[l]['part'].format(n=num(n, l))}", desc=desc, published=pt['date'], modified=pt['date'],
                                heads=[{'t': 'p', 'x': S[l]['part'].format(n=num(n, l))}], hero_video=None, body=[{'t': 'p', 'x': t} for kk, t in blocks],
                                tags=[], og='x', img=dict(w=sizes[n][0], h=sizes[n][1], orig=sizes[n]), blocks=blocks, refs=refs)
    for (l, n), a in arts.items():
        href = lambda k=None, lg=l: f"{PFX[lg]}/articles/{SLUG}/" + (f'{k}/' if k else '')
        sr = dict(name=NAME[l], href=href(), n=n)
        before = [k for k in PARTS if k < n and (l, k) in arts]; after = [k for k in PARTS if k > n and (l, k) in arts]
        if before: sr['prev'] = (href(max(before)), arts[(l, max(before))]['title'])
        if after: sr['next'] = (href(min(after)), arts[(l, min(after))]['title'])
        path = BA.page(f'{SLUG}/{n}', l, a, avail(n), TP, series=sr)
        mobile_banner(ROOT + path, l, n)
        CAT[f'{SLUG}/{n}'] = dict(CAT.get(f'{SLUG}/{n}', {}), slug=f'{SLUG}/{n}', series=SLUG, month=5, langs=avail(n), titles={ll: arts[(ll, n)]['title'] for ll in avail(n)},
                                  tags=[], tags_l={ll: [] for ll in avail(n)}, published=PARTS[n]['date'], img=True, descs={ll: arts[(ll, n)]['desc'] for ll in avail(n)})
    M.SER, M.NAME, M.series_desc, M.TP = SLUG, NAME, (lambda lang: SERIES_DESC[lang]), TP
    for l in LANGS4:
        M.series_page(l, {(l, n): arts[(l, n)] for n in PARTS if (l, n) in arts}, LANGS4)
    last = max(pt['date'] for pt in PARTS.values())
    CAT[SLUG] = dict(slug=SLUG, kind='series', month=5, langs=LANGS4, titles=NAME, tags=[], tags_l={}, published=last, img=True, descs=SERIES_DESC)
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    print({n: avail(n) for n in PARTS})


if __name__ == '__main__':
    a = sys.argv[1:3]
    if not a and os.path.exists(ROOT + 'images/zaynab-khadijah-poster-wide.jpg'):      # default: the supplied posters
        a = [ROOT + 'images/zaynab-khadijah-poster-wide.jpg', ROOT + 'images/zaynab-khadijah-poster-square.jpg']
    build(*a)
