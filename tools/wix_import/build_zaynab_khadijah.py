"""Special edition: the resemblance of Lady Zaynab (p) to Lady Khadijah (p) — one article in four languages (posted 16 Oct 2026).

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
POSTS = json.load(open(HERE + 'work/tg/zaynab-khadijah-posts.json', encoding='utf-8'))
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


REFS_H = {'en': 'Source', 'ar': 'المصدر', 'fa': 'منبع', 'ur': 'حوالہ'}


def body(a):
    out = []
    for k, t in a['blocks']:
        out.append(f'<blockquote class="art-quote">{esc(t)}</blockquote>' if k == 'Q' else f'<p>{esc(t)}</p>')
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
        if square: Image.open(square).convert('RGB').resize((1000, 1000), Image.LANCZOS).save(D + f'{SLUG}-mobile.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    else:
        og = Image.open(ROOT + 'images/og-default.jpg').convert('RGB'); ban = og
    for l in LANGS4:
        f = f'{SLUG}-{l}'
        ban.save(D + f + '.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
        og.save(D + f'og-{f}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
        og.resize((480, round(480 * og.height / og.width)), Image.LANCZOS).save(D + f'thumb-{f}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    return ban.size


def mobile_banner(path, lang):
    if not os.path.exists(D + f'{SLUG}-mobile.jpg'): return
    s = open(path, encoding='utf-8').read()
    old = re.search(r'(<div class="kw-banner[^"]*"[^>]*>\s*)(<img src="/images/articles/' + SLUG + '-' + lang + r'\.jpg"[^>]*>)', s)
    if not old or '<picture' in s: return
    pic = f'<picture><source media="(max-width: 700px)" srcset="/images/articles/{SLUG}-mobile.jpg" width="1000" height="1000">{old.group(2)}</picture>'
    open(path, 'w', encoding='utf-8').write(s.replace(old.group(0), old.group(1) + pic))


def build(wide=None, square=None):
    size = images(wide, square)
    CAT = json.load(open(HERE + 'catalog.json'))
    TP = {l: template(l) for l in LANGS4}
    titles, descs, arts = {}, {}, {}
    for l in LANGS4:
        blocks, refs = parse(POSTS[l]['text'])
        desc = BA.clip(re.sub(r'\s+', ' ', blocks[0][1]), 160)
        arts[l] = dict(lang=l, title=TITLES[l], desc=desc, published=DATE, modified=DATE, heads=[], hero_video=None, body=[{'t': 'p', 'x': t} for k, t in blocks],
                       tags=[], og='x', img=dict(w=size[0], h=size[1], orig=size), blocks=blocks, refs=refs)
        titles[l], descs[l] = TITLES[l], desc
    for l in LANGS4:
        path = BA.page(SLUG, l, arts[l], LANGS4, TP)
        mobile_banner(ROOT + path, l)
    CAT[SLUG] = dict(slug=SLUG, month=5, langs=LANGS4, titles=titles, tags=[], tags_l={l: [] for l in LANGS4}, published=DATE, img=True, descs=descs)
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    print(titles)


if __name__ == '__main__':
    a = sys.argv[1:3]
    if not a and os.path.exists(ROOT + 'images/zaynab-khadijah-poster-wide.jpg'):      # default: the supplied posters
        a = [ROOT + 'images/zaynab-khadijah-poster-wide.jpg', ROOT + 'images/zaynab-khadijah-poster-square.jpg']
    build(*a)
