import os, re, json, html
from gen_kawthar import *

ORD = {'en': {1: 'Part 1', 2: 'Part 2'}, 'ar': {1: 'القسم الأول', 2: 'القسم الثاني'},
       'fa': {1: 'بخش اول', 2: 'بخش دوم'}, 'ur': {1: 'حصہ اول', 2: 'حصہ دوم'}}
DESC = feed_desc()
ART = {(l, p): load(l, p) for l in LANGS for p in (1, 2)}
TITLES = feed_titles()
for k, a in ART.items():
    a['title'] = TITLES[k]   # the published post title; the in-body heading differs in ur Part 1 (Persian) and en Part 2 (split)
print({k: v for k, v in TITLES.items()})


def write(path, content):
    full = ROOT + path
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)


def words(a):
    return len(' '.join(b['x'] for b in a['body']).split())


def clip(t, n=155):
    t = re.sub(r'\s+', ' ', t).strip()
    if len(t) <= n:
        return t
    return t[:n].rsplit(' ', 1)[0].rstrip('،,.;:') + '…'


def part_page(lang, part):
    L = S[lang]; a = ART[(lang, part)]; tp = TP[lang]
    vid = VIDEO[(lang, part)]
    series_href = f'{PFX[lang]}/articles/{SLUG}/'
    title_tag = f"{L['series']}{ENDASH}{ORD[lang][part]} | {L['brand']}"
    desc = DESC[(lang, part)]
    cur = url(lang, f'part-{part}')
    mins = max(1, round(words(a) / 180))
    crumb_items = [(L['series'], series_href), (ORD[lang][part], None)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": cur + "#article", "headline": a['title'], "description": desc,
         "image": f"{SITE}/images/kawthar/og-part{part}-{lang}.jpg", "url": cur, "inLanguage": lang,
         "datePublished": a['published'], "dateModified": a['published'],
         "author": {"@id": SITE + "/#organization"}, "publisher": {"@id": SITE + "/#organization"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": cur},
         "isPartOf": {"@type": "CreativeWorkSeries", "name": L['series'], "url": url(lang)},
         "position": part, "keywords": a['tags'],
         "video": {"@type": "VideoObject", "name": a['title'], "description": desc,
                   "thumbnailUrl": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg", "uploadDate": a['published'],
                   "embedUrl": f"https://www.youtube.com/embed/{vid}", "contentUrl": f"https://www.youtube.com/watch?v={vid}",
                   "inLanguage": lang}},
        breadcrumb_ld(lang, [(L['series'], series_href), (ORD[lang][part], None)]),
        ORG]}
    extra = (f'  <meta property="article:published_time" content="{a["published"]}T00:00:00+00:00">\n'
             f'  <meta property="article:author" content="Misbah Inc.">\n'
             f'  <meta property="article:section" content="{html.escape(L["series"], quote=True)}">\n' +
             ''.join(f'  <meta property="article:tag" content="{html.escape(t, quote=True)}">\n' for t in a['tags']))
    h = head(lang, tp, title=title_tag, desc=clip(desc, 160), parts=(f'part-{part}',), og_img=f'/images/kawthar/og-part{part}-{lang}.jpg',
             og_type='article', published=a['published'], ld=ld, extra_meta=extra)
    prev = next_ = ''
    if part == 2:
        pa = ART[(lang, 1)]
        prev = f'<a class="prev" href="{PFX[lang]}/articles/{SLUG}/part-1/" rel="prev"><small>{"→" if lang != "en" else "←"} {L["prev"]}</small><strong>{esc(pa["title"])}</strong></a>'
    if part == 1:
        na = ART[(lang, 2)]
        next_ = f'<a class="next" href="{PFX[lang]}/articles/{SLUG}/part-2/" rel="next"><small>{L["next"]} {"←" if lang != "en" else "→"}</small><strong>{esc(na["title"])}</strong></a>'
    import taxonomy as TX
    tags = '<ul class="kw-tags" aria-label="Tags">' + ''.join(f'<li class="kw-tag-{kd}"><a href="{PFX[lang]}/articles/{c}">{esc(lb)}</a></li>' for kd, _, lb, c in TX.tag_list('al-kawthar', lang)) + '</ul>'
    back_arrow = '<path d="M5 12h14M12 5l7 7-7 7"/>' if lang != 'en' else '<path d="M19 12H5M12 5l-7 7 7 7"/>'
    main = f'''<main>

{banner(lang, part, a['title'])}

{crumbs(lang, crumb_items)}

<div class="art-page">
  <div class="art-container">

    <a href="{series_href}" class="art-back">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        {back_arrow}
      </svg>
      {esc(L['series'])}
    </a>

    <div class="art-meta">
      <span class="art-tag">{L['tag']}</span>
      <span class="art-month">{esc(L['series_short'])} · {ORD[lang][part]}</span>
      <span class="art-reading">{L['min'].format(n=num(mins, lang))}</span>
    </div>

    <div class="art-title-block">
      <h1 class="art-title">{esc(a['title'])}</h1>
    </div>

    {lang_switch(lang, f'part-{part}')}

    <div class="kw-lead-headings">{lead_heads_html(a)}</div>

    {video_html(a, lang, vid)}

    <section class="art-part" id="part{part}">
      <div class="art-body">

        {body_html(a)}

      </div>
    </section>

    <div class="art-divider">❖ &nbsp; ❖ &nbsp; ❖</div>

    {sources_html(a, lang)}

    {tags}

    <nav class="kw-partnav" aria-label="{esc(L['more_in'])}">{prev}{next_}</nav>

  </div><!-- /art-container -->
</div><!-- /art-page -->

</main>

'''
    tail = f'''
{tp['footer']}

<script src="/assets/theme.js"></script>
<script src="/assets/script.js"></script>
{VIDEO_JS}
</body>
</html>
'''
    write(f'{PFX[lang].lstrip("/")}{"/" if PFX[lang] else ""}articles/{SLUG}/part-{part}/index.html', h + main + tail)


