"""Generate /ar/moonsighting/, /fa/moonsighting/, /ur/moonsighting/ from the English page."""
import re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from formula_translations import FORMULA

BASE   = r"G:\My Drive\Misbah Library\Misbah Website"
SRC    = os.path.join(BASE, "moonsighting", "index.html")

with open(SRC, encoding="utf-8") as f:
    en = f.read()

LANGS = {
    "ar": {
        "dir": "rtl",
        "html_lang": "ar",
        "title": "رؤية الهلال ١٤٤٨ هـ | مسبح",
        "desc":  "توقعات رؤية الهلال لعام ١٤٤٨ هجري — خريطة عالمية بمعيار يالوب",
        "hero_label": "مسبح · التقويم الإسلامي",
        "hero_title": "☽ رؤية الهلال",
        "og_title": "رؤية الهلال ١٤٤٨ هـ | مسبح",
        "nav": """\
    <a href="/" class="nav-logo" aria-label="الصفحة الرئيسية لمصباح إنك.">
      <img src="../../assets/logo.png" alt="Misbah" onerror="this.style.display='none'">
      <span class="nav-logo-text">MISBAH</span>
    </a>
    <button class="hamburger" id="hamburger" aria-label="تبديل القائمة" aria-expanded="false" aria-controls="nav-links">
      <span></span><span></span><span></span>
    </button>
    <div class="nav-links" id="nav-links">
      <a href="/articles" class="nav-link">المقالات</a>
      <a href="https://library.misbah128.com" class="nav-link" target="_blank" rel="noopener">مكتبة مصباح</a>
      <div class="nav-dropdown">
        <button class="nav-link" aria-haspopup="true" aria-expanded="false">
          تواصل
          <svg class="dropdown-arrow" viewBox="0 0 10 6" fill="none" aria-hidden="true">
            <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
        <div class="dropdown-panel" role="menu">
          <a href="/connect#subscribe" class="dropdown-item" role="menuitem">اشترك</a>
          <a href="/connect#contact"   class="dropdown-item" role="menuitem">اتصل بنا</a>
        </div>
      </div>
      <a href="/hijri-calendar/" class="nav-link">التقويم الهجري</a>
      <a href="/ar/moonsighting/" class="nav-link" style="color:var(--gold)">رؤية الهلال</a>
      <a href="/donate" class="nav-link nav-cta">تبرع</a>
      <a href="/about"  class="nav-link">من نحن</a>
      <div class="lang-sw" aria-label="اللغة">
        <a href="/moonsighting/"    hreflang="en">EN</a>
        <a href="/ar/moonsighting/" hreflang="ar" class="active">AR</a>
        <a href="/fa/moonsighting/" hreflang="fa">FA</a>
        <a href="/ur/moonsighting/" hreflang="ur">UR</a>
      </div>
    </div>""",
    },
    "fa": {
        "dir": "rtl",
        "html_lang": "fa",
        "title": "رؤیت هلال ۱۴۴۸ هـ | مصباح",
        "desc":  "پیش‌بینی رؤیت هلال برای سال ۱۴۴۸ هجری — نقشه جهانی با معیار یالوپ",
        "hero_label": "مصباح · تقویم اسلامی",
        "hero_title": "☽ رؤیت هلال",
        "og_title": "رؤیت هلال ۱۴۴۸ هـ | مصباح",
        "nav": """\
    <a href="/" class="nav-logo" aria-label="صفحه اصلی مصباح اینک.">
      <img src="../../assets/logo.png" alt="Misbah" onerror="this.style.display='none'">
      <span class="nav-logo-text">MISBAH</span>
    </a>
    <button class="hamburger" id="hamburger" aria-label="نمایش منو" aria-expanded="false" aria-controls="nav-links">
      <span></span><span></span><span></span>
    </button>
    <div class="nav-links" id="nav-links">
      <a href="/articles" class="nav-link">مقالات</a>
      <a href="https://library.misbah128.com" class="nav-link" target="_blank" rel="noopener">کتابخانه مصباح</a>
      <div class="nav-dropdown">
        <button class="nav-link" aria-haspopup="true" aria-expanded="false">
          ارتباط
          <svg class="dropdown-arrow" viewBox="0 0 10 6" fill="none" aria-hidden="true">
            <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
        <div class="dropdown-panel" role="menu">
          <a href="/connect#subscribe" class="dropdown-item" role="menuitem">اشتراک</a>
          <a href="/connect#contact"   class="dropdown-item" role="menuitem">تماس با ما</a>
        </div>
      </div>
      <a href="/hijri-calendar/" class="nav-link">تقویم هجری</a>
      <a href="/fa/moonsighting/" class="nav-link" style="color:var(--gold)">رؤیت هلال</a>
      <a href="/donate" class="nav-link nav-cta">کمک مالی</a>
      <a href="/about"  class="nav-link">درباره ما</a>
      <div class="lang-sw" aria-label="زبان">
        <a href="/moonsighting/"    hreflang="en">EN</a>
        <a href="/ar/moonsighting/" hreflang="ar">AR</a>
        <a href="/fa/moonsighting/" hreflang="fa" class="active">FA</a>
        <a href="/ur/moonsighting/" hreflang="ur">UR</a>
      </div>
    </div>""",
    },
    "ur": {
        "dir": "rtl",
        "html_lang": "ur",
        "title": "رؤیت ہلال ١٤٤٨ ہجری | مصباح",
        "desc":  "١٤٤٨ ہجری کے لیے چاند نظر آنے کی پیش گوئی — یالوپ معیار کے ساتھ عالمی نقشہ",
        "hero_label": "مصباح · اسلامی تقویم",
        "hero_title": "☽ رؤیت ہلال",
        "og_title": "رؤیت ہلال ١٤٤٨ ہجری | مصباح",
        "nav": """\
    <a href="/" class="nav-logo" aria-label="مصباح انک. ہوم پیج">
      <img src="../../assets/logo.png" alt="Misbah" onerror="this.style.display='none'">
      <span class="nav-logo-text">MISBAH</span>
    </a>
    <button class="hamburger" id="hamburger" aria-label="مینو کھولیں" aria-expanded="false" aria-controls="nav-links">
      <span></span><span></span><span></span>
    </button>
    <div class="nav-links" id="nav-links">
      <a href="/articles" class="nav-link">مضامین</a>
      <a href="https://library.misbah128.com" class="nav-link" target="_blank" rel="noopener">مصباح لائبریری</a>
      <div class="nav-dropdown">
        <button class="nav-link" aria-haspopup="true" aria-expanded="false">
          رابطہ
          <svg class="dropdown-arrow" viewBox="0 0 10 6" fill="none" aria-hidden="true">
            <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
        <div class="dropdown-panel" role="menu">
          <a href="/connect#subscribe" class="dropdown-item" role="menuitem">سبسکرائب</a>
          <a href="/connect#contact"   class="dropdown-item" role="menuitem">ہم سے رابطہ</a>
        </div>
      </div>
      <a href="/hijri-calendar/" class="nav-link">ہجری تقویم</a>
      <a href="/ur/moonsighting/" class="nav-link" style="color:var(--gold)">رؤیت ہلال</a>
      <a href="/donate" class="nav-link nav-cta">چندہ دیں</a>
      <a href="/about"  class="nav-link">ہمارے بارے میں</a>
      <div class="lang-sw" aria-label="زبان">
        <a href="/moonsighting/"    hreflang="en">EN</a>
        <a href="/ar/moonsighting/" hreflang="ar">AR</a>
        <a href="/fa/moonsighting/" hreflang="fa">FA</a>
        <a href="/ur/moonsighting/" hreflang="ur" class="active">UR</a>
      </div>
    </div>""",
    },
}

