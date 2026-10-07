"""Articles index pages (all four languages) + EN month-modal data, from catalog.json."""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_kawthar as G
from gen_kawthar import S, PFX, LANGS, ROOT, SITE, esc, head, template, ORG, breadcrumb_ld
from PIL import Image, ImageOps

SP = G.SP
CAT = json.load(open(HERE + 'catalog.json'))
for l, v in {'en': 'Article', 'ar': 'مقالة', 'fa': 'مقاله', 'ur': 'مضمون'}.items(): S[l]['article'] = v
MONTH = {
 'en': ['Muharram', 'Safar', "Rabi' al-Awwal", "Rabi' al-Thani", 'Jumada al-Awwal', 'Jumada al-Thani', 'Rajab', "Sha'ban", 'Ramadan', 'Shawwal', "Dhu al-Qi'dah", 'Dhu al-Hijjah'],
 'ar': ['مُحَرَّم', 'صَفَر', 'رَبِيعُ الأَوَّل', 'رَبِيعُ الآخِر', 'جُمَادَى الأُولَى', 'جُمَادَى الآخِرَة', 'رَجَب', 'شَعْبَان', 'رَمَضَان', 'شَوَّال', 'ذُو القَعْدَة', 'ذُو الحِجَّة'],
 'fa': ['محرم', 'صفر', 'ربیع‌الاول', 'ربیع‌الثانی', 'جمادی‌الاول', 'جمادی‌الثانی', 'رجب', 'شعبان', 'رمضان', 'شوال', 'ذی‌القعده', 'ذی‌الحجه'],
 'ur': ['محرم', 'صفر', 'ربیع الاول', 'ربیع الثانی', 'جمادی الاول', 'جمادی الثانی', 'رجب', 'شعبان', 'رمضان', 'شوال', 'ذیقعدہ', 'ذوالحجہ']}
UI = {
 'en': dict(title='Articles', eyebrow='Misbah Inc.  ·  Knowledge & Reflection', h1="Ma'ārif of the Ahlul Bayt (p)", sub='Through the Year',
            desc="Articles, reflections and Ma'ārif of the Ahlul Bayt (p) from Misbah Inc., organised through the Islamic year.", all='All articles', series='Series', read='Read'),
 'ar': dict(title='المقالات', eyebrow='مؤسسة مصباح  ·  معرفة وتأمل', h1='معارف أهل البيت عليهم السلام', sub='عبر العام',
            desc='مقالات وتأملات ومعارف أهل البيت عليهم السلام من مؤسسة مصباح، مرتبة على السنة الهجرية.', all='جميع المقالات', series='سلسلة', read='اقرأ'),
 'fa': dict(title='مقالات', eyebrow='مصباح انک.  ·  دانش و اندیشه', h1='معارف اهل‌بیت علیهم‌السلام', sub='در گذر سال',
            desc='مقالات، تأملات و معارف اهل‌بیت علیهم‌السلام از مصباح انک.، به ترتیب سال هجری.', all='همه مقالات', series='سلسله', read='بخوانید'),
 'ur': dict(title='مضامین', eyebrow='مصباح انک.  ·  علم و فکر', h1='معارفِ اہلِ بیت علیہم السلام', sub='سال بھر',
            desc='مصباح انک. کی طرف سے اہلِ بیت علیہم السلام کے معارف پر مضامین اور تحریریں، ہجری سال کی ترتیب سے۔', all='تمام مضامین', series='سلسلہ', read='پڑھیں')}


def title_of(l, rel):
    t = open(ROOT + rel, encoding='utf-8').read()
    return html.unescape(re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S).group(1).replace('<br>', ' ').strip())


