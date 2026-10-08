"""PDF booklet -> ordered article blocks.

The booklets are illustrated, slide-style PDFs (exported from PowerPoint). Per page this returns, top to bottom:
  ('P', text)            English text, from the PDF's text layer
  ('AR', jpg_bytes)      an Arabic line, cropped from the rendered page (the text layer's Arabic is scrambled by the font encoding)
  ('IMG', jpg_bytes, w, h)  an illustration embedded in the page
Decorative images (full-page backgrounds, small logos/title calligraphy) are skipped.
"""
import io, re, hashlib
import fitz
from PIL import Image

ARABIC = re.compile(r'[؀-ۿﭐ-﷿ﹰ-﻿]')
LATIN = re.compile(r'[A-Za-z]')


def _jpg(im, q=78, maxw=960):
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=q, progressive=True, optimize=True); return b.getvalue(), im.size


def decoration_hashes(doc):
    """md5 of every embedded image that appears on 3+ pages: the repeated background/frame/logo, not an illustration."""
    from collections import Counter
    c = Counter()
    for p in doc:
        seen = set()
        for img in p.get_images(full=True):
            h = hashlib.md5(doc.extract_image(img[0])['image']).hexdigest()
            if h not in seen: seen.add(h); c[h] += 1
    return {h for h, n in c.items() if n >= 3}


def page_items(doc, pno, dpi=200, deco=frozenset()):
    page = doc[pno]; W, H = page.rect.width, page.rect.height
    items = []
    d = page.get_text('dict')
    pix = None
    ar_lines, en_lines = [], []          # (bbox, text); a block can mix Arabic and English, so decide per line
    for blk in d['blocks']:
        if blk['type'] != 0: continue
        run = []
        def flush():
            if run: en_lines.append((tuple(run[0][0]), '\n'.join(t for _, t in run), tuple(run[-1][0])))
            run.clear()
        for ln in blk['lines']:
            t = ''.join(sp['text'] for sp in ln['spans']).strip()
            if not t: continue
            ar, la = len(ARABIC.findall(t)), len(LATIN.findall(t))
            if ar > la:
                flush(); ar_lines.append((ln['bbox'], t))
            else:
                run.append((ln['bbox'], t))
        flush()
    # English runs: bbox = union of the first and last line of the run
    en_blocks = []
    for first, txt, last in en_lines:
        en_blocks.append(((min(first[0], last[0]), first[1], max(first[2], last[2]), last[3]), txt))
    # runs that share a baseline are one visual line (a footnote or reference the PDF stores word by word): join them left to right
    en_blocks.sort(key=lambda e: (round(e[0][1]), e[0][0]))
    lines_ = []
    for bb, txt in en_blocks:
        for L in lines_:
            lo, hi = max(L['y0'], bb[1]), min(L['y1'], bb[3])
            if hi - lo > 0.5 * min(L['y1'] - L['y0'], bb[3] - bb[1]) and bb[0] >= L['x0'] - 1:
                L['parts'].append((bb[0], txt)); L['x0'] = min(L['x0'], bb[0]); L['y1'] = max(L['y1'], bb[3]); break
        else:
            lines_.append(dict(y0=bb[1], y1=bb[3], x0=bb[0], parts=[(bb[0], txt)]))
    en_blocks = []
    for L in lines_:
        L['parts'].sort()
        txt = ' '.join(t.replace('\n', ' ') if len(L['parts']) > 1 else t for _, t in L['parts'])
        en_blocks.append(((L['x0'], L['y0'], 0, L['y1']), txt))
    # lone quote marks / brackets that sit on an Arabic line belong to that picture: drop them
    ar_y = [(b[0][1], b[0][3]) for b in [((0, a[0][1], 0, a[0][3]), None) for a in ar_lines]]
    keep = []
    for bb, txt in en_blocks:
        if len(txt.strip()) <= 3 and re.fullmatch(r'[«»“”"()\[\]\-–—.…،؛:;\s]+', txt) and any(min(y1, bb[3]) - max(y0, bb[1]) > 0 for y0, y1 in ar_y):
            continue
        keep.append((bb, txt))
    en_blocks = keep
    for (x0, y0, x1, y1), txt in en_blocks:
        items.append((y0, 'P', re.sub(r'[ \t]+\n', '\n', txt)))
    # Arabic lines are scrambled in the text layer, and their boxes overlap each other: group the boxes that touch
    # vertically and cut one picture per group, stopping above the next English run so no English gets in.
    ar_lines.sort(key=lambda t: t[0][1])
    groups = []
    for (x0, y0, x1, y1), _ in ar_lines:
        if groups and y0 <= groups[-1][3] + 6:
            g = groups[-1]; groups[-1] = [min(g[0], x0), g[1], max(g[2], x1), max(g[3], y1)]
        else:
            groups.append([x0, y0, x1, y1])
    for x0, y0, x1, y1 in groups:
        below = [e[0][1] for e in en_blocks if e[0][1] >= y0 + 8]
        padb = 6
        # an English line just above whose box reaches into this one: start below it
        above = [e[0][3] for e in en_blocks if e[0][1] < y0 and y0 - 2 <= e[0][3] <= y0 + 22]
        if above: y0 = max(y0, max(above) + 1)
        y1_full = y1
        if below: y1 = min(y1, min(below) - 3); padb = 0
        if y1 - y0 < 10: y1, padb = y1_full, 6      # clipped to nothing (overlapping boxes): keep the whole box rather than lose the line
        if pix is None: pix = page.get_pixmap(dpi=dpi)
        s = dpi / 72; pad = 6
        im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples).crop(
            (max(0, (x0 - pad) * s), max(0, (y0 - (0 if above else pad)) * s), min(pix.width, (x1 + pad) * s), min(pix.height, (y1 + padb) * s)))
        bb, (w, h) = _jpg(im, 85, 1000)
        items.append((y0, 'AR', bb, w, h))
    for img in page.get_images(full=True):
        xref, sw, sh = img[0], img[2], img[3]
        for r in page.get_image_rects(xref):
            if hashlib.md5(doc.extract_image(xref)['image']).hexdigest() in deco: continue   # same picture on 3+ pages: frame/background/logo
            if sw < 400 or sh < 300: continue                    # logos, title calligraphy
            pm = fitz.Pixmap(doc, xref)
            if pm.n - pm.alpha >= 4: pm = fitz.Pixmap(fitz.csRGB, pm)
            im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples) if pm.alpha == 0 else Image.open(io.BytesIO(pm.tobytes('png')))
            b, (w, h) = _jpg(im)
            items.append((r.y0, 'IMG', b, w, h))
    items.sort(key=lambda t: t[0])
    return [t[1:] for t in items]


