"""Articles index with filters + static month / type / tag pages, in every language that has entries. Also: sitemap block + homepage month cards."""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_kawthar as G
import taxonomy as TX
import build_index as BI
from gen_kawthar import S, PFX, LANGS, ROOT, SITE, esc, head, template, ORG

U = {
 'en': dict(month='Month', type='Type', tag='Tag', all='All', search='Search articles…', clear='Clear filters', count='{n} results', none='Nothing matches these filters.',
            browse='Browse', by_month='By month', by_type='By type', by_tag='By tag', people='People', topics='Topics', home_all='All articles',
            page_desc='Articles and announcements from Misbah Inc. about {name}.', h1_suffix='', crumb_arts='Articles'),
 'ar': dict(month='الشهر', type='النوع', tag='الوسم', all='الكل', search='ابحث في المقالات…', clear='مسح التصفية', count='{n} نتيجة', none='لا توجد نتائج تطابق هذه التصفية.',
            browse='تصفّح', by_month='حسب الشهر', by_type='حسب النوع', by_tag='حسب الوسم', people='الأشخاص', topics='المواضيع', home_all='جميع المقالات',
            page_desc='مقالات وإعلانات من مؤسسة مصباح عن {name}.', h1_suffix='', crumb_arts='المقالات'),
 'fa': dict(month='ماه', type='نوع', tag='برچسب', all='همه', search='جستجو در مقالات…', clear='پاک کردن فیلترها', count='{n} نتیجه', none='موردی با این فیلترها یافت نشد.',
            browse='مرور', by_month='بر اساس ماه', by_type='بر اساس نوع', by_tag='بر اساس برچسب', people='شخصیت‌ها', topics='موضوعات', home_all='همه مقالات',
            page_desc='مقالات و اعلان‌های مصباح انک. درباره‌ی {name}.', h1_suffix='', crumb_arts='مقالات'),
 'ur': dict(month='مہینہ', type='قسم', tag='ٹیگ', all='سب', search='مضامین تلاش کریں…', clear='فلٹر ہٹائیں', count='{n} نتائج', none='ان فلٹرز سے کوئی نتیجہ نہیں ملا۔',
            browse='براؤز کریں', by_month='مہینے کے مطابق', by_type='قسم کے مطابق', by_tag='ٹیگ کے مطابق', people='شخصیات', topics='موضوعات', home_all='تمام مضامین',
            page_desc='مصباح انک. کی طرف سے {name} کے بارے میں مضامین اور اعلانات۔', h1_suffix='', crumb_arts='مضامین'),
}


def entries(lang):
    return BI.entries(lang)


def keys_of(e):
    return [('month', TX.month_path(e['month'])), ('type', e['type'])] + [('tag', t) for t in e['tags']]


def label(kind, key, lang):
    if kind == 'month':
        return TX.ANY_MONTH[lang] if key == 'any-time' else TX.MONTHS[lang][TX.MONTH_SLUG.index(key)]
    if kind == 'type': return TX.TYPES[key][lang]
    return TX.TAGS[key][lang]


def card(e, lang):
    mo = TX.month_name(lang, e['month'])
    tagl = ' '.join(t for t in e['tags'])
    srch = ' '.join([e['title'], mo, TX.TYPES[e['type']][lang]] + [TX.TAGS[t][lang] for t in e['tags']]).lower()
    ty_cls = ' al-ann' if e['type'] == 'announcement' else ''
    return f'''      <a class="al-card{ty_cls}" href="{e['href']}" data-month="{TX.month_path(e['month'])}" data-type="{e['type']}" data-tags="{tagl}" data-search="{html.escape(srch, quote=True)}">
        <img src="{e['img']}" alt="" width="480" height="270" loading="lazy" decoding="async">
        <div class="al-body">
          <span class="al-tag">{esc(TX.TYPES[e['type']][lang])}</span><span class="al-month">{esc(mo)}</span>
          <h3 class="al-title">{esc(e['title'])}</h3>
        </div>
      </a>'''


def counts(lang):
    c = {}
    for e in entries(lang):
        for k in keys_of(e): c[k] = c.get(k, 0) + 1
    return c


def pages_exist():
    """(kind,key,lang) -> number of entries, for every filter page that gets built."""
    out = {}
    for l in LANGS:
        for (k, key), n in counts(l).items(): out[(k, key, l)] = n
    return out


