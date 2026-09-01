# CLAUDE.md — Misbah Inc. Website

Claude Code instructions for working with this repository.

---

## Project Overview

**misbah128.com** — static HTML/CSS/JS website for Misbah Inc., a U.S.-based Shia Islamic nonprofit.

- Hosted: **GitHub Pages** (branch: `main`, root folder)
- CDN/DNS: **Cloudflare** (proxied, SSL Full)
- Custom domain: **misbah128.com** (CNAME file at repo root)
- No build step, no framework — pure static files

---

## Directory Structure

```
/                          ← English root (index.html = homepage)
├── index.html             ← Homepage (EN)
├── CNAME                  ← GitHub Pages custom domain
├── assets/
│   ├── style.css          ← All site-wide CSS (CSS variables, components)
│   ├── script.js          ← All site-wide JS (nav, prayer times, dropdowns)
│   ├── logo.png           ← Main nav logo
│   ├── logo-barak.png     ← Hero calligraphy (top)
│   ├── logo-ajjil.png     ← Hero calligraphy pair (left)
│   └── logo-biymnih.png   ← Hero calligraphy pair (right)
├── images/
│   ├── CATALOG.md         ← Image registry (add a row for every new image)
│   ├── lady-khadijah-article.jpg   ← 760×920, 280 KB — Lady Khadijah article card
│   └── mosque-madinah-hero.jpg     ← 1200×675, 109 KB — Hero/Madinah article (unused)
├── hijri-calendar/
│   └── index.html         ← Hijri calendar page (EN)
├── articles/
│   └── rabi_al_awwal/
│       └── index.html     ← Article: Virtues of Lady Khadijah (EN)
├── ar/                    ← Arabic (RTL, lang="ar")
│   ├── index.html         ← Arabic homepage placeholder (noindex until translated)
│   └── articles/
│       └── rabi_al_awwal/
│           └── index.html ← Arabic article placeholder
├── fa/                    ← Farsi (RTL, lang="fa")
│   ├── index.html
│   └── articles/rabi_al_awwal/index.html
└── ur/                    ← Urdu (RTL, lang="ur")
    ├── index.html
    └── articles/rabi_al_awwal/index.html
```

---

## URL Scheme

| Page                    | English URL                                    | Arabic                              | Farsi                              | Urdu                              |
|-------------------------|------------------------------------------------|-------------------------------------|------------------------------------|-----------------------------------|
| Homepage                | `/`                                            | `/ar/`                              | `/fa/`                             | `/ur/`                            |
| Hijri Calendar          | `/hijri-calendar/`                             | (not yet)                           | (not yet)                          | (not yet)                         |
| Lady Khadijah article   | `/articles/rabi_al_awwal/`                     | `/ar/articles/rabi_al_awwal/`       | `/fa/articles/rabi_al_awwal/`      | `/ur/articles/rabi_al_awwal/`     |
| Articles index          | `/articles/`                                   | (not yet)                           | (not yet)                          | (not yet)                         |

**Convention:** articles are grouped by Hijri month — `/articles/<hijri_month_key>/`.

---

## CSS Architecture (`assets/style.css`)

### Key CSS variables
```css
--dark-bg:    #0e1f0e    /* page/hero background */
--nav-bg:     #152b15    /* sticky nav */
--dark-green: #1a3d1b    /* primary green */
--gold:       #c9a46b    /* primary gold accent */
--gold-light: #e8d5a3    /* light gold text */
--white:      #ffffff
--max-w:      1200px     /* container max-width */
--nav-h:      64px       /* sticky header height */
```

### Font stack
- **Display/headings:** `'Cinzel'` (Google Fonts) → serif fallback
- **Body:** `'Inter'` (Google Fonts) → system-ui fallback
- **Arabic/Farsi/Urdu:** `'Amiri'` (Google Fonts) → Georgia fallback

### RTL pages
All language pages under `/ar/`, `/fa/`, `/ur/` use `<html lang="XX" dir="rtl">`.
CSS border sides flip: left borders become right borders, etc.

---

## SEO Standards (apply to every page)

