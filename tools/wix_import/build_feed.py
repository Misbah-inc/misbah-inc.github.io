"""feed.xml — RSS 2.0 for the Misbah app (spec: misbah-app/docs/article-feed-spec.md).

One <item> per article per language, newest first, newest 20 per language. The <link> is the page's canonical URL, so the
language is the first path segment (/ar/, /fa/, /ur/; English has none) and `articles` follows it — which is what the app reads.
Everything (title, description, date, cover image) is taken from the generated pages themselves, so the feed cannot drift from the site.
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html, email.utils, datetime
sys.path.insert(0, HERE)
import build_index as BI
from gen_kawthar import PFX, LANGS, ROOT, SITE

PER_LANG = 20
CAT = json.load(open(HERE + 'catalog.json'))
# Al-Kawthar is listed as a series card on the index; the feed wants its two parts as separate items.
EXTRA = {'en': [('al-kawthar/part-1', '2026-09-25'), ('al-kawthar/part-2', '2026-10-01')],
         'ar': [('al-kawthar/part-1', '2026-09-29'), ('al-kawthar/part-2', '2026-10-05')],
         'fa': [('al-kawthar/part-1', '2026-09-29'), ('al-kawthar/part-2', '2026-10-05')],
         'ur': [('al-kawthar/part-1', '2026-09-29'), ('al-kawthar/part-2', '2026-10-05')]}


def page_path(lang, slug):
    return ROOT + (f'{lang}/' if lang != 'en' else '') + f'articles/{slug}/index.html'


def meta(s, pat):
    m = re.search(pat, s, re.S)
    return html.unescape(m.group(1)).strip() if m else ''


def item(lang, slug, date=None):
    f = page_path(lang, slug)
    if not os.path.exists(f):
        return None
    s = open(f, encoding='utf-8').read()
    link = meta(s, r'rel="canonical"\s+href="([^"]+)"')
    title = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', meta(s, r'<h1[^>]*>(.*?)</h1>')))
    desc = meta(s, r'name="description" content="([^"]*)"')
    img = meta(s, r'property="og:image"\s+content="([^"]+)"')
    pub = date or meta(s, r'article:published_time" content="(\d{4}-\d{2}-\d{2})') or CAT.get(slug, {}).get('published')
    if not (link and title and pub):
        return None
    local = ROOT + img.replace(SITE + '/', '') if img.startswith(SITE) else None
    return dict(lang=lang, title=title.strip(), link=link, desc=desc, date=pub, img=img, size=os.path.getsize(local) if local and os.path.exists(local) else 0)


def collect():
    out = []
    for lang in LANGS:
        items = []
        seen = set()
        for e in BI.entries(lang):
            slug = e['slug']
            if slug == 'al-kawthar':
                continue                       # replaced by its parts below
            it = item(lang, slug)
            if it and it['link'] not in seen:
                items.append(it); seen.add(it['link'])
        for sub, d in EXTRA[lang]:
            it = item(lang, sub, d)
            if it and it['link'] not in seen:
                items.append(it); seen.add(it['link'])
        items.sort(key=lambda x: (x['date'], x['link']), reverse=True)
        out += items[:PER_LANG]
    out.sort(key=lambda x: (x['date'], x['lang'] != 'en', x['link']), reverse=True)
    return out


def rfc822(d):
    dt = datetime.datetime.strptime(d, '%Y-%m-%d').replace(hour=9, tzinfo=datetime.timezone.utc)
    return email.utils.format_datetime(dt)


def esc(t):
    return html.escape(t, quote=False)


def build():
    items = collect()
    now = email.utils.format_datetime(datetime.datetime.now(datetime.timezone.utc))
    x = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', '  <channel>',
         '    <title>Misbah Articles</title>', f'    <link>{SITE}/</link>', '    <description>Articles from Misbah Inc.</description>',
         f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>', f'    <lastBuildDate>{now}</lastBuildDate>']
    for it in items:
        x += ['    <item>', f'      <title>{esc(it["title"])}</title>', f'      <link>{it["link"]}</link>', f'      <guid isPermaLink="true">{it["link"]}</guid>',
              f'      <description>{esc(it["desc"])}</description>', f'      <pubDate>{rfc822(it["date"])}</pubDate>']
        if it['img']:
            x.append(f'      <enclosure url="{it["img"]}" type="image/jpeg" length="{it["size"]}"/>')
        x.append('    </item>')
    x += ['  </channel>', '</rss>', '']
    open(ROOT + 'feed.xml', 'w', encoding='utf-8').write('\n'.join(x))
    return items


if __name__ == '__main__':
    its = build()
    import xml.dom.minidom as m
    m.parse(ROOT + 'feed.xml')
    bad = [i['link'] for i in its if not re.match(r'^https://article\.misbah-inc\.com/((ar|fa|ur)/)?articles/', i['link'])]
    print(len(its), 'items;', {l: sum(1 for i in its if i['lang'] == l) for l in LANGS}, '| bad links:', bad)