def url(lang, path=''):
    return f'{SITE}{PFX[lang]}/articles/{path}'


def build_head(lang, tp, title, desc, path, langs, ld, noindex=False, og='/images/kawthar/og-part1-en.jpg'):
    h = head(lang, tp, title=title, desc=desc, parts=(), og_img=og, og_type='website', published='', ld=ld)
    hl = ''.join(f'  <link rel="alternate" hreflang="{l}" href="{url(l, path)}">\n' for l in langs)
    hl += f'  <link rel="alternate" hreflang="x-default" href="{url("en" if "en" in langs else langs[0], path)}">'
    h = re.sub(r'  <!-- Canonical \+ hreflang -->.*?(?=\n\n  <!-- Open Graph)', f'  <!-- Canonical + hreflang -->\n  <link rel="canonical" href="{url(lang, path)}">\n{hl}', h, flags=re.S)
    h = h.replace(f'content="{SITE}{PFX[lang]}/articles/{G.SLUG}/"', f'content="{url(lang, path)}"')
    if noindex: h = h.replace('  <meta name="description"', '  <meta name="robots" content="noindex, follow">\n  <meta name="description"', 1)
    return h


FILTER_JS = '''<script>
/* Filters: month, type, tag and free-text search. State lives in the query string so a filtered view can be shared. */
(function () {
  var f = document.getElementById('al-filters'); if (!f) return;
  var cards = [].slice.call(document.querySelectorAll('.al-grid .al-card'));
  var sel = { month: f.querySelector('[name=month]'), type: f.querySelector('[name=type]'), tag: f.querySelector('[name=tag]') };
  var q = f.querySelector('[name=q]'), out = document.getElementById('al-count'), none = document.getElementById('al-none');
  function norm(s) { return (s || '').toLowerCase().replace(/[\\u064B-\\u0652\\u0670\\u0640]/g, ''); }
  function apply(push) {
    var m = sel.month.value, t = sel.type.value, g = sel.tag.value, s = norm(q.value.trim()), n = 0;
    cards.forEach(function (c) {
      var ok = (!m || c.dataset.month === m) && (!t || c.dataset.type === t) && (!g || (' ' + c.dataset.tags + ' ').indexOf(' ' + g + ' ') > -1) && (!s || norm(c.dataset.search).indexOf(s) > -1);
      c.hidden = !ok; if (ok) n++;
    });
    out.textContent = out.getAttribute('data-tpl').replace('{n}', n);
    none.hidden = n > 0;
    if (push) {
      var p = new URLSearchParams(); if (m) p.set('month', m); if (t) p.set('type', t); if (g) p.set('tag', g); if (s) p.set('q', q.value.trim());
      history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : ''));
    }
  }
  var p0 = new URLSearchParams(location.search);
  ['month', 'type', 'tag'].forEach(function (k) { if (p0.get(k)) sel[k].value = p0.get(k); });
  if (p0.get('q')) q.value = p0.get('q');
  [sel.month, sel.type, sel.tag].forEach(function (x) { x.addEventListener('change', function () { apply(true); }); });
  q.addEventListener('input', function () { apply(true); });
  f.querySelector('[type=reset]').addEventListener('click', function () { setTimeout(function () { apply(true); }, 0); });
  f.addEventListener('submit', function (e) { e.preventDefault(); });
  apply(false);
})();
</script>'''


def filter_bar(lang):
    u = U[lang]
    mopts = f'<option value="">{u["all"]}</option>' + ''.join(f'<option value="{TX.MONTH_SLUG[i]}">{esc(TX.MONTHS[lang][i])}</option>' for i in range(12)) + f'<option value="any-time">{esc(TX.ANY_MONTH[lang])}</option>'
    topts = f'<option value="">{u["all"]}</option>' + ''.join(f'<option value="{k}">{esc(v[lang])}</option>' for k, v in TX.TYPES.items())
    present = {k[1] for k in counts(lang) if k[0] == 'tag'}
    def grp(g, name): return f'<optgroup label="{esc(name)}">' + ''.join(f'<option value="{k}">{esc(v[lang])}</option>' for k, v in TX.TAGS.items() if v['group'] == g and k in present) + '</optgroup>'
    gopts = f'<option value="">{u["all"]}</option>' + grp('person', u['people']) + grp('topic', u['topics'])
    return f'''<form id="al-filters" class="al-filters" role="search">
      <label>{u['month']}<select name="month">{mopts}</select></label>
      <label>{u['type']}<select name="type">{topts}</select></label>
      <label>{u['tag']}<select name="tag">{gopts}</select></label>
      <label class="al-q">{u['search'].rstrip('…')}<input type="search" name="q" placeholder="{html.escape(u['search'], quote=True)}"></label>
      <button type="reset" class="btn btn-outline">{u['clear']}</button>
    </form>
    <p class="al-count" id="al-count" data-tpl="{u['count']}" aria-live="polite"></p>
    <p class="al-none" id="al-none" hidden>{u['none']}</p>'''


