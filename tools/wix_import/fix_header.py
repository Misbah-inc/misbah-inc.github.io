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


def fix(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'<header class="site-header">.*?</header>', s, re.S)
    if not m: return False
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    first = rel.split('/')[0]
    cur = first if first in ('ar', 'fa', 'ur') else 'en'
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
