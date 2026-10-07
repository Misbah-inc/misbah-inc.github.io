# Wix blog → article pages

Imports posts from the Wix blog (misbah-inc.com) as static pages in all languages that exist. **Text is copied verbatim — never reworded or translated.**

Run from the repo root. Needs Python 3 + Pillow. Downloaded pages live in `work/` (gitignored); `catalog.json` (tracked) records what has been imported.

1. Wix lists every post in `https://www.misbah-inc.com/blog-posts-sitemap.xml`; each English post page links its ar/fa/ur translations as `<link rel="alternate" hreflang="ar-ae" …>`.
2. **Fetch slowly** (one page every ~4 s). Wix answers a burst with HTTP 429 / "Checking Your Request" — `fetch_tr.py` backs off and retries.
3. Edit/add a batch JSON (`{"slug", "wix", "month"}`; `month` = Hijri month 1–12 or null) and run `python3 tools/wix_import/run_batch.py tools/wix_import/batch1.json`.
4. `python3 tools/wix_import/build_index.py` (articles index in 4 languages + the English month modal), then add the sitemap entries, then `python3 tools/wix_import/check_site.py`.
5. Series (several parts) use `build_kawthar.py` as the model. Update `catalog.json`/CHANGELOG, commit.

The scripts were written for the Al-Kawthar series first; per-series values (video IDs, titles) are hard-coded in `gen_kawthar.py`.