def browse_links(lang):
    u = U[lang]; ex = pages_exist()
    def row(title, items):
        li = ''.join(f'<li><a href="{PFX[lang]}/articles/{p}">{esc(lbl)}</a></li>' for lbl, p in items)
        return f'<div class="al-browse-row"><h2>{esc(title)}</h2><ul>{li}</ul></div>' if items else ''
    months = [(label('month', k, lang), f'month/{k}/') for k in TX.MONTH_SLUG + ['any-time'] if (('month', k, lang) in ex)]
    types = [(v[lang], f'type/{k}/') for k, v in TX.TYPES.items() if ('type', k, lang) in ex]
    tags = [(v[lang], f'tag/{k}/') for k, v in TX.TAGS.items() if ('tag', k, lang) in ex]
    return f'<nav class="al-browse" aria-label="{u["browse"]}">' + row(u['by_month'], months) + row(u['by_type'], types) + row(u['by_tag'], tags) + '</nav>'


def write(lang, path, content):
    p = ROOT + f'{PFX[lang].lstrip("/")}{"/" if PFX[lang] else ""}articles/{path}index.html'
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(content)


def index_page(lang):
    ui = BI.UI[lang]; u = U[lang]; L = S[lang]; tp = template(lang)
    ents = entries(lang)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url(lang) + "#webpage", "url": url(lang), "name": ui['title'], "description": ui['desc'], "inLanguage": lang,
         "isPartOf": {"@id": SITE + "/#website"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": SITE + e['href'], "name": e['title']} for i, e in enumerate(ents, 1)]}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": L['home'], "item": SITE + (PFX[lang] or '') + '/'},
                                                        {"@type": "ListItem", "position": 2, "name": ui['title']}]}, ORG]}
    h = build_head(lang, tp, f"{ui['title']} | {L['brand']}", ui['desc'], '', LANGS, ld, og=f'/images/kawthar/og-part1-{lang}.jpg')
    main = f'''<main>

<section class="al-hero">
  <span class="al-eyebrow">{esc(ui['eyebrow'])}</span>
  <h1>{esc(ui['h1'])}</h1>
  <p class="al-sub">{esc(ui['sub'])}</p>
</section>

<section class="section al-section" aria-label="{esc(ui['all'])}">
  <div class="container">
    {filter_bar(lang)}
    <div class="al-grid">
{chr(10).join(card(e, lang) for e in ents)}
    </div>
    {browse_links(lang)}
  </div>
</section>

</main>

'''
    tail = f'\n{tp["footer"]}\n\n<script src="/assets/theme.js"></script>\n<script src="/assets/script.js"></script>\n{FILTER_JS}\n</body>\n</html>\n'
    write(lang, '', h + main + tail)