# Regex: match the existing nav inner content
NAV_RE = re.compile(r'(<nav class="nav-inner"[^>]*>)(.*?)(</nav>)', re.DOTALL)
# Match <html ...>
HTML_RE = re.compile(r'<html([^>]*)>')
# Match hero elements
HERO_LABEL_RE = re.compile(r'(<div class="nm-hero-label">)(.*?)(</div>)')
HERO_TITLE_RE = re.compile(r'(<h1 class="nm-hero-title">)(.*?)(</h1>)')
# Match <title>
TITLE_RE = re.compile(r'<title>(.*?)</title>')
# Meta description
DESC_RE  = re.compile(r'(<meta name="description" content=")([^"]*?)(")')
# og:title
OG_TITLE_RE = re.compile(r'(<meta property="og:title" content=")([^"]*?)(")')
# Asset paths: need to go up two levels from /xx/moonsighting/
ASSET_RE = re.compile(r'(src|href)="../assets/')
MAP_SRC_RE = re.compile(r"'/moonsighting/maps/")

for lc, cfg in LANGS.items():
    html = en

    # Fix <html> tag
    html = HTML_RE.sub(f'<html lang="{cfg["html_lang"]}" dir="{cfg["dir"]}">', html, count=1)

    # Fix asset paths (../../ instead of ../)
    html = html.replace('src="../assets/', 'src="../../assets/')
    html = html.replace('href="../assets/', 'href="../../assets/')

    # Fix JS/CSS links
    html = html.replace("src='../assets/", "src='../../assets/")
    html = html.replace("href='../assets/", "href='../../assets/")

    # Fix map PNG path (absolute, no change needed)

    # Replace nav
    html = NAV_RE.sub(lambda m: m.group(1) + '\n' + cfg['nav'] + '\n  ', html, count=1)

    # Hero
    html = HERO_LABEL_RE.sub(lambda m: m.group(1) + cfg['hero_label'] + m.group(3), html, count=1)
    html = HERO_TITLE_RE.sub(lambda m: m.group(1) + cfg['hero_title'] + m.group(3), html, count=1)

    # Meta
    html = TITLE_RE.sub(f'<title>{cfg["title"]}</title>', html, count=1)
    html = DESC_RE.sub(lambda m: m.group(1) + cfg['desc'] + m.group(3), html, count=1)
    html = OG_TITLE_RE.sub(lambda m: m.group(1) + cfg['og_title'] + m.group(3), html, count=1)

    # canonical
    html = re.sub(r'<link rel="canonical" href="[^"]*"',
                  f'<link rel="canonical" href="https://misbah128.com/{lc}/moonsighting/"', html)

    # Replace formula section with translated version
    FORMULA_RE = re.compile(
        r'<div class="nm-formula">.*?</div><!--\s*/nm-formula\s*-->',
        re.DOTALL)
    if lc in FORMULA:
        html = FORMULA_RE.sub(FORMULA[lc].strip(), html, count=1)

    # Output
    out_dir = os.path.join(BASE, lc, "moonsighting")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Written: {out_path}  ({len(html)//1024}KB)")

print("Done.")