def entries(lang):
    """one entry per article/series in this language, newest first."""
    out = []
    d = ROOT + 'images/articles/'
    os.makedirs(d, exist_ok=True)

    def thumb(src, name):
        dst = f'{d}thumb-{name}.jpg'
        if not os.path.exists(ROOT + src): return '/images/articles/thumb-fallback.jpg'   # no cover on Wix: branded placeholder
        if not os.path.exists(dst):
            im = ImageOps.fit(Image.open(ROOT + src).convert('RGB'), (480, 270), method=Image.LANCZOS, centering=(0.5, 0.4))
            im.save(dst, 'JPEG', quality=78, progressive=True, optimize=True)
        return f'/images/articles/thumb-{name}.jpg'

    # Khadijah (hand-written page, four languages)
    kp = ('' if lang == 'en' else lang + '/') + 'articles/rabi_al_awwal/index.html'
    out.append(dict(href=f'{PFX[lang]}/articles/rabi_al_awwal/', title=title_of(lang, kp), month=3, date='2026-09-01',
                    tag={'en': 'Lady Khadijah (p)', 'ar': 'السيدة خديجة عليها السلام', 'fa': 'حضرت خدیجه سلام الله علیها', 'ur': 'حضرت خدیجہ سلام اللہ علیہا'}[lang],
                    img=thumb('images/lady-khadijah-article.jpg', 'rabi_al_awwal'), series=False))
    # Al-Kawthar series
    out.append(dict(href=f'{PFX[lang]}/articles/al-kawthar/', title=S[lang]['series'], month=None, date='2026-10-05',
                    tag=UI[lang]['series'], img=thumb(f'images/kawthar/part1-{lang}.jpg', f'al-kawthar-{lang}'), series=True))
    for slug, c in CAT.items():
        if lang not in c['langs']: continue
        tags = c.get('tags_l', {}).get(lang) or []
        out.append(dict(href=f'{PFX[lang]}/articles/{slug}/', title=c['titles'][lang], month=c['month'], date=c['published'],
                        tag=tags[0] if tags else UI[lang]['title'],
                        img=thumb(f'images/articles/{slug}-{lang}.jpg', f'{slug}-{lang}'), series=False))
    out.sort(key=lambda e: e['date'], reverse=True)
    return out


def card(e, lang):
    mn = MONTH[lang][e['month'] - 1] if e['month'] else ''
    meta = f'<span class="al-month">{esc(mn)}</span>' if mn else ''
    return f'''      <a class="al-card" href="{e['href']}">
        <img src="{e['img']}" alt="" width="480" height="270" loading="lazy" decoding="async">
        <div class="al-body">
          <span class="al-tag">{esc(e['tag'])}</span>{meta}
          <h3 class="al-title">{esc(e['title'])}</h3>
        </div>
      </a>'''


def grid(lang):
    return '<div class="al-grid">\n' + '\n'.join(card(e, lang) for e in entries(lang)) + '\n    </div>'


def page(lang):
    U = UI[lang]; L = S[lang]; tp = template(lang)
    cur = f'{SITE}{PFX[lang]}/articles/'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": cur + "#webpage", "url": cur, "name": U['title'], "description": U['desc'], "inLanguage": lang,
         "isPartOf": {"@id": SITE + "/#website"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i, "url": SITE + e['href'], "name": e['title']} for i, e in enumerate(entries(lang), 1)]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": L['home'], "item": SITE + (PFX[lang] or '') + '/'},
            {"@type": "ListItem", "position": 2, "name": U['title']}]}, ORG]}
    h = head(lang, tp, title=f"{U['title']} | {L['brand']}", desc=U['desc'], parts=(), og_img='/images/kawthar/og-part1-' + lang + '.jpg', og_type='website', published='', ld=ld)
    hl = ''.join(f'  <link rel="alternate" hreflang="{l}" href="{SITE}{PFX[l]}/articles/">\n' for l in LANGS) + f'  <link rel="alternate" hreflang="x-default" href="{SITE}/articles/">'
    h = re.sub(r'  <!-- Canonical \+ hreflang -->.*?(?=\n\n  <!-- Open Graph)', f'  <!-- Canonical + hreflang -->\n  <link rel="canonical" href="{cur}">\n{hl}', h, flags=re.S)
    h = h.replace(f'content="{SITE}{PFX[lang]}/articles/{G.SLUG}/"', f'content="{cur}"')
    main = f'''<main>

<section class="al-hero">
  <span class="al-eyebrow">{esc(U['eyebrow'])}</span>
  <h1>{esc(U['h1'])}</h1>
  <p class="al-sub">{esc(U['sub'])}</p>
</section>

<section class="section al-section" aria-label="{esc(U['all'])}">
  <div class="container">
    {grid(lang)}
  </div>
</section>

</main>

'''
    tail = f'\n{tp["footer"]}\n\n<script src="/assets/theme.js"></script>\n<script src="/assets/script.js"></script>\n</body>\n</html>\n'
    path = f'{PFX[lang].lstrip("/")}{"/" if PFX[lang] else ""}articles/index.html'
    open(ROOT + path, 'w', encoding='utf-8').write(h + main + tail)
    return path


