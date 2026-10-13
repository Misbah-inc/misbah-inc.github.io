"""Occasions of the Month of Jumada al-Ula (Shia calendar post, 12 Oct 2026) — one article in four languages.

Source: the channel posts (fa @misbah110 #22933, en _en #23724, ar _ar #469, ur _ur #509), kept in work/tg/jumada1-posts.json.
Text is word for word; only the hashtag header, the ✦━✦ dividers and the @channel footer are dropped. The emoji that open each occasion
(✨ ⚔️ ▪️) are decoration and go too; the numbers stay.
usage: python3 build_occasions_jumada.py <dir with the wide and square images>   (images are optional on a rebuild)
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_articles import *
import build_articles as BA
from PIL import Image, ImageOps

LANGS4 = ['en', 'ar', 'fa', 'ur']
SLUG = 'occasions-of-jumada-al-ula'
DATE = '2026-10-12'
D = ROOT + 'images/articles/'
POSTS = json.load(open(HERE + 'work/tg/jumada1-posts.json', encoding='utf-8'))
DIV = re.compile(r'^[\s✦━❁ا🌸─\-–—_•·]*$')
LEAD = re.compile(r'^[✨⚔️▪️💫🌸\s]+')
ITEM = re.compile(r'^[✨⚔▪️️\s]*([0-9٠-٩۰-۹]+\s*\))')


def parse(text):
    lines = [l.strip() for l in text.split('\n')]
    title, blocks = '', []
    for l in lines:
        if not l or DIV.match(l) or l.startswith('#') or l.startswith('@'): continue
        if not title and l.startswith('🌸'): title = l.strip('🌸 ').strip(); continue
        if l.startswith('💫'): blocks.append(('lead', LEAD.sub('', l))); continue
        if ITEM.match(l): blocks.append(('item', LEAD.sub('', l))); continue
        blocks.append(('p', LEAD.sub('', l)))
    return title, blocks


def rbody(a):
    out, items = [], []
    for k, t in a['blocks']:
        if k == 'item': items.append(f'<li>{esc(t)}</li>'); continue
        if items: out.append('<ul class="occ-list">' + ''.join(items) + '</ul>'); items = []
        out.append(f'<p>{esc(t)}</p>')
    if items: out.append('<ul class="occ-list">' + ''.join(items) + '</ul>')
    return out


BA.body_html = rbody


def images(src_dir):
    wide = next(os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.startswith('wide'))
    sq = next(os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.startswith('square'))
    w = Image.open(wide).convert('RGB'); s = Image.open(sq).convert('RGB')
    ban = w.resize((1600, round(1600 * w.height / w.width)), Image.LANCZOS)
    og = ImageOps.fit(w, (1200, 630), Image.LANCZOS, centering=(0.5, 0.45))
    for l in LANGS4:
        f = f'{SLUG}-{l}'
        ban.save(D + f + '.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
        og.save(D + f'og-{f}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
        og.resize((480, 252), Image.LANCZOS).save(D + f'thumb-{f}.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    s.resize((1000, 1000), Image.LANCZOS).save(D + f'{SLUG}-mobile.jpg', 'JPEG', quality=80, progressive=True, optimize=True)
    return ban.size


def mobile_banner(path, lang, size):
    """Phones get the square picture (as supplied), laptops the wide one."""
    s = open(path, encoding='utf-8').read()
    old = re.search(r'(<div class="kw-banner[^"]*"[^>]*>\s*)(<img src="/images/articles/' + SLUG + '-' + lang + r'\.jpg"[^>]*>)', s)
    if not old or '<picture' in s: return
    pic = f'<picture><source media="(max-width: 700px)" srcset="/images/articles/{SLUG}-mobile.jpg" width="1000" height="1000">{old.group(2)}</picture>'
    s = s.replace(old.group(0), old.group(1) + pic)
    open(path, 'w', encoding='utf-8').write(s)


def build(src_dir=None):
    size = images(src_dir) if src_dir else (1600, 900)
    CAT = json.load(open(HERE + 'catalog.json'))
    TP = {l: template(l) for l in LANGS4}
    arts, titles, descs = {}, {}, {}
    for l in LANGS4:
        title, blocks = parse(POSTS[l]['text'])
        lead = next(t for k, t in blocks if k == 'lead')
        first = next(t for k, t in blocks if k == 'item')
        desc = BA.clip(re.sub(r'\s+', ' ', lead + ' ' + first), 160)
        arts[l] = dict(title=title, desc=desc, published=DATE, modified=DATE, heads=[], hero_video=None, body=[{'t': 'p', 'x': t} for k, t in blocks],
                       tags=[], og='x', img=dict(w=size[0], h=size[1], orig=size), blocks=blocks)
        titles[l], descs[l] = title, desc
    for l in LANGS4:
        path = BA.page(SLUG, l, arts[l], LANGS4, TP)
        mobile_banner(ROOT + path, l, size)
    CAT[SLUG] = dict(slug=SLUG, month=5, langs=LANGS4, titles=titles, tags=[], tags_l={l: [] for l in LANGS4}, published=DATE, img=True, descs=descs)
    json.dump(CAT, open(HERE + 'catalog.json', 'w'), ensure_ascii=False, indent=1)
    print({l: titles[l] for l in LANGS4})


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else None)
