"""Make every page's header right: language links go to the SAME page in each language, and the theme button is present.

The generators copy the header of the Lady Khadijah article into every page they write, so all of those pages used to carry that page's
language links (EN/AR/FA/UR all pointed at /…/articles/rabi_al_awwal/) and no theme button. This pass rewrites the language switcher
per page and adds the missing button. Idempotent; run after any build (build_sitemap.py and build_taxo.py call it).

For each language: the page's own hreflang alternate if it has one; otherwise the same path under that language prefix if the page exists
and is indexable; otherwise that language's articles index (for article pages) or home page. The current language gets class="active".
"""
import os, re, sys
ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..') + '/'
LANGS = ['en', 'ar', 'fa', 'ur']
LABEL = {'en': 'EN', 'ar': 'AR', 'fa': 'FA', 'ur': 'UR'}
SKIP = ('tools/', 'node_modules/', '.git/', 'assets/')
TOGGLE = None


def pfx(l): return '' if l == 'en' else f'/{l}'


def page_ok(rel_dir):
    f = ROOT + rel_dir + 'index.html'
    if not os.path.exists(f): return False
    head = open(f, encoding='utf-8').read(3000)
    return 'noindex' not in head


def theme_toggle():
    global TOGGLE
    if TOGGLE is None:
        s = open(ROOT + 'index.html', encoding='utf-8').read()
        TOGGLE = re.search(r'<button class="theme-toggle".*?</button>', s, re.S).group(0)
    return TOGGLE


_DD = {}


def dropdown_blocks(lang):
    """The homepage's WhatsApp / Telegram dropdown (button + the four channel links) for this language, as markup."""
    if lang not in _DD:
        f = ROOT + ('index.html' if lang == 'en' else f'{lang}/index.html')
        s = open(f, encoding='utf-8').read()
        blocks = {}
        for key in ('wa', 'tg'):
            i = s.index(f'<div class="social-dropdown" id="{key}-dropdown">')
            depth, j = 0, i
            for m in re.finditer(r'<div\b|</div>', s[i:]):
                depth += 1 if m.group(0) == '<div' else -1
                if depth == 0: j = i + m.end(); break
            blocks[key] = s[i:j]
        _DD[lang] = blocks
    return _DD[lang]


def balanced_div(s, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0: return start + m.end()
    return len(s)


def fix_footer(s, lang):
    """The footer's WhatsApp and Telegram icons were single links (one channel); give them the same four-channel menus as the top of the homepage."""
    i = s.find('<div class="footer-social"')
    if i < 0: return s
    j = balanced_div(s, i)
    blk, new = s[i:j], s[i:j]
    for key, pat in (('wa', r'<a href="https://chat\.whatsapp\.com/[^"]*" class="social-btn"[^>]*>.*?</a>'), ('tg', r'<a href="https://t\.me/misbah110[a-z_]*" class="social-btn"[^>]*>.*?</a>')):
        d = dropdown_blocks(lang)[key].replace(f'id="{key}-dropdown"', f'id="{key}-dropdown-f"').replace(f'id="{key}-menu"', f'id="{key}-menu-f"').replace(f'aria-controls="{key}-menu"', f'aria-controls="{key}-menu-f"')
        new = re.sub(pat, lambda _: d, new, count=1, flags=re.S)
    return s[:i] + new + s[j:] if new != blk else s


def fix(path):
    s = open(path, encoding='utf-8').read()
    # default theme = light: the attribute is the default, assets/theme.js replaces it with the visitor's saved choice
    ht = re.search(r'<html [^>]*>', s)
    if ht and 'data-theme' not in ht.group(0):
        s = s.replace(ht.group(0), ht.group(0)[:-1] + ' data-theme="light">', 1)
        open(path, 'w', encoding='utf-8').write(s)
    m = re.search(r'<header class="site-header">.*?</header>', s, re.S)
    if not m: return False
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    first = rel.split('/')[0]
    cur = first if first in ('ar', 'fa', 'ur') else 'en'
    s2 = fix_footer(s, cur)
    if s2 != s:
        s = s2; open(path, 'w', encoding='utf-8').write(s)
    rel_dir = rel[:-len('index.html')] if rel.endswith('index.html') else rel
    if cur != 'en': rel_dir = rel_dir[len(cur) + 1:]               # path without the language prefix, e.g. 'articles/x/1/'
    alts = {l: p for l, p in re.findall(r'hreflang="([a-z]{2})"\s+href="https://article\.misbah-inc\.com([^"]*)"', s)}
    hrefs = {}
    for l in LANGS:
        if l in alts: hrefs[l] = alts[l]
        elif page_ok((l + '/' if l != 'en' else '') + rel_dir): hrefs[l] = f'{pfx(l)}/{rel_dir}'
        elif rel_dir.startswith('articles/') and page_ok((l + '/' if l != 'en' else '') + 'articles/'): hrefs[l] = f'{pfx(l)}/articles/'
        else: hrefs[l] = f'{pfx(l)}/'
    if cur == 'en' and rel == '404.html': hrefs = {l: f'{pfx(l)}/' for l in LANGS}
    act = ' class="active"'
    rows = [f'        <a href="{hrefs[l]}" hreflang="{l}"{act if l == cur else ""}>{LABEL[l]}</a>' for l in LANGS]
    block = '<div class="lang-sw" aria-label="Language">\n' + '\n'.join(rows) + '\n      </div>'
    h = m.group(0)
    h2 = re.sub(r'<div class="lang-sw"[^>]*>.*?</div>', lambda _: block, h, count=1, flags=re.S)
    if 'theme-toggle' not in h2:
        h2 = h2.replace(block, block + '\n      ' + theme_toggle(), 1)
    if h2 == h: return False
    open(path, 'w', encoding='utf-8').write(s.replace(h, h2, 1))
    return True


def main():
    n = 0
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT).replace(os.sep, '/') + '/'
        dn[:] = [d for d in dn if d not in ('.git', 'node_modules', 'tools', 'assets', 'work', '.claude')]
        for name in fn:
            if name.endswith('.html') and fix(os.path.join(dp, name)): n += 1
    return n


if __name__ == '__main__':
    print('headers fixed:', main())
