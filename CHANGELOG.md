# Changelog

All notable changes to the Misbah Inc. website are recorded here.
Format: `## [Date] — Summary` followed by bulleted details.

---

## [2026-09-01] — Moonsighting map overhaul

- **2D latitude-corrected visibility gradient** — replaced flat vertical bands with per-row canvas computation using solar declination + day-length formula, producing correct S-shaped curved bands matching moonsighting.com style
- **Conjunction Night picker** — added ☽₀/☽₁/☽₂ three-button night selector; `nightOff` parameter added to `showMonthMap()` so all region cards and the gradient update together
- **Natural Earth 110m country outlines** — replaced hand-crafted approximate polygons with proper 177-country SVG paths generated from Natural Earth GeoJSON; eliminates wrong circles/blobs for islands
- **Map land fill** — increased opacity to `rgba(0,4,2,0.55)` so land is clearly visible (dark) against the colored gradient; stroke `rgba(220,210,175,0.75)`
- **Nav alignment fix** — moonsighting page `nav-container` corrected to `nav-inner` to match homepage placement

---

## [2026-09-01] — Crescent Moonsighting dedicated page

- **`/moonsighting/` page** created as a dedicated Hijri crescent visibility tool for 1448 AH
  - 12-month picker (Muharram → Dhu al-Hijjah) powered by Meeus algorithm new-moon computation
  - Color-coded SVG world map (9 regions) with improved geographic detail
  - Region breakdown grid with lunar age, visibility label, and predicted date per region
  - Full formula article explaining Meeus algorithm, Yallop criterion, and regional gradient
  - Religious disclaimer (astronomical prediction only — not a fatwa)
- **"Moonsighting" nav link** added to: EN homepage, Hijri Calendar page, AR/FA/UR homepages (translated: رؤية الهلال / رؤیت هلال / رؤیت ہلال)
- **Visibility bug fixed** in `assets/moonsighting.js`: corrected `utcH+24/+48` offset (was checking days 2–3 instead of 1–2, causing always-green map)
- Updated visibility thresholds to 17 h (not visible) / 26 h (binoculars) matching standard criteria
- Moonsighting placeholder removed from homepage (moved to dedicated page)

---

## [2026-09-01] — Domain change + full multilingual homepages

- **Domain renamed** from `misbah-inc.com` to `misbah128.com` — CNAME updated, all HTML meta tags and JSON-LD updated across every page
- **Arabic homepage** (`/ar/index.html`) — replaced "coming soon" placeholder with full Arabic translation (RTL, Amiri font, all sections translated)
- **Farsi homepage** (`/fa/index.html`) — replaced "coming soon" placeholder with full Farsi translation; eyebrow slogan set to "روزگارم با غلامی علی سر می شود"
- **Urdu homepage** (`/ur/index.html`) — replaced "coming soon" placeholder with full Urdu translation; hero title forced to one line via CSS
- **Git repo** initialized and pushed to `github.com/Misbah-inc/misbah-website`; deployed via GitHub Pages

---

## [2026-08-31] — Article page + language scaffolding + calendar label

- **Lady Khadijah article** (`/articles/rabi_al_awwal/index.html`) — full article page built with dark-green hero, TOC, 6 parts, Quranic verse boxes, hadith blocks, 43-source accordion, full SEO
- **Article title block** added in content body (visible below hero) with Arabic subtitle
- **Calendar label** changed from "Events This Month" to "SHIA CALENDAR"
- **Language placeholder pages** created for `/ar/`, `/fa/`, `/ur/` and their article subdirectories with `noindex` and "coming soon" hero
- **SEO** added to all pages: canonical, hreflang, Open Graph, Twitter Card, JSON-LD structured data
- **Hijri calendar page** (`/hijri-calendar/index.html`) — SEO block added
- **`CLAUDE.md`** created documenting full website infrastructure
- **`images/CATALOG.md`** created as image registry

---

## [2026-08-30] — Hero image fix + featured article image

- **Featured image** (`lady-khadijah-article.jpg`) — replaced with correctly-sized 760×920 portrait; old incorrectly-proportioned images deleted
- **CSS fix** — `.featured-img` changed from `min-height` to `aspect-ratio: 1200/760` + `object-fit: cover` to eliminate cropping

---

## [2026-08-29] — Initial build

- Static HTML/CSS/JS site created from scratch
- Homepage with hero, prayer times, Shia calendar, featured article, Morning & Evening Mourning series, YouTube section, donation widget, footer
- Hijri calendar page with full month grid, event dots, events list
- Navigation with dropdown, hamburger mobile menu, language switcher
- CSS design system: dark green (#0e1f0e), gold (#c9a46b), Cinzel + Inter + Amiri fonts
- `.gitignore` added

---