Every page must have:
1. `<title>` — unique, ≤60 chars, format: `Page Name | Misbah Inc.`
2. `<meta name="description">` — unique, 140–160 chars
3. `<link rel="canonical">` — absolute URL
4. `<link rel="alternate" hreflang>` — for every language variant that exists
5. Open Graph: `og:type`, `og:url`, `og:title`, `og:description`, `og:image`, `og:locale`
6. Twitter Card: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`
7. JSON-LD structured data:
   - Homepage → `WebSite` + `Organization`
   - Article pages → `Article` + `BreadcrumbList` + `Organization`
   - Other pages → `WebPage` + `BreadcrumbList`

**OG image sizes:**
- Homepage / general: `mosque-madinah-hero.jpg` (1200×675)
- Article pages: use the article's own image

**Organization JSON-LD** (`@id: https://misbah128.com/#organization`) is referenced by all pages — define it fully only on the homepage, reference it elsewhere.

---

## Multilingual Strategy

- Language variants live at `/<lang>/` prefix (e.g., `/ar/`, `/fa/`, `/ur/`)
- Placeholder pages use `<meta name="robots" content="noindex, nofollow">`
- **Remove `noindex` when a page has real translated content**
- hreflang must be added to ALL language variants simultaneously (not just the English page)
- `x-default` always points to the English URL

### Adding a translation
1. User provides translated text
2. Create/update `/<lang>/articles/<month>/index.html` with full content
3. Set `<html lang="XX" dir="rtl">` (Arabic/Farsi/Urdu are RTL)
4. Remove `noindex` meta tag
5. Verify hreflang on all variants point to each other

---

## Adding a New Article

1. Create directory: `articles/<hijri_month_key>/index.html`
2. Copy structure from `articles/rabi_al_awwal/index.html`
3. Add image to `images/` and register in `images/CATALOG.md`
4. Update `images/CATALOG.md` with new image info
5. Add SEO: canonical, hreflang, OG, Twitter, JSON-LD Article
6. Create placeholder pages under `/ar/`, `/fa/`, `/ur/` (noindex)
7. Update homepage featured article card in `index.html`

---

## Prayer Times (`index.html`)

- API: `https://api.aladhan.com/v1/timings` — method `0` = Shia Ithna-Ashari (Jafari) by default
- Reverse geocoding: `https://api.bigdatacloud.net/data/reverse-geocode-client`
- Caches last GPS coords in `localStorage` (`misbah_lat`, `misbah_lon`)
- Method dropdown: user can switch formula; choices in `index.html` `#prayer-method-select`

---

## Hijri Calendar (`hijri-calendar/index.html`)

- Pure JS Hijri–Gregorian conversion (tabular Julian Day Number algorithm) — no library
- Events object hard-coded by Hijri month (1–12)
- To add events: edit the `EVENTS` object in the `<script>` section
- Homepage calendar section uses `tools/update_calendar.py` (requires `hijri-converter` pip package)

---

## Images Policy

- Add every image to `images/CATALOG.md` with: filename, dimensions, size, subject, used-in
- **Target sizes:** article card images ≤ 200 KB; hero images ≤ 150 KB
- **Preferred dimensions:** article cards 760×920 px (matches the `.featured-card` box ratio); hero banners 1200×675 px
- Optimize with Python Pillow: quality 82%, progressive JPEG, max-width 1200 px
- No raw/unoptimized originals in the repo

---

## Deployment

### GitHub Pages
- Repo: `github.com/misbah-inc/misbah-website` (or similar — confirm with user)
- Branch: `main`, deploy from root `/`
- Custom domain set via `CNAME` file + GitHub repo Settings → Pages → Custom domain
- HTTPS enforced via GitHub Pages setting

### Cloudflare
- DNS: CNAME `misbah128.com` → `<github-username>.github.io` (proxied)
- SSL mode: **Full** (not Flexible, not Full Strict)
- Page rules / caching: static assets cached at edge
- After pointing DNS to GitHub Pages, enable "Enforce HTTPS" in GitHub Pages settings

### Deployment workflow
```bash
git add .
git commit -m "describe change"
git push origin main
# GitHub Pages deploys automatically in ~1 minute
```

---

## Tools

| Script | Purpose |
|--------|---------|
| `tools/extract_book.py` | Extract text from Hadith PDFs |
| `tools/build_index.py`  | Build TOC index card for a book |
| `tools/normalize_arabic.py` | Normalize Arabic for search |
| `tools/update_calendar.py` | Update homepage calendar for current Hijri month |

---

## Pending Pages (not yet built)

- `/articles/` — Articles index / listing page
- `/donate/` — Donation page
- `/connect/` — Subscribe + contact form
- `/about/` — About Misbah Inc.
- Multilingual homepages: full translated content for `/ar/`, `/fa/`, `/ur/`