def series_page(lang):
    L = S[lang]; tp = TP[lang]
    a1, a2 = ART[(lang, 1)], ART[(lang, 2)]
    intro = a1['body'][0]['x'] if not is_arabic_quote(a1['body'][0]['x']) else a1['body'][1]['x']
    # first paragraph of Part 1 that is actual prose
    for b in a1['body']:
        if len(b['x']) > 80 and not is_arabic_quote(b['x']):
            intro = b['x']; break
    desc = clip(intro)
    cur = url(lang)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": cur + "#webpage", "url": cur, "name": L['series'], "description": desc,
         "inLanguage": lang, "isPartOf": {"@id": SITE + "/#website"},
         "mainEntity": {"@type": "CreativeWorkSeries", "name": L['series'], "numberOfItems": 2,
                        "hasPart": [{"@type": "Article", "name": ART[(lang, p)]['title'], "url": url(lang, f'part-{p}'),
                                     "datePublished": ART[(lang, p)]['published']} for p in (1, 2)]}},
        breadcrumb_ld(lang, [(L['series'], None)]), ORG]}
    title_tag = f"{L['series']} | {L['brand']}"
    h = head(lang, tp, title=title_tag, desc=desc, parts=(), og_img='/images/kawthar/og-part1-' + lang + '.jpg',
             og_type='website', published='', ld=ld)
    cards = ''
    for p in (1, 2):
        a = ART[(lang, p)]
        cards += f'''
    <a class="kw-part-card" href="{PFX[lang]}/articles/{SLUG}/part-{p}/">
      <img src="/images/kawthar/part{p}-{lang}.jpg" alt="{html.escape(a['title'], quote=True)}" width="1400" height="{483 if p == 1 else 467}" loading="lazy" decoding="async">
      <div class="kw-part-body">
        <span class="kw-series-chip">{ORD[lang][p]}</span>
        <h2>{esc(a['title'])}</h2>
        <p>{esc(DESC[(lang, p)])}</p>
        <span class="btn btn-gold">{L['read']}</span>
      </div>
    </a>'''
    back_arrow = '<path d="M5 12h14M12 5l7 7-7 7"/>' if lang != 'en' else '<path d="M19 12H5M12 5l-7 7 7 7"/>'
    main = f'''<main>

{banner(lang, 1, L['series'])}

{crumbs(lang, [(L['series'], None)])}

<div class="art-page">
  <div class="art-container">

    <a href="{PFX[lang]}/articles/" class="art-back">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        {back_arrow}
      </svg>
      {L['all']}
    </a>

    <div class="art-meta"><span class="art-tag">{L['tag']}</span></div>

    <div class="art-title-block">
      <h1 class="art-title">{esc(L['series'])}</h1>
    </div>

    {lang_switch(lang)}

    <p class="art-intro">{esc(intro)}</p>

    <h2 class="art-section-title">{L['parts']}</h2>
    <div class="kw-parts">{cards}
    </div>

  </div>
</div>

</main>

'''
    tail = f'''
{tp['footer']}

<script src="/assets/theme.js"></script>
<script src="/assets/script.js"></script>
</body>
</html>
'''
    write(f'{PFX[lang].lstrip("/")}{"/" if PFX[lang] else ""}articles/{SLUG}/index.html', h + main + tail)


TP = {l: template(l) for l in LANGS}
for l in LANGS:
    series_page(l)
    for p in (1, 2):
        part_page(l, p)
print('built', [(l, p, len(ART[(l, p)]['body']), len(ART[(l, p)]['sources']), ART[(l, p)]['tags']) for l in LANGS for p in (1, 2)])
