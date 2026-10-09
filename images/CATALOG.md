# Image Catalog — Misbah Inc. Website

Add a row here whenever you add a new image. Helps avoid duplicates and makes
it easy to find which image belongs where as the library grows.

| File | Dimensions | Size | Subject / Description | Used In |
|------|-----------|------|-----------------------|---------|
| `lady-khadijah-article.jpg` | 1200 × 760 | 280 KB | AI-generated illustration: Lady Khadijah al-Kubra with Arabic calligraphy "خَدِيجَةُ الْكُبْرَى، أُمُّ الْمُؤْمِنِين". Warm gold/cream tones, heavenly setting. | `index.html` → Featured Article card (right column image) |
| `mosque-madinah-hero.jpg` | 1200 × 675 | 109 KB | Aerial/architectural view of Masjid al-Nabawi, Madinah. Green dome visible. Warm daylight tones. | **Not yet placed** — intended for hero section background or a Madinah-related article |
| `months/01.jpg` … `12.jpg` | 480 × 640 | 22–61 KB | Home "Through the Year" thumbnails, cropped from `month-*.png` | `index.html` and `ar|fa|ur/index.html` |
| `kawthar/part{1,2}-{en,ar,fa,ur}.jpg` | 1400 × 483 / 467 | 138–211 KB | Banners from the Wix Al-Kawthar posts (titles are baked into each language's image) | `articles/al-kawthar/…`, home series card |
| `kawthar/og-part{1,2}-{lang}.jpg` | 1200 × 630 | 135–193 KB | Social-share crops of the banners | OG/Twitter tags on the Al-Kawthar pages |
| `articles/<slug>-<lang>.jpg` | ≤ 1400 w | 50–400 KB | Cover image of each imported Wix article (per language; falls back to the English cover) | `articles/<slug>/` pages |
| `articles/og-<slug>-<lang>.jpg` | 1200 × 630 | ~100–200 KB | Social-share crop of the cover | OG/Twitter tags |
| `articles/thumb-<slug>-<lang>.jpg` | 480 × 270 | ~15–30 KB | Card thumbnail for the articles indexes | `articles/index.html`, `/ar|fa|ur/articles/` |
| `articles/khutbat-al-muttaqin-{1..14}-en.jpg`, `og-…`, `thumb-…`, `khutbat-al-muttaqin-cover-en.jpg` | 1200 × 630 / 480 × 270 | ~50–90 KB | Sermon of Muttaqin covers: series cover and parts 1–13 are the supplied posters (parts: 720 × 1280 portrait banner; og/thumb = letterboxed on a blurred copy); part 14 is a generated card (Pillow) | `articles/khutbat-al-muttaqin/…`, homepage "Latest series" card, articles index |
| `articles/{muharram-safar,ghadir}-booklets-<n>-en.jpg`, `og-…`, `thumb-…`, `articles/<series>/<n>/*.jpg` | banner 720 w / OG 1200 × 630 / thumb 480 × 270 / body ≤ 960 w | 15–120 KB each | Booklet covers and the illustrations and Arabic-line crops extracted from the PDF booklets (build_booklets.py) | `articles/muharram-safar-booklets/…`, `articles/ghadir-booklets/…` |

---

## Naming conventions

- All lowercase, words separated by hyphens: `subject-description.jpg`
- Include a hint of the subject and its role: `lady-khadijah-article`, `mosque-madinah-hero`
- JPEG for photos, PNG only if transparency is needed
- Target: ≤ 150 KB for article cards, ≤ 200 KB for hero/full-width images
- Recommended dimensions: 1200 × 760 px for article cards (matches the 600 × 380 card box at 2×), 1200 × 675 px for 16:9 hero banners

## images/topics/ (homepage Topics cards, 640×360, made from existing images)
| File | Source | Used in |
|---|---|---|
| al-kawthar.jpg | kawthar/part1-en.jpg (letterboxed) | homepage Topics |
| lady-khadijah.jpg | lady-khadijah-article.jpg (crop) | homepage Topics |
| imam-hussain.jpg | articles/morning-and-evening-mourning-1-en.jpg | homepage Topics |
| holy-prophet.jpg | articles/virtues-of-the-messenger-of-allah-en.jpg | homepage Topics (fa/ur fallback) |
| khutbat-al-muttaqin.jpg | articles/khutbat-al-muttaqin-cover-en.jpg (centre crop) | homepage Topics (EN only) |
| recognition-of-arbaeen.jpg, morning-and-evening-mourning.jpg | articles/recognition-of-arbaeen-1-en.jpg, articles/morning-and-evening-mourning-2-en.jpg (centre crop) | homepage Topics (EN) |
| muharram-safar-booklets.jpg, ghadir-booklets.jpg, ramadan-booklets.jpg | articles/og-<series>-1-en.jpg (crop) | homepage Topics (EN) |

## images/home/ (homepage section backgrounds)
| File | Size | Source | Used in |
|---|---|---|---|
| muttaqin-section.jpg | 1920 × 900, ~115 KB | text-free strip of the Sermon of Muttaqin poster (city + crowd), sky extended and darkened | `index.html` → "Latest series" section background |
| muttaqin-section-mobile.jpg | 720 × 600, ~36 KB | crop of the same | same, ≤ 700 px wide |
