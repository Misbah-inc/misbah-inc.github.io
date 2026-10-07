"""Regenerate the 'Imported articles + indexes' block of sitemap.xml from catalog.json."""
import re, json, os
ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..') + '/'
cat = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/catalog.json'))
s = open(ROOT + 'sitemap.xml', encoding='utf-8').read()
s = re.sub(r'\n  <!-- ── Imported articles.*?(?=\n</urlset>)', '', s, flags=re.S)
for b in re.findall(r'\s*<url>.*?</url>', s, re.S):
    if re.search(r'<loc>https://article\.misbah-inc\.com(/ar|/fa|/ur)?/articles/</loc>', b): s = s.replace(b, '')
P = {'en': '', 'ar': '/ar', 'fa': '/fa', 'ur': '/ur'}
D = 'https://article.misbah-inc.com'

def blk(path, langs, pri, lm, freq='monthly'):
    out = ''
    for l in langs:
        out += f'  <url>\n    <loc>{D}{P[l]}{path}</loc>\n'
        out += ''.join(f'    <xhtml:link rel="alternate" hreflang="{x}" href="{D}{P[x]}{path}"/>\n' for x in langs)
        out += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{D}{P["en" if "en" in langs else langs[0]]}{path}"/>\n'
        out += f'    <lastmod>{lm}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>\n'
    return out

add = '\n  <!-- ── Imported articles + indexes ────────────────────────────── -->\n'
add += blk('/articles/', ['en', 'ar', 'fa', 'ur'], '0.9', max(c['published'] for c in cat.values()), 'weekly')
for slug, c in sorted(cat.items(), key=lambda kv: kv[1]['published'], reverse=True):
    add += blk(f'/articles/{slug}/', c['langs'], '0.7', c['published'])
s = s.replace('</urlset>', add.rstrip('\n') + '\n</urlset>')
open(ROOT + 'sitemap.xml', 'w', encoding='utf-8').write(s)
import xml.dom.minidom as m; m.parse(ROOT + 'sitemap.xml'); print('sitemap urls', s.count('<url>'))
