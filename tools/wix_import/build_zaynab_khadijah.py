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
         2: dict(posts=json.load(open(HERE + 'work/tg/zaynab-khadijah-posts-2.json', encoding='utf-8')), date='2026-10-17')}   # part 2: fa #22982, en #23775, ar #516, ur #556
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
        if k == 'Q': out.append(f'<blockquote class="art-quote">{esc(t)}</blockquote>')
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
    for n in PARTS:                                  # later parts share the series picture until they get their own
        if n == 1: continue
        for l in LANGS4:
            for stem in (f'{SLUG}', f'og-{SLUG}', f'thumb-{SLUG}'):
                shutil.copy(D + f'{stem}-1-{l}.jpg', D + f'{stem}-{n}-{l}.jpg')
        shutil.copy(D + f'{SLUG}-1-mobile.jpg', D + f'{SLUG}-{n}-mobile.jpg')
    CAT = json.load(open(HERE + 'catalog.json'))
    TP = {l: template(l) for l in LANGS4}
    arts = {}
    for n, pt in PARTS.items():
        for l in LANGS4:
            text = pt['posts'][l]['text']
            blocks, refs = parse(text) if n == 1 else parse2(text)
            for start, new in (OVERRIDES.get(l, []) if n == 1 else []):
                k = next(k for k, (kk, t) in enumerate(blocks) if t.startswith(start))
                blocks[k:k + 1] = [('P', t) for t in new]
            first = next(t for kk, t in blocks if kk == 'P')
            desc = BA.clip(re.sub(r'\s+', ' ', first), 160)
            arts[(l, n)] = dict(lang=l, title=f"{NAME[l]} — {S[l]['part'].format(n=num(n, l))}", desc=desc, published=pt['date'], modified=pt['date'],
                                heads=[{'t': 'p', 'x': S[l]['part'].format(n=num(n, l))}], hero_video=None, body=[{'t': 'p', 'x': t} for kk, t in blocks],
                                tags=[], og='x', img=dict(w=size[0], h=size[1], orig=size), blocks=blocks, refs=refs)
    for (l, n), a in arts.items():
        href = lambda k=None, lg=l: f"{PFX[lg]}/articles/{SLUG}/" + (f'{k}/' if k else '')
        sr = dict(name=NAME[l], href=href(), n=n)
        if (l, n - 1) in arts: sr['prev'] = (href(n - 1), arts[(l, n - 1)]['title'])
        if (l, n + 1) in arts: sr['next'] = (href(n + 1), arts[(l, n + 1)]['title'])
        path = BA.page(f'{SLUG}/{n}', l, a, LANGS4, TP, series=sr)
        mobile_banner(ROOT + path, l, n)
        CAT[f'{SLUG}/{n}'] = dict(CAT.get(f'{SLUG}/{n}', {}), slug=f'{SLUG}/{n}', series=SLUG, month=5, langs=LANGS4, titles={ll: arts[(ll, n)]['title'] for ll in LANGS4},
                                  tags=[], tags_l={ll: [] for ll in LANGS4}, published=PARTS[n]['date'], img=True, descs={ll: arts[(ll, n)]['desc'] for ll in LANGS4})
    M.SER, M.NAME, M.series_desc, M.TP = SLUG, NAME, (lambda lang: SERIES_DESC[lang]), TP
    for l in LANGS4:
        M.series_page(l, {(l, n): arts[(l, n)] for n in PARTS}, LANGS4)
    last = max(pt['date'] for pt in PARTS.values())
    CAT[SLUG] = dict(slug=SLUG, kind='series', month=5, langs=LANGS4, titles=NAME, tags=[], tags_l={}, published=last, img=True, descs=SERIES_DESC)
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    print({n: {l: arts[(l, n)]['title'][-12:] for l in LANGS4} for n in PARTS})


if __name__ == '__main__':
    a = sys.argv[1:3]
    if not a and os.path.exists(ROOT + 'images/zaynab-khadijah-poster-wide.jpg'):      # default: the supplied posters
        a = [ROOT + 'images/zaynab-khadijah-poster-wide.jpg', ROOT + 'images/zaynab-khadijah-poster-square.jpg']
    build(*a)
