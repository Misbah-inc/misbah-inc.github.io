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
