# CLAUDE.md — Misbah Inc. Website

Claude Code instructions for working with this repository.

---

## Standing rule: SEO in every language

**Every change to this website must be SEO-friendly, in all four languages (English, Arabic, Farsi, Urdu).** This is not a final polish step. It applies to every new page, edit, section, link, image and removal.

- A change that touches a page's English version must also keep the `/ar/`, `/fa/` and `/ur/` versions correct: `lang`/`dir`, title, description, canonical, hreflang (all variants, `x-default` = English), Open Graph, Twitter Card, JSON-LD and `alt` text, each written in that page's language.
- Work through the **SEO Checklist** below for every page you create or change, and update `sitemap.xml` (with its hreflang links) in the same change.
- When a page is removed or moved, remove it from the sitemap and fix every link and hreflang that pointed at it.
- Where a translation does not exist yet, keep the placeholder `noindex` rather than publishing an empty or machine-filled page.
- Do not state something is finished if the SEO items for any language are unverified. Say which ones are.

---

## Project Overview

**https://article.misbah-inc.com** — static HTML/CSS/JS articles site for Misbah Inc., a U.S.-based Shia Islamic nonprofit. (Formerly misbah128.com, which is **retired — no redirect**.)

- **Articles only (Oct 2026).** Hijri calendar, moonsighting, prayer times and donate were removed; those live in the app.
- Working copy: `~/Developer/misbah-website` (git). The Drive copy is an archive. Remote: `Misbah-inc/misbah-inc.github.io`.
- **Hosting: S3 + CloudFront on AWS** (same pattern as `library.misbah-inc.com`; see `Library/_translation-kit/DEPLOY.md`). DNS stays at **Wix** — one CNAME. `git push` only records history; `tools/deploy_s3.py` publishes.
- The main company site is Wix (`misbah-inc.com`) and is not touched by this repo.
- No build step, no framework — pure static files.
- Every canonical, hreflang, OG, JSON-LD and sitemap URL uses `https://article.misbah-inc.com/…`; the Library link is `https://library.misbah-inc.com`.

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
| Lady Khadijah article   | `/articles/rabi_al_awwal/`                     | `/ar/articles/rabi_al_awwal/`       | `/fa/articles/rabi_al_awwal/`      | `/ur/articles/rabi_al_awwal/`     |
| Al-Kawthar series       | `/articles/al-kawthar/` (+ `part-1/`, `part-2/`) | `/ar/articles/al-kawthar/…`         | `/fa/articles/al-kawthar/…`        | `/ur/articles/al-kawthar/…`       |
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

## SEO Checklist (apply to every page)

Run through this checklist whenever creating or updating any page.

### 1. Basic meta tags
- [ ] `<title>` — unique, ≤60 chars, format: `Page Name | Misbah Inc.`
- [ ] `<meta name="description">` — unique, 140–160 chars, no keyword stuffing
- [ ] `<meta name="robots">` — omit on indexable pages; add `noindex, nofollow` on placeholders only
- [ ] `<html lang="XX" dir="ltr/rtl">` — correct language code and direction

### 2. Canonical + hreflang
- [ ] `<link rel="canonical" href="https://misbah128.com/path/">` — absolute URL, trailing slash consistent
- [ ] `<link rel="alternate" hreflang="en" href="...">` — for every language variant that exists
- [ ] `<link rel="alternate" hreflang="ar" href="...">` — Arabic variant
- [ ] `<link rel="alternate" hreflang="fa" href="...">` — Farsi variant
- [ ] `<link rel="alternate" hreflang="ur" href="...">` — Urdu variant
- [ ] `<link rel="alternate" hreflang="x-default" href="...">` — always points to English URL
- [ ] hreflang set on ALL language variants simultaneously (not just the English page)

### 3. Open Graph
- [ ] `og:type` — `website` for homepage/landing, `article` for article pages
- [ ] `og:url` — canonical absolute URL
- [ ] `og:site_name` — `Misbah Inc.`
- [ ] `og:title` — same as `<title>` (can be slightly longer, ≤95 chars)
- [ ] `og:description` — same as meta description
- [ ] `og:image` — absolute URL, minimum 1200×630 px
- [ ] `og:image:width` + `og:image:height` — explicit dimensions
- [ ] `og:locale` — `en_US` / `ar_AR` / `fa_IR` / `ur_PK`
- [ ] Article pages only: `article:published_time`, `article:author`, `article:section`, `article:tag`

### 4. Twitter Card
- [ ] `twitter:card` — `summary_large_image`
- [ ] `twitter:title`
- [ ] `twitter:description`
- [ ] `twitter:image` — same as og:image

### 5. JSON-LD Structured Data
- [ ] Homepage → `WebSite` + `Organization` (full definition)
- [ ] Article pages → `Article` + `BreadcrumbList` + `Organization` (reference only)
- [ ] Other pages → `WebPage` + `BreadcrumbList`
- [ ] All `@id` values use absolute URLs with fragment (`#website`, `#organization`, `#article`)
- [ ] `Organization @id` (`https://misbah128.com/#organization`) — define fully on homepage, reference elsewhere