def patch_en_index():
    p = ROOT + 'articles/index.html'
    s = open(p, encoding='utf-8').read()
    ents = [e for e in entries('en')]
    by_month = {}
    for e in ents:
        if e['month']: by_month.setdefault(e['month'], []).append(e)
    # 1) month data: keep names/images, replace the invented article lists with the real ones
    def repl(m):
        n = int(m.group(1))
        arts = ',\n        '.join("{ tag: %s, title: %s, href: %s }" % (json.dumps(x['tag']), json.dumps(x['title']), json.dumps(x['href'])) for x in by_month.get(n, []))
        return m.group(0)[:m.start(2) - m.start(0)] + (f"[\n        {arts}\n      ]" if arts else '[]') + m.group(0)[m.end(2) - m.start(0):]
    s = re.sub(r"num: (\d+), en: [^\n]*\n\s*img: '[^']*',\n\s*articles: (\[.*?\n\s*\]|\[\])", repl, s, flags=re.S)
    # 2) cards use the small thumbnails; the 2 MB originals load only when a month is opened
    s = s.replace("'<img class=\"month-card-img\" src=\"' + m.img + '\"", "'<img class=\"month-card-img\" src=\"/images/months/' + (m.num < 10 ? '0' : '') + m.num + '.jpg\"")
    # 3) ?month=N opens that month
    if 'URLSearchParams' not in s:
        s = s.replace("  closeBtn.addEventListener('click', closeModal);", """  closeBtn.addEventListener('click', closeModal);

  /* /articles/?month=3 opens that month's collection (linked from the homepage). */
  try {
    var q = parseInt(new URLSearchParams(location.search).get('month'), 10);
    var mm = MONTHS.filter(function (x) { return x.num === q; })[0];
    if (mm) openModal(mm);
  } catch (e) {}""")
    # 4) the full list, below the month grid
    s = re.sub(r'\n<!-- ══ ALL ARTICLES.*?</section>\n', '\n', s, flags=re.S)
    block = f'''
<!-- ══ ALL ARTICLES ═══════════════════════════════════════════ -->
<section class="section al-section" aria-label="{UI['en']['all']}">
  <div class="container">
    <h2 class="section-title dark text-center">{UI['en']['all']}</h2>
    <div class="divider" aria-hidden="true"><span class="divider-gem">◆</span></div>
    {grid('en')}
  </div>
</section>
'''
    s = s.replace('\n<!-- ══ MODAL', block + '\n<!-- ══ MODAL', 1)
    # 5) hreflang for all four index pages
    s = re.sub(r'  <link rel="alternate" hreflang="en"[^\n]*\n  <link rel="alternate" hreflang="x-default"[^\n]*\n',
               ''.join(f'  <link rel="alternate" hreflang="{l}" href="{SITE}{PFX[l]}/articles/">\n' for l in LANGS) + f'  <link rel="alternate" hreflang="x-default" href="{SITE}/articles/">\n', s, count=1)
    open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    patch_en_index()
    for l in ('ar', 'fa', 'ur'): print(page(l))
    print(len(entries('en')), 'entries in en;', {l: len(entries(l)) for l in LANGS})