OPEN = re.compile(r'^[«“"(\[‘]+$'); CLOSE = re.compile(r'^[»”")\].,…;:!?’-]+$')


SHORT_OK = set('a i of to is in be by or on as at an it we he me my up so no do go us if am oh o'.split())


def _junk(t):
    """Fragments the PDF's text layer leaves behind: a lone footnote number, or a transliteration whose letters were dropped
    ("ā humma b ā rik li - mawl ā n ā"): mostly 1-2 letter pieces. The Arabic picture next to it already carries the text."""
    t = t.strip()
    if re.fullmatch(r'[\d\s\[\]()*.,:;\-–—…"“”«»]*', t): return True
    toks = re.findall(r"[^\W\d_]+", t)
    iso = [w for w in toks if len(w) == 1 and w in 'āīūḥṣḍṭẓĀĪŪ']       # a long vowel / dotted letter standing alone = a transliteration that lost its glyphs
    if len(t) < 140 and (len(iso) >= 2 or (len(iso) == 1 and len(toks) <= 4)): return True
    return len(toks) == 1 and len(toks[0]) <= 3 and len(t) <= 4 and not t.endswith('.')


def merge_text(items):
    items = _attach_punct(items)
    items = _merge_text(items)
    return [it for it in items if not (it[0] == 'P' and _junk(it[1]))]


def _attach_punct(items):
    """A paragraph that is only an opening bracket/quote joins the next text; one that is only closing punctuation joins the previous."""
    out, pend = [], ''
    for it in items:
        if it[0] == 'P':
            t = it[1].strip()
            if OPEN.match(t): pend += t; continue
            if CLOSE.match(t) and out and out[-1][0] == 'P': out[-1] = ('P', out[-1][1] + t); continue
            if pend: t = pend + t; pend = ''
            out.append(('P', t))
        else:
            out.append(it)
    return out


def _merge_text(items):
    """Join consecutive English text blocks that are one sentence broken across lines/blocks."""
    out = []
    for it in items:
        if it[0] == 'P':
            t = re.sub(r'\s*\n\s*', ' ', it[1]).strip()
            if out and out[-1][0] == 'P' and not re.search(r'[.!?…:”"»)\]]$', out[-1][1]) and t and (t[0].islower() or len(out[-1][1]) >= 40):   # a long line with no ending is a wrapped line
                out[-1] = ('P', out[-1][1] + ' ' + t)
            else:
                out.append(('P', t))
        else:
            out.append(it)
    return out


def stack_ar(items):
    """Consecutive Arabic crops are lines of one passage: stack them into one image."""
    out = []
    for it in items:
        if it[0] == 'AR' and out and out[-1][0] == 'AR':
            a = Image.open(io.BytesIO(out[-1][1])); b = Image.open(io.BytesIO(it[1]))
            w = max(a.width, b.width)
            bg = Image.new('RGB', (w, a.height + b.height), a.getpixel((2, 2)))
            bg.paste(a, ((w - a.width) // 2, 0)); bg.paste(b, ((w - b.width) // 2, a.height))
            j, (ww, hh) = _jpg(bg, 85, 1000)
            out[-1] = ('AR', j, ww, hh)
        else:
            out.append(it)
    return out


def extract(path, first_page=0):
    doc = fitz.open(path)
    deco = decoration_hashes(doc)
    pages = []
    for i in range(doc.page_count):
        pages.append(merge_text(page_items(doc, i, deco=deco)))
    cover = doc[0].get_pixmap(dpi=110)
    return dict(pages=pages, n=doc.page_count, meta=doc.metadata, cover=Image.frombytes('RGB', (cover.width, cover.height), cover.samples))
