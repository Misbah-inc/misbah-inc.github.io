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


SPOTIFY_ICON = '<path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>'
SPOTIFY = {'en': ('Spotify', 'Misbah Podcast', 'Kawthar Series'), 'ar': ('Spotify', 'بودكاست مصباح', 'سلسلة مباحث الكوثر'),
           'fa': ('Spotify', 'پادکست مصباح', 'سلسله مباحث کوثر'), 'ur': ('Spotify', 'مصباح پوڈکاسٹ', 'سلسلۂ مباحثِ کوثر')}
SPOTIFY_URLS = ('https://open.spotify.com/show/1T4EHdbm7O0UhUMxXJ0y9w', 'https://open.spotify.com/show/1uIz5DDmEnCKS1OtrTsQFv')   # Misbah Podcast, Kawthar Series


def spotify_block(lang, suffix=''):
    lab, a, b = SPOTIFY[lang]
    return (f'<div class="social-dropdown" id="sp-dropdown{suffix}">\n'
            f'        <button class="social-btn" aria-label="{lab}" aria-expanded="false" aria-controls="sp-menu{suffix}">\n'
            f'          <svg viewBox="0 0 24 24" aria-hidden="true">{SPOTIFY_ICON}</svg>\n        </button>\n'
            f'        <div class="social-menu" id="sp-menu{suffix}" role="menu">\n'
            f'          <a href="{SPOTIFY_URLS[0]}" target="_blank" rel="noopener" role="menuitem">{a}</a>\n'
            f'          <a href="{SPOTIFY_URLS[1]}" target="_blank" rel="noopener" role="menuitem">{b}</a>\n        </div>\n      </div>')


def add_spotify(s, lang, tg_id, suffix):
    """Insert the Spotify menu right after the Telegram menu (idempotent)."""
    if f'id="sp-dropdown{suffix}"' in s: return s
    i = s.find(f'<div class="social-dropdown" id="{tg_id}">')
    if i < 0: return s
    j = balanced_div(s, i)
    return s[:j] + '\n\n      ' + spotify_block(lang, suffix) + s[j:]


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
    new = add_spotify(new, lang, 'tg-dropdown-f', '-f')
    return s[:i] + new + s[j:] if new != blk else s


MAIN = {'en': 'https://www.misbah-inc.com/', 'ar': 'https://www.misbah-inc.com/ar', 'fa': 'https://www.misbah-inc.com/fa', 'ur': 'https://www.misbah-inc.com/ur'}
MAIN_LABEL = {'en': 'Misbah Inc. main website', 'ar': 'الموقع الرئيسي لمصباح إنك.', 'fa': 'وب‌سایت اصلی مصباح انک.', 'ur': 'مصباح انک. کی مرکزی ویب سائٹ'}
_VER = {}
def asset_ver(name):
    """Short hash of the asset's content: the page links ?v=<hash>, so a changed stylesheet / script is fetched at once instead of after the 10-minute cache."""
    if name not in _VER:
        import hashlib
        _VER[name] = hashlib.md5(open(ROOT + 'assets/' + name, 'rb').read()).hexdigest()[:8]
    return _VER[name]


def version_assets(s):
    return re.sub(r'(assets/(theme\.js|script\.js|style\.css))(\?v=[0-9a-f]+)?(?=")', lambda m: f'{m.group(1)}?v={asset_ver(m.group(2))}', s)


def fix(path):
    s = open(path, encoding='utf-8').read()
    sv = version_assets(s)
    if sv != s:
        s = sv; open(path, 'w', encoding='utf-8').write(s)
    if 'id="tg-dropdown"' in s:                          # homepage hero: Spotify beside Telegram
        rel0 = os.path.relpath(path, ROOT).replace(os.sep, '/')
        hl = rel0.split('/')[0] if rel0.split('/')[0] in ('ar', 'fa', 'ur') else 'en'
        sp = add_spotify(s, hl, 'tg-dropdown', '')
        if sp != s: s = sp; open(path, 'w', encoding='utf-8').write(s)
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
    # the logo / "MISBAH" in the header leads to the organisation's main website (in the page's language), not to this article site's homepage
    logo = re.sub(r'<a href="[^"]*" class="nav-logo" aria-label="[^"]*">',
                  lambda _: f'<a href="{MAIN[cur]}" class="nav-logo" aria-label="{MAIN_LABEL[cur]}">', s, count=1)
    if logo != s:
        s = logo; open(path, 'w', encoding='utf-8').write(s)
        m = re.search(r'<header class="site-header">.*?</header>', s, re.S)
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
