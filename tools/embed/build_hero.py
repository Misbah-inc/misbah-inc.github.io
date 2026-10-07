"""Builds tools/embed/misbah-hero.html — the homepage hero as ONE self-contained file (images inlined) for a Wix "Embed HTML" element."""
import re, io, base64, os
from PIL import Image
ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..') + '/'

def opt(name, maxw):
    im = Image.open(ROOT + f'assets/{name}.png').convert('RGBA')
    bb = im.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
    im = im.crop(bb); w, h = im.size
    im = im.resize((maxw, round(h * maxw / w)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=88, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(), im.size

top, ts = opt('logo-barak', 900); aj, as_ = opt('logo-ajjil', 560); bi, bs = opt('logo-biymnih', 560)
src = open(ROOT + 'index.html', encoding='utf-8').read()

def svg(label):
    m = re.search(r'aria-label="' + re.escape(label) + r'"[^>]*>\s*<svg[^>]*>(.*?)</svg>', src, re.S)
    return '<svg viewBox="0 0 24 24" aria-hidden="true">' + m.group(1) + '</svg>'

T = open(os.path.dirname(os.path.abspath(__file__)) + '/hero.template.html', encoding='utf-8').read()
for k, v in {'@@TOP@@': top, '@@AJ@@': aj, '@@BI@@': bi, '@@TOPW@@': str(ts[0]), '@@TOPH@@': str(ts[1]), '@@AJW@@': str(as_[0]), '@@AJH@@': str(as_[1]),
             '@@BIW@@': str(bs[0]), '@@BIH@@': str(bs[1]), '@@WA@@': svg('WhatsApp channels'), '@@TG@@': svg('Telegram channels'), '@@IG@@': svg('Instagram'),
             '@@FB@@': svg('Facebook'), '@@X@@': svg('X (Twitter)'), '@@YT@@': svg('YouTube'), '@@TT@@': svg('TikTok')}.items():
    T = T.replace(k, v)
open(os.path.dirname(os.path.abspath(__file__)) + '/misbah-hero.html', 'w', encoding='utf-8').write(T)
print(len(T) // 1024, 'KB')