def filter_page(kind, key, lang, n_by_lang):
    u = U[lang]; L = S[lang]; tp = template(lang)
    name = label(kind, key, lang)
    ents = [e for e in entries(lang) if (kind, key) in keys_of(e)]
    langs = [l for l in LANGS if n_by_lang.get(l, 0) > 0]
    path = f'{kind}/{key}/'
    thin = len(ents) < 2
    desc = u['page_desc'].format(name=name)
    title = f"{name} | {L['brand']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url(lang, path) + "#webpage", "url": url(lang, path), "name": name, "description": desc, "inLanguage": lang,
         "isPartOf": {"@id": SITE + "/#website"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": SITE + e['href'], "name": e['title']} for i, e in enumerate(ents, 1)]}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": L['home'], "item": SITE + (PFX[lang] or '') + '/'},
                                                        {"@type": "ListItem", "position": 2, "name": BI.UI[lang]['title'], "item": url(lang)},
                                                        {"@type": "ListItem", "position": 3, "name": name}]}, ORG]}
    h = build_head(lang, tp, title, desc, path, langs, ld, noindex=thin, og=f'/images/kawthar/og-part1-{lang}.jpg')
    sep = '›' if lang == 'en' else '‹'
    main = f'''<main>

<section class="al-hero">
  <span class="al-eyebrow"><a href="{PFX[lang]}/articles/">{esc(BI.UI[lang]['title'])}</a> {sep} {esc({'month': u['month'], 'type': u['type'], 'tag': u['tag']}[kind])}</span>
  <h1>{esc(name)}</h1>
</section>

<section class="section al-section">
  <div class="container">
    <div class="al-grid">
{chr(10).join(card(e, lang) for e in ents)}
    </div>
    <p class="al-all"><a class="btn btn-outline" href="{PFX[lang]}/articles/">{u['home_all']}</a></p>
  </div>
</section>

</main>

'''
    tail = f'\n{tp["footer"]}\n\n<script src="/assets/theme.js"></script>\n<script src="/assets/script.js"></script>\n</body>\n</html>\n'
    write(lang, path, h + main + tail)
    return thin


def sitemap():
    ex = pages_exist()
    s = open(ROOT + 'sitemap.xml', encoding='utf-8').read()
    s = re.sub(r'\n  <!-- ── Filter pages.*?(?=\n</urlset>|\n  <!-- ── )', '', s, flags=re.S)
    P = PFX
    D = SITE
    out = '\n  <!-- ── Filter pages (month / type / tag), only those with 2+ entries ── -->\n'
    done = set()
    for (k, key, l), n in sorted(ex.items()):
        if n < 2: continue
        langs = [x for x in LANGS if ex.get((k, key, x), 0) >= 2]
        path = f'/articles/{k}/{key}/'
        out += f'  <url>\n    <loc>{D}{P[l]}{path}</loc>\n' + ''.join(f'    <xhtml:link rel="alternate" hreflang="{x}" href="{D}{P[x]}{path}"/>\n' for x in langs)
        out += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{D}{P["en" if "en" in langs else langs[0]]}{path}"/>\n    <changefreq>weekly</changefreq>\n    <priority>0.5</priority>\n  </url>\n'
    s = s.replace('</urlset>', out.rstrip('\n') + '\n</urlset>')
    open(ROOT + 'sitemap.xml', 'w', encoding='utf-8').write(s)
    import xml.dom.minidom as m; m.parse(ROOT + 'sitemap.xml')
    return s.count('<url>')


def home_cards():
    """Homepage 'Through the Year': a month card is live when that language has an entry for the month."""
    ex = pages_exist()
    LBL = {'en': ('Read articles', 'Coming soon'), 'ar': ('اقرأ المقالات', 'قريباً'), 'fa': ('خواندن مقالات', 'به‌زودی'), 'ur': ('مضامین پڑھیں', 'جلد آرہا ہے')}
    for l in LANGS:
        f = ROOT + ('index.html' if l == 'en' else f'{l}/index.html')
        s = open(f, encoding='utf-8').read()
        many, soon = LBL[l]
        for n in range(1, 13):
            slug = TX.MONTH_SLUG[n - 1]
            live = ex.get(('month', slug, l), 0) > 0
            m = re.search(rf'<(?:a|div) class="year-card year-card--(?:live|soon)" data-month="{n}"[^>]*>(.*?)\n      </(?:a|div)>\n', s, re.S)
            inner = re.sub(r'<span class="year-status">.*?</span>', f'<span class="year-status">{many if live else soon}</span>', m.group(1))
            new = (f'<a class="year-card year-card--live" data-month="{n}" href="{PFX[l]}/articles/month/{slug}/">{inner}\n      </a>\n' if live
                   else f'<div class="year-card year-card--soon" data-month="{n}">{inner}\n      </div>\n')
            s = s[:m.start()] + new + s[m.end():]
        open(f, 'w', encoding='utf-8').write(s)


def main():
    ex = pages_exist()
    for l in LANGS: index_page(l)
    thin = 0; total = 0
    for (k, key, l), n in ex.items():
        by_lang = {x: ex.get((k, key, x), 0) for x in LANGS}
        total += 1; thin += filter_page(k, key, l, by_lang)
    print('index pages 4; filter pages', total, '(noindex, 1 entry:', thin, ')')
    print('sitemap urls', sitemap())
    home_cards()


if __name__ == '__main__':
    main()
