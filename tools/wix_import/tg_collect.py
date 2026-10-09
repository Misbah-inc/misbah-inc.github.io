"""Collect the posts of a Telegram channel that carry a given hashtag (public web preview, read-only).
usage: python3 tg_collect.py   -> work/tg/<series>-<lang>.json  and a summary table
"""
import urllib.request, urllib.parse, re, html, json, os, time, sys
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
OUT = HERE + 'work/tg/'
CH = {'fa': 'misbah110', 'en': 'misbah110_en', 'ar': 'misbah110_ar', 'ur': 'misbah110_ur'}
SERIES = {
 'poems': {'fa': '#اشعار_حضرت_خدیجه_درباره_پیامبر', 'en': '#Poems_of_Lady_Khadijah_About_the_Prophet', 'ar': '#أشعار_السيدة_خديجة_في_النبي', 'ur': '#نبی_اکرم_کے_بارے_میں_حضرت_خدیجہ_کے_اشعار'},
 'biography': {'fa': '#زندگی_نامه_حضرت_خدیجه', 'en': '#Biography_of_Lady_Khadijah', 'ar': '#سيرة_السيدة_خديجة', 'ur': '#سوانح_حضرت_خدیجہ'},
 'ziyarat': {'fa': '#شرح_زیارت_حضرت_ام_المومنین', 'en': '#Explanation_of_the_Ziyarat_of_Ummul_Muminin', 'ar': '#شرح_زيارة_السيدة_أم_المؤمنين', 'ur': '#شرح_زیارت_حضرت_ام_المومنین'},
}


def fetch(ch, q=None, before=None):
    p = {}
    if q: p['q'] = q
    if before: p['before'] = before
    u = f'https://t.me/s/{ch}' + ('?' + urllib.parse.urlencode(p) if p else '')
    for k in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=25).read().decode('utf8', 'ignore')
        except Exception as e:
            time.sleep(2 * (k + 1))
    raise RuntimeError(u)


def parse(h):
    out = []
    for blk in re.split(r'(?=<div class="tgme_widget_message_wrap)', h)[1:]:
        pid = re.search(r'data-post="([^"]+)"', blk)
        if not pid: continue
        tx = re.search(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>\s*(?=<div class="tgme_widget_message_(?:footer|info)|<a class="tgme_widget_message_(?:link|date)|$)', blk, re.S) or re.search(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', blk, re.S)
        text = ''
        if tx:
            t = re.sub(r'<br\s*/?>', '\n', tx.group(1)); t = re.sub(r'</(?:p|div)>', '\n', t)
            text = html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
        d = re.search(r'<time[^>]*datetime="([^"]+)"', blk)
        out.append(dict(id=pid.group(1), n=int(pid.group(1).split('/')[1]), date=d.group(1) if d else '', text=text,
                        media=bool(re.search(r'tgme_widget_message_(photo|video|voice|document|roundvideo)', blk))))
    return out


def has_tag(text, tag):
    return re.search(r'(?<![\w])' + re.escape(tag) + r'(?![\w])', text) is not None


def collect(ch, tag):
    found, seen, before = {}, set(), None
    for _ in range(40):
        ps = parse(fetch(ch, tag, before))
        if not ps: break
        new = [p for p in ps if p['n'] not in seen]
        if not new: break
        for p in new:
            seen.add(p['n'])
            if has_tag(p['text'], tag): found[p['n']] = p
        before = min(p['n'] for p in ps)
        if len(ps) < 20: break
        time.sleep(0.4)
    return [found[k] for k in sorted(found)]


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    rows = {}
    for s, per in SERIES.items():
        for lang, tag in per.items():
            ps = collect(CH[lang], tag)
            json.dump(dict(series=s, lang=lang, channel=CH[lang], tag=tag, posts=ps), open(f'{OUT}{s}-{lang}.json', 'w'), ensure_ascii=False, indent=1)
            rows[(s, lang)] = ps
            print(f'{s:10} {lang}  {CH[lang]:13} {len(ps):3} posts', [p['n'] for p in ps][:30])
