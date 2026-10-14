"""Give every sitemap <url> a <lastmod> (YYYY-MM-DD) when the generators left it out.

Date = the page file's last git commit; a file with uncommitted changes counts as today.
Entries that already carry a lastmod (articles, from catalog.json) are left alone.
Run after build_sitemap.py / build_taxo.py; both call it at the end."""
import re, os, subprocess, datetime
ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..') + '/'
SITE = 'https://article.misbah-inc.com'


def main():
    today = datetime.date.today().isoformat()
    dirty = set(l[3:].strip().strip('"') for l in subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True).stdout.splitlines())
    s = open(ROOT + 'sitemap.xml', encoding='utf-8').read()

    def page_file(loc):
        p = loc[len(SITE):].lstrip('/')
        return p + 'index.html' if p == '' or p.endswith('/') else p

    def sub(m):
        blk = m.group(0)
        if '<lastmod>' in blk: return blk
        f = page_file(re.search(r'<loc>([^<]+)</loc>', blk).group(1))
        d = today if f in dirty else subprocess.run(['git', 'log', '-1', '--format=%cs', '--', f], cwd=ROOT, capture_output=True, text=True).stdout.strip() or today
        return blk.replace('</loc>', f'</loc>\n    <lastmod>{d}</lastmod>', 1)

    s2 = re.sub(r'<url>.*?</url>', sub, s, flags=re.S)
    open(ROOT + 'sitemap.xml', 'w', encoding='utf-8').write(s2)
    import xml.dom.minidom as m; m.parse(ROOT + 'sitemap.xml')
    print('lastmod on', s2.count('<lastmod>'), 'of', s2.count('<url>'), 'urls')


if __name__ == '__main__':
    main()
