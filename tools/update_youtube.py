#!/usr/bin/env python3
"""Refresh the homepage "Latest on YouTube" cards (all four languages) with the channel's newest Shorts.

The site is static and YouTube's feed has no CORS headers, so a browser cannot read it; this runs at build time instead:
  python3 tools/update_youtube.py            # rewrite index.html, ar|fa|ur/index.html if the cards changed
  python3 tools/update_youtube.py --dry-run  # only show what it would pick
Then deploy (tools/deploy_s3.py). Run it before every deploy, or on a schedule.

How a Short is recognised: YouTube's watch page of a Short has a canonical URL under /shorts/. Each language page gets the newest
Shorts whose title is in that language (English = Latin script; Arabic / Farsi / Urdu = by their letters), topped up with the newest
other Shorts, then with normal videos, so there are always 5 cards. Needs only the Python standard library and internet access.
"""
import re, sys, html, urllib.request, os

CHANNEL = 'UCqKAr8CHf_lziNorVvUgB0g'
ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/..') + '/'
PAGES = {'en': 'index.html', 'ar': 'ar/index.html', 'fa': 'fa/index.html', 'ur': 'ur/index.html'}
COUNT = 5
UA = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en'}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode('utf-8', 'ignore')


def lang_of(title):
    ar = len(re.findall(r'[\u0600-\u06FF]', title)); la = len(re.findall(r'[A-Za-z]', title))
    if la >= ar: return 'en'                       # mixed titles ("English | عربي") count as English
    if re.search(r'[ٹڈڑںہےۓ]', title): return 'ur'
    if re.search(r'[پچژگکی]', title): return 'fa'
    return 'ar'


def is_short(vid):
    try:
        page = get('https://www.youtube.com/watch?v=' + vid)
    except Exception:
        return False
    m = re.search(r'rel="canonical" href="([^"]+)"', page)
    return bool(m and '/shorts/' in m.group(1))


def feed():
    xml = get(f'https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}')
    out = []
    for e in re.findall(r'<entry>(.*?)</entry>', xml, re.S):
        out.append(dict(id=re.search(r'<yt:videoId>(.*?)</yt:videoId>', e).group(1),
                        title=html.unescape(re.search(r'<title>(.*?)</title>', e).group(1)).strip(),
                        date=re.search(r'<published>(.*?)</published>', e).group(1)[:10]))
    return out


def pick(videos, lang):
    same = [v for v in videos if v['short'] and lang_of(v['title']) == lang]
    other = [v for v in videos if v['short'] and v not in same]
    rest = [v for v in videos if not v['short']]
    return (same + other + rest)[:COUNT]


def card(v):
    t = html.escape(v['title'], quote=True)
    img = f"https://img.youtube.com/vi/{v['id']}/{'0' if v['short'] else 'hqdefault'}.jpg"
    return (f'<div class="short-card" data-id="{v["id"]}"><img src="{img}" alt="{t}" loading="lazy">'
            f'<div class="short-play-btn" aria-label="Play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></div>'
            f'<div class="short-title">{html.escape(v["title"])}</div></div>')


def main():
    dry = '--dry-run' in sys.argv
    vids = feed()
    for v in vids: v['short'] = is_short(v['id'])
    print(f'{len(vids)} videos in the feed, {sum(v["short"] for v in vids)} Shorts')
    changed = 0
    for lang, rel in PAGES.items():
        chosen = pick(vids, lang)
        print(f'[{lang}]', ', '.join(f"{v['id']}{'' if v['short'] else '(video)'}" for v in chosen))
        if dry: continue
        path = ROOT + rel
        s = open(path, encoding='utf-8').read()
        pat = re.compile(r'(<div class="shorts-grid"[^>]*>)(.*?)(\n?\s*</div>\s*<div class="shorts-footer">)', re.S)
        m = pat.search(s)
        if not m: print('  ! no shorts grid in', rel); continue
        new = '\n      ' + '\n      '.join(card(v) for v in chosen)
        s2 = s[:m.start(2)] + new + s[m.end(2):]
        if s2 != s:
            open(path, 'w', encoding='utf-8').write(s2); changed += 1
    print('pages updated:', changed)


if __name__ == '__main__':
    main()
