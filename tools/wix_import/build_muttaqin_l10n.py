"""Sermon of Muttaqin in Farsi / Arabic / Urdu, part by part as the translations arrive.

Source: muttaqin_src/part<NN>.<lang>.txt (the channel's own posts, pasted by the editor), word for word. Only Telegram furniture is removed:
hashtags, ▪️◾️🔸 separators, the ༺《N》༻ counter, emoji bullets. Lines are classified as
  H  the "first characteristic…" heading      S  the characteristic itself (sub-heading)
  A  a Qur'an verse / hadith in Arabic (heavily vowelled)      P  prose      refs  the sources
Part N exists in a language only when its file does; the English page of that part then lists the other languages in its hreflang set.
The part's picture is the English poster (shared). The English video is NOT repeated on the other languages' pages (a translated video may exist).
usage: python3 build_muttaqin_l10n.py [--dry]     then build_sitemap.py, build_taxo.py, check_site.py
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
import build_muttaqin as BM
import build_mourning as M

SER = BM.SER
OTHER = ['ar', 'fa', 'ur']
LANGS4 = ['en', 'ar', 'fa', 'ur']
NAME = {'en': 'Sermon of Muttaqin', 'ar': 'خطبة المتقين', 'fa': 'خطبه متقین', 'ur': 'خطبۂ متقین'}
SERIES_DESC = {
 'en': BM.SERIES_DESC,
 'ar': 'سلسلة عن خطبة المتقين للإمام علي (ع): صفات المتقين صفةً صفة، مع قصص من أهل البيت (ع).',
 'fa': 'مجموعه‌ای درباره‌ی خطبه متقین امام علی (ع): ویژگی‌های پرهیزکاران، یکی پس از دیگری، همراه با داستان‌هایی از اهل بیت (ع).',
 'ur': 'امام علی (ع) کے خطبۂ متقین پر ایک سلسلہ: متقین کی صفات ایک ایک کر کے، اہل بیت (ع) کے واقعات کے ساتھ۔',
}
REFS_H = {'ar': 'المصادر', 'fa': 'منابع', 'ur': 'حوالہ جات'}
# the characteristic each part is about, in the part's own words (taken from its text); desc = one sentence for search results
CHARS = {
 1: {'ar': 'حُسنُ الكلام', 'fa': 'نیکو گفتار', 'ur': 'نیک اور درست گفتار'},
}
DESC = {
 1: {'ar': 'القسم ١ من خطبة المتقين: المتقون صواب المنطق. جواب الإمام علي (ع) لهمّام، والسيدة فضّة التي لم تتكلم إلا بالقرآن.',
     'fa': 'بخش ۱ خطبه متقین: متقین گفتاری درست و نیکو دارند. پاسخ امام علی (ع) به همام و داستان فضه که جز با قرآن سخن نگفت.',
     'ur': 'حصہ ۱ خطبۂ متقین: متقین کی گفتار درست اور نیک ہوتی ہے۔ ہمام کو امام علی (ع) کا جواب اور فضہ خاتون جو صرف قرآن کی زبان میں بولتی تھیں۔'},
}
DIAC = re.compile(r'[ً-ْٰ]')
ARLET = re.compile(r'[ء-يٮ-ە]')
SEP = re.compile(r'^[\s▪️◾️🔸▫️⸻➖\-—_*]*$')
BUL = re.compile(r'^[\s⚜️🔸▪️▫️◾️🔳📙📓📔📖✨️•]+')


def vowelled(t):
    a = len(ARLET.findall(t))
    return a >= 6 and len(DIAC.findall(t)) / a > 0.5


def parse(n, lang):
    raw = open(HERE + f'muttaqin_src/part{n:02d}.{lang}.txt', encoding='utf-8').read()
    blocks, refs, in_refs = [], [], False
    paras = [b for b in re.split(r'\n\s*\n', raw) if b.strip()]
    for bi, block in enumerate(paras):
        lines = [l.strip() for l in block.split('\n')]
        for ln in lines:
            if not ln or SEP.match(ln) or ln.startswith('#') or ln.startswith('༺'): continue
            is_ref = ln[:1] in '📓📔📙'
            emph = ln.startswith('⚜')
            ln = BUL.sub('', ln).strip()
            if not ln: continue
            if lang != 'fa' and re.match(r'^سور[ةۂه]', ln): in_refs = True      # ar / ur: the sources start at the surah line and run to the end
            if is_ref or in_refs:
                refs.append(ln); continue
            if re.match(r'^(اولین ویژگی|وأوَّلُ صفةٍ|خطبہ متقین میں امام کی بیان کردہ پہلی صفت)', ln): blocks.append(('H', ln)); continue
            if emph:
                blocks.append(('S', ln)); continue
            if vowelled(ln) and not re.match(r'^(يا|اے|ای) ', ln): blocks.append(('A', ln)); continue
            blocks.append(('P', ln))
    return blocks, refs


def body(a):
    lang = a['lang']
    if lang == 'en': return BM.mbody(a)
    out = []
    for k, t in a['blocks']:
        if k == 'H': out.append(f'<h3 class="art-section-title">{esc(t)}</h3>')
        elif k == 'S': out.append(f'<p class="kw-subhead">{esc(t)}</p>')
        elif k == 'A': out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">{esc(t)}</span></div>')
        else: out.append('<p>' + esc(t) + '</p>')
    if a['refs']:
        out.append(f'<h3 class="art-section-title">{REFS_H[lang]}</h3>')
        out.append('<ul class="kw-sources-list">' + ''.join(f'<li>{esc(r)}</li>' for r in a['refs']) + '</ul>')
    return out


BA.body_html = body


def available():
    got = {}
    for f in os.listdir(HERE + 'muttaqin_src'):
        m = re.match(r'part(\d\d)\.(ar|fa|ur)\.txt$', f)
        if m: got.setdefault(int(m.group(1)), []).append(m.group(2))
    return {n: sorted(v) for n, v in sorted(got.items())}


def sref(lang, n=None): return f"{PFX[lang]}/articles/{SER}/" + (f'{n}/' if n else '')


def share_images(n):
    D = BM.D
    for lang in OTHER:
        for stem in (f'{SER}-{n}', f'og-{SER}-{n}', f'thumb-{SER}-{n}'):
            shutil.copy(D + f'{stem}-en.jpg', D + f'{stem}-{lang}.jpg')


def main(dry=False):
    avail = available()
    CAT = json.load(open(HERE + 'catalog.json'))
    TPs = {l: template(l) for l in LANGS4}
    BA_TP = TPs
    arts = {}
    for n, langs in avail.items():
        if not dry: share_images(n)
        langs_n = ['en'] + langs
        a_en = BM.load(n); a_en['lang'] = 'en'
        arts[('en', n)] = a_en
        for l in langs:
            blocks, refs = parse(n, l)
            if dry:
                print(f'=== part {n} {l}')
                for k, t in blocks: print(f'  [{k}] {t[:90]}')
                print('  [refs]', refs)
                continue
            char = CHARS[n][l]
            title = f"{NAME[l]}، {S[l]['part'].format(n=num(n, l))} — {char}" if l != 'ur' else f"{NAME[l]}، {S[l]['part'].format(n=num(n, l))} — {char}"
            arts[(l, n)] = dict(lang=l, title=title, desc=DESC[n][l], published=a_en['published'], modified=a_en['published'], heads=[], hero_video=None,
                                body=[{'t': 'p', 'x': t} for _, t in blocks], tags=[], og='x', img=a_en['img'], blocks=blocks, refs=refs)
    if dry: return
    for (l, n), a in arts.items():
        langs_n = ['en'] + avail[n]
        sr = dict(name=NAME[l], href=sref(l), n=n)
        if (l, n - 1) in arts: sr['prev'] = (sref(l, n - 1), arts[(l, n - 1)]['title'])
        if (l, n + 1) in arts: sr['next'] = (sref(l, n + 1), arts[(l, n + 1)]['title'])
        path = BA.page(f'{SER}/{n}', l, a, langs_n, BA_TP, series=sr)
        if l == 'en': BM.retitle(path, n)
        else:
            tt = f"{a['title']} | {S[l]['brand']}"
            s = open(ROOT + path, encoding='utf-8').read()
            s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{html.escape(tt, quote=False)}</title>', s, count=1, flags=re.S)
            for pat in (r'(property="og:title"\s+content=")[^"]*', r'(name="twitter:title"\s+content=")[^"]*'):
                s = re.sub(pat, lambda m: m.group(1) + html.escape(tt, quote=True), s, count=1)
            open(ROOT + path, 'w', encoding='utf-8').write(s)
        e = CAT[f'{SER}/{n}']
        e['langs'] = langs_n
        e['titles'][l] = a['title']; e['descs'][l] = a['desc']
        e['tags_l'][l] = e['tags_l'].get('en', [])
    # series pages in the other languages, listing only the parts that exist there
    sl = ['en'] + sorted({l for (l, n) in arts if l != 'en'}, key=LANGS4.index)
    M.SER, M.NAME, M.series_desc, M.TP = SER, NAME, (lambda lang: SERIES_DESC[lang]), TPs
    for l in OTHER:
        cards = {(l, n): dict(arts[(l, n)], heads=[{'t': 'p', 'x': S[l]['part'].format(n=num(n, l))}]) for (ll, n) in arts if ll == l}
        if not cards: continue
        first = min(n for (_, n) in cards)
        M.series_page(l, cards, sl)
    # English series page: add the other languages to its hreflang set
    f = ROOT + f'articles/{SER}/index.html'
    s = open(f, encoding='utf-8').read()
    cur = f'{SITE}{sref("en")}'
    alts = ''.join(f'  <link rel="alternate"  hreflang="{l}" href="{SITE}{sref(l)}">\n' for l in sl)
    s = re.sub(r'(  <link rel="canonical"  href="[^"]*">\n)(?:  <link rel="alternate"[^\n]*\n)+', lambda m: m.group(1) + alts + f'  <link rel="alternate"  hreflang="x-default" href="{cur}">\n', s, count=1)
    open(f, 'w', encoding='utf-8').write(s)
    ser = CAT[SER]
    ser['langs'] = sl
    for l in OTHER:
        if l in sl: ser['titles'][l] = NAME[l]; ser['descs'][l] = SERIES_DESC[l]
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    print('built', {f'{l}{n}' for (l, n) in arts})


if __name__ == '__main__':
    main('--dry' in sys.argv)