### 6. Images
- [ ] Every `<img>` has a descriptive `alt` attribute
- [ ] Hero/featured images have `loading="lazy"` and `decoding="async"` (except above-the-fold)
- [ ] OG image is 1200×630 px minimum (article cards: 760×920 px is acceptable — crop handled by platforms)

### 7. Page performance basics
- [ ] Google Fonts loaded via `<link rel="preconnect">` + single stylesheet URL
- [ ] No render-blocking scripts (all `<script>` at bottom of `<body>`)
- [ ] Images optimized: ≤200 KB for article cards, ≤150 KB for heroes

### 8. After publishing
- [ ] Add entry to `CHANGELOG.md` with date and reason
- [ ] Add/update row in `images/CATALOG.md` if new image added
- [ ] Remove `noindex` when a placeholder page gets real translated content
- [ ] Commit and push via GitHub Desktop

---

**OG image reference:**
- Homepage / general pages: `mosque-madinah-hero.jpg` (1200×675)
- Article pages: use the article's own featured image

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



## Images Policy

- Add every image to `images/CATALOG.md` with: filename, dimensions, size, subject, used-in
- **Target sizes:** article card images ≤ 200 KB; hero images ≤ 150 KB
- **Preferred dimensions:** article cards 760×920 px (matches the `.featured-card` box ratio); hero banners 1200×675 px
- Optimize with Python Pillow: quality 82%, progressive JPEG, max-width 1200 px
- No raw/unoptimized originals in the repo

---

## Deployment

Status: **AWS not yet set up** (bucket, certificate, CloudFront). Steps, in order: private S3 bucket → least-privilege deploy policy → ACM certificate (us-east-1) for `article.misbah-inc.com` validated by a Wix CNAME → CloudFront distribution with Origin Access Control, the `rewrite-index` function (directory URLs → `index.html`) and 403/404 → `/404.html` → verify on the `*.cloudfront.net` address → one Wix CNAME `article` → `<distribution>.cloudfront.net`.

```bash
python3 tools/deploy_s3.py --bucket <bucket> --dist <DISTRIBUTION_ID> --dry-run
python3 tools/deploy_s3.py --bucket <bucket> --dist <DISTRIBUTION_ID>
git add -A && git commit && git push      # history only; does not publish
```

- Run the deploy from the local clone, never from Google Drive. AWS credentials live in `~/.aws/credentials` on each machine, never in the repo or on Drive, and never in chat.
- The script refuses to run unless `index.html`, `sitemap.xml`, `assets/style.css` and `articles/al-kawthar/` exist, because it uses `--delete`.
- GitHub Pages is no longer the host. Rollback = remove the Wix CNAME.

---

## Tools

| Script | Purpose |
|--------|---------|
| `tools/extract_book.py` | Extract text from Hadith PDFs |
| `tools/build_index.py`  | Build TOC index card for a book |
| `tools/normalize_arabic.py` | Normalize Arabic for search |
| `tools/update_calendar.py` | *(obsolete — the homepage calendar was removed)* |

---

## Series and the Wix import

Articles also come as **series** (several parts, one page listing them): `articles/<series>/` is the landing page, `articles/<series>/part-N/` the parts, mirrored under `/ar|fa|ur/`. Al-Kawthar (2 parts, 4 languages) is the first.

- **Source of truth for older posts is the Wix blog** at misbah-inc.com. `https://www.misbah-inc.com/blog-feed.xml` lists every post (titles, descriptions, per-language URLs `/ar|fa|ur/post/…`); the post page's `<article>` holds the full text. Copy the text **verbatim** — never reword, restyle or "tidy" it. Each language is built from its own post; never translate to fill a gap.
- Each Wix post has one YouTube video; its ID is in the `i.ytimg.com/vi/<id>/` thumbnail URL on the post page. Embed it click-to-load through `youtube-nocookie.com` (see `.kw-video*` in `style.css`), with `VideoObject` JSON-LD.
- Pages are generated from each language's Khadijah article (head styles, nav, footer), so a restyle there should be mirrored. The series pages are static HTML like everything else — adding a part means adding its page in all four languages, the sitemap entries, and a link from the series page.
- Homepage "Through the Year" cards: when an article is published for a Hijri month, turn that month's `year-card--soon` `<div>` into a `year-card--live` `<a>` in all four homepages.
- `images/months/` = 480×640 thumbnails for those cards; `images/kawthar/` = banners and 1200×630 social crops. Register new images in `images/CATALOG.md`.

---

## Pending Pages (not yet built)

- `/articles/` — Articles index / listing page
- `/connect/` — Subscribe + contact form
- `/about/` — About Misbah Inc.
- Multilingual homepages: full translated content for `/ar/`, `/fa/`, `/ur/`
