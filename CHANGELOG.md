# Changelog

All notable changes to the Misbah Inc. website are recorded here.
Format: `## [Date] — Summary` followed by bulleted details.

---

## [2026-10-16] — New article: Lady Zaynab's resemblance to Lady Khadijah; Shia-calendar card off the homepage

- `/articles/resemblance-of-lady-zaynab-to-lady-khadijah/` (+ `/ar/`, `/fa/`, `/ur/`): the special-edition post of 16 Oct 2026 (the Prophet's words at Lady Zaynab's birth and naming — «she is like Khadijah al-Kubra»), word for word from the four channels (fa #22964, en #23758, ar #499, ur #538). Filed under Jumada al-Awwal, type *Article*, tags Lady Zaynab, Lady Khadijah, the Holy Prophet; the narrations are quote blocks, the source (*al-Khasa'is al-Zaynabiyyah*, p. 60) a Source list. Heading = the editor's special-edition hashtag. Picture: the site's default logo card until its pictures arrive. Generator: `tools/wix_import/build_zaynab_khadijah.py [wide [square]]`.
- The homepage **Shia Calendar — Month of Jumada al-Ula** card was removed (all four languages); the Jumada al-Ula article itself stays online. `build_home_featured.py` keeps `occasions()` if it should come back.

## [2026-10-16] — Zaynab/Khadijah article: pictures, and on the homepage

- The article now has its pictures: the wide poster as banner / share image / thumbnail, the square one for phones (`images/zaynab-khadijah-poster-*.jpg`).
- **Featured** (homepage, four languages): the article is the first card of the "More on Lady Khadijah (p)" row, followed by the three series; the row is four across on wide screens, two on tablets, one on phones. Card picture `images/home/feat-zaynab-khadijah-v1.jpg` (square).

## [2026-10-25] — "What's new" line on the homepages

- A small line under the social icons on the four homepages: a *New* tag and one sentence at a time, fading to the next every ~6.5 s (six updates now: Spotify, Zaynab–Khadijah Part 7, Muttaqin Part 3 in ar/fa/ur, the Musibat al-Zahra series, Kawthar Parts 3–5, the text-size buttons). Each sentence links to its page when it has one. It stops while hovered / focused or with its pause button, does not rotate at all for visitors who prefer reduced motion, and shows the newest sentence without JavaScript. The change from one sentence to the next is a quick cross-fade (0.3 s out, 0.3 s in; a new sentence every 1.65 s, so each one stands still for 1 s, as the editor asked — hovering or focusing pauses it). To announce something: add an entry at the top of `ITEMS` in `tools/wix_import/build_whats_new.py` (sentence in each language + optional path) and run it; trim old entries. The sentences are my wording (not reviewed by a native speaker). Styles `.wn*` in `style.css`, rotation at the end of `script.js`.

## [2026-10-25] — Zaynab/Khadijah series: Part 7

- **Part 7** (posted 24 Oct 18:38 UTC; fa #23051, en #23844 + #23845 — the English post continued in a second message —, ar #582, ur #624): sections 7 (modesty, chastity and veiling), 8 (precedence in faith and wilayah; deputyship and wasiyya) and 9 (Mother of the Believers and Mother of Calamities), each Arabic quotation in a box with its translation and source; the post's own picture as banner. Series page, Part 6 ↔ 7 links, sitemap and feed updated. Nothing in Parts 1–6 was edited on the channels (checked). Arabic Part 4 still has no post. The 24 Oct posts tagged #Fatimiyya / martyrdom of Zahra are a different topic and were not added.

## [2026-10-24] — Spotify menu next to Telegram (homepage hero and every footer)

- A Spotify icon with a two-entry menu — **Misbah Podcast** (open.spotify.com/show/1T4EHdbm7O0UhUMxXJ0y9w) and **Kawthar Series** (…/1uIz5DDmEnCKS1OtrTsQFv) — sits right after Telegram in the four homepages' icon row and in the footer social row of all pages; same hover / tap behaviour as the WhatsApp and Telegram menus. Entry names: Misbah Podcast / «بودكاست مصباح» / «پادکست مصباح» / «مصباح پوڈکاسٹ» and the Kawthar series name in each language (taken from the channels' own hashtags and the series titles). Added by `fix_header.py` (idempotent, runs on every build). The same menu is in `wix/hero-section.html` for the Wix site.

## [2026-10-24] — Sermon of Muttaqin, Part 3 in Farsi, Arabic and Urdu

- `/fa/`, `/ar/`, `/ur/articles/khutbat-al-muttaqin/3/` — «مَشْيُهُمُ التَّوَاضُعُ» (Malik al-Ashtar and the man who threw clay at him in Kufa), word for word from the posts of 20 Oct (fa #23007, ar #540, ur #584; `muttaqin_src/part03.<lang>.txt`); only the Arabic line is a quotation box (the Arabic text's narrative lines are fully vowelled, so the vowel heuristic is off for this part); the *Bihar al-Anwar* reference is in the Sources list. Same video as the English page; the three series pages now list Parts 1–3; English Part 3 and the series page link all four languages. Titles are the posts' own subtitle lines. Part 15 (English only) still waits for translations.

## [2026-10-24] — Kawthar of the Qur'an: Parts 3–5 (from the channels)

- `/…/articles/al-kawthar/part-3/`, `part-4/`, `part-5/` — the weekly episodes after Part 2: **3** (7–10 Oct: the origin of goodness, self-knowledge, the Prophet's Mi'raj apple, Fatimah as a heavenly maiden in human form), **4** (14–18 Oct), **5** (21–23 Oct: the Alawi & Fatimi reality of Imam al-Ridha; **no Urdu Part 5 yet**). Posts: fa #22905/#22952/#23035, en #23691(+#23692)/#23747/#23821, ar #455/#497/#577, ur #497/#560. Word for word; each post's own portrait picture is the banner (the channels' 450×800 preview, enlarged); the Arabic originals sit in boxes with their translations; the 📚 sources (and the Resources message of the English Part 3) form a collapsible Sources list. The old Parts 1–2 pages were not rebuilt: Part 2 got a "next" link, the series page the new cards and structured data, the feed the new parts, the Articles list the new date. The episodes' YouTube Shorts are **not** embedded (the links in the channel are inconsistent; Parts 1–2 keep theirs). Generator `tools/wix_import/build_kawthar_tg.py`.

## [2026-10-24] — New series: Musibat al-Zahra (#مصیبة_الزهراء #فاطمیه), four languages; Fatimiyya block first on the homepage

- `/…/articles/musibat-al-zahra/` — the Friday posts of the Fatimiyya season, 4 parts × 4 languages: **1** The Silent Revolution (2 Oct; fa #22856, en #23624, ar #397, ur #429), **2** He Weeps — Not for His Kin (9 Oct; fa #22907, en #23695 + #23696, ar #444, ur #480 + #481 — the en and ur posts were split in two messages), **3** The Grave Hidden from the Impure (16 Oct), **4** Which House Was Burned? (23 Oct). Text word for word; each post's title line is the page heading; the ⚜️ / ✨ « … » lines are quotation boxes; the (1)(2)… are footnote links into a collapsible Sources list (the post's 📚 block); each post's own square picture is the banner (800×800) with a letterboxed share image / thumbnail. Filed under Jumada al-Awwal, series, tags Lady Fatimah al-Zahra + Mourning. The 2023 posts with the same hashtags are an older cycle and are not included. Generator `tools/wix_import/build_musibat.py`. Series name and the one-line description in each language are my wording (unreviewed).
- **Homepage, all four languages:** a new first block (before Featured) for the Fatimiyya days — "Fatimiyya Days 1448" (ایام فاطمیه ۱۴۴۸ / الأيام الفاطمية ١٤٤٨ / ایامِ فاطمیہ ۱۴۴۸), the series card with the Part 4 picture and a Read-the-series button (`build_home_featured.py` → `fatimiyya()`).

## [2026-10-24] — Zaynab/Khadijah series: Parts 4–6 (their own pictures)

- Found by the channels' hashtags: **Part 4** (19 Oct: Companionship, solace and support for the Wali of God — fa #22994, en #23786, ur #571; **no Arabic post was published**, so `/ar/` has no Part 4 and its series page lists 1, 2, 3, 5, 6), **Part 5** (21 Oct: sacrificing wealth and all one has for wilayah — fa #23023, en #23818, ar #556, ur #600), **Part 6** (23 Oct: sections 5 and 6, coming to the aid of the Wali of God, and knowledge — fa #23043, en #23836, ar #573, ur #618). Each has the photo from its channel post as banner / share image / thumbnail (800×450 Telegram preview, enlarged; same picture in every language). Word for word; the Arabic originals sit in boxes with their translations and sources, the numbered section headings are headings. `parse3()` was generalised for these posts; the page set per part follows the languages that exist (hreflang, catalogue, sitemap, prev/next links skip the gap). The 16 Oct 00:45 posts (Hussainiyya / luminous appearance) are a different topic and are not part of the series.

## [2026-10-18] — Zaynab/Khadijah series: Part 3 (four languages)

- `/…/articles/resemblance-of-lady-zaynab-to-lady-khadijah/3/` — «بخشی از وجوه شباهت هر دو خاتون» / "Some Aspects of Resemblance Between the Two Ladies" (posts of 18 Oct 20:47 UTC: fa #22988, en #23780, ar #522, ur #565). Word for word (only the stray `**` markdown marks dropped): 1. the title «Kubra» with both ladies' lists of titles; 2. intellect and wisdom, each Arabic quotation in a box with its translation and source. The Arabic post has no translations. Own picture from the photo post (two veiled figures in a house and in a camp; 800×450 from the Telegram preview, enlarged like Part 2's), same in all languages. Series page, Part 2 ↔ Part 3 navigation, catalogue, sitemap, feed updated. `build_zaynab_khadijah.py`: `parse3()`.

## [2026-10-17] — Zaynab/Khadijah series: Part 2 has its own picture

- Part 2's banner, social image and card thumbnail are now the picture from the channels' photo post of 17 Oct (two ladies in prayer, bright rays — one set in a house, one in a camp), the same in every language. The Telegram web preview only exposes it at 800×450, so it is enlarged to the 1600-px banner width (a little soft); send the original file for a sharper banner. No square version, so phones get the wide one. Series picture (Part 1's) is unchanged. `PARTS[n]['image']` in `build_zaynab_khadijah.py`.

## [2026-10-17] — Zaynab/Khadijah series: Part 2 (four languages)

- `/…/articles/resemblance-of-lady-zaynab-to-lady-khadijah/2/` — «خدیجة و أین مثل خدیجة؟ / زینب و ما زینب؟» (posts of 17 Oct 21:22 UTC: fa #22982, en #23775, ar #516, ur #556). Word for word: the two Arabic title lines, three sections (Khadijah — the Prophet's words recorded by Umm Salamah; Zaynab — the scholars' words; the Infallibles' expressions about Lady Zaynab), the hadiths in Arabic boxes, their translations as quotations (ar has none in the post), each 📚 source line kept right under its hadith. Series page, Part 1 → Part 2 navigation, catalogue, sitemap, feed updated; Part 2 uses the series picture. `build_zaynab_khadijah.py` now builds all parts (`PARTS`).

## [2026-10-17] — The Zaynab/Khadijah article is now a series, with this text as Part 1

- `/…/articles/resemblance-of-lady-zaynab-to-lady-khadijah/` is now the **series page** (all four languages; it keeps the old address) and the text is **Part 1** at `/…/1/` (heading "<series title> — Part 1"). New parts: add the posts to `POSTS`-style data in `build_zaynab_khadijah.py` and rebuild. Series description lines in ar/fa/ur are my wording (unreviewed). Filed as a series under Jumada al-Awwal with the same tags. The homepage Featured card now reads Series with the series description. Picture files were renamed to `…-1-<lang>.jpg` (banner, og, thumb) and `…-1-mobile.jpg`.

## [2026-10-17] — Zaynab/Khadijah article: the rewritten opening in Arabic, Farsi and Urdu

- The same rewrite (Prophet away travelling, Lady Zaynab (p) still unnamed at that time, Imam Ali's answer, the Prophet hurrying to the house; then the dangling "When Amir al-Mu'minin … came … and said:") is now on the `/ar/`, `/fa/` and `/ur/` pages. These are **my translations of the English text** (each in the register and honorifics of its own post), not reviewed by a native speaker; the Telegram posts keep their original wording.

## [2026-10-17] — Zaynab/Khadijah article (English): the narration's opening rewritten

- English page: the paragraph "It is narrated that when Lady Zaynab (peace be upon her) was born, Amir al-Mu'minin … came to the Prophet and said:" is replaced, at the editor's request, by two paragraphs (the Prophet away travelling, the unnamed baby, Imam Ali's answer, the Prophet hurrying to the house; then "When Amir al-Mu'minin … said:"). The Telegram post keeps its original wording, and the Arabic, Farsi and Urdu pages are unchanged until their wording is supplied (`OVERRIDES` in `build_zaynab_khadijah.py`). "The baby still unnamed" became "Lady Zaynab (peace be upon her) still unnamed at that time", out of respect.

## [2026-10-16] — Biography of Lady Khadijah, chapter 1 laid out like the Rabi' al-Awwal article

- `/…/articles/lady-khadijah-biography/1/` (all four languages): a **contents box** ("In this chapter" / «في هذا الفصل» / «در این فصل» / «اس باب میں») linking to the four sections, **numbered section headings** (the post's own 🌳 lines, trailing colon dropped; I, II, III, IV — ١ ٢ ٣ ٤ / ۱ ۲ ۳ ۴ in ar / fa, ur), the Arabic genealogies in quotation boxes, **footnote numbers (1)(2)… as links** into a collapsible **Sources** list at the end (grouped by the sections that cite them; a footnote link opens the list and highlights the source). Text word for word. Generator: `tools/wix_import/build_khadijah_ch1.py` (rewrites only that page's body, in place, idempotent); styles `.bio-*` in `style.css`, the toggle at the end of `script.js`. Chapters 2–4 are unchanged.

## [2026-10-16] — Zaynab/Khadijah article: new title

- Title is now «شباهت حضرت خانم زینب کبری (س) به حضرت خانم خدیجه کبری (س)» (Farsi, as supplied); English "The Resemblance of Lady Zaynab al-Kubra (p) to Lady Khadijah al-Kubra (p)", Arabic «شبه السيدة زينب الكبرى (ع) بالسيدة خديجة الكبرى (ع)», Urdu «حضرت بی بی زینب کبریٰ (س) کی حضرت بی بی خدیجہ کبریٰ (س) سے شباہت» follow the wording of each post (not reviewed by a native speaker). Updated on the article, the homepage card, the Articles lists, sitemap and feed.

## [2026-10-16] — Logo and "MISBAH" lead to the main website

- In the header of every page (all four languages) the logo / MISBAH wordmark now links to https://www.misbah-inc.com/ (`/ar`, `/fa`, `/ur` on the translated pages) instead of this site's own homepage; the aria-label says so. Enforced by `fix_header.py`, which every build runs. The article site's home is still reachable from the breadcrumb "Home" link and the Articles menu.

## [2026-10-14] — Assets are versioned (changes show at once)

- Pages link `style.css`, `script.js` and `theme.js` with `?v=<content hash>` (added by `fix_header.py`, which every build runs), so a changed stylesheet or script is fetched immediately instead of staying in the browser's 10-minute cache. This is why the new text-size buttons did not show for some visitors right after publishing.

## [2026-10-14] — Muttaqin Part 15: its own poster

- Part 15 now uses its supplied poster (banner, series-page card, social image, thumbnail) instead of the generated card. `build_muttaqin.py --poster <part> <file>` does one part. Part 14 still uses the generated card until its poster is supplied.

## [2026-10-14] — Text size buttons on every page

- **A− / A+** beside the theme button in the header of every page (desktop bar and mobile menu), labelled in the page's language. Six steps (90 %–160 %; 140 % at most on phones, where 160 % would push the page wider than the screen). The page content scales (`zoom` on `<main>`) while the header and footer keep their size, so the bar never overflows; the choice is remembered (`localStorage` `misbah-fs`). Code: `assets/theme.js` + the end of `style.css`.

## [2026-10-14] — Sermon of Muttaqin, Part 15 (English)

- `/articles/khutbat-al-muttaqin/15/` — "They endured patiently for only a few days, and it resulted in an everlasting comfort" (Lady Rubab (p)); video wzn9qUMPkMs (published 13 Oct 2026), text word for word from the supplied post (`muttaqin_src/wzn9qUMPkMs.txt`), references as a list. Series page, homepage part buttons, month/tag pages, sitemap updated; series date 13 Oct. The cover is the generated card for now (the supplied Part 15 poster did not arrive as a file). Farsi / Arabic / Urdu follow when sent (`build_muttaqin_l10n.py`).

## [2026-10-14] — Muttaqin: the video on every language

- Farsi / Arabic / Urdu Part 1–2 pages now start with the same YouTube video as the English page (the other voices are being added to that one video as audio tracks, so viewers pick their language in the player). VideoObject structured data included.

## [2026-10-14] — Muttaqin Parts 1–2: titles are the editor's own lines

- Farsi / Arabic / Urdu page headings now end with the subtitle line supplied for each part («گفتاری درست و نیکو دارند», «مَنْطِقُهُمُ الصَّوَابُ», «متقین کی گفتار درست اور نیک ہوتی ہے»; Part 2: the posts' own lines, minus a stray word in the Farsi one) instead of my shortened versions.

## [2026-10-14] — Sermon of Muttaqin, Part 2 in Farsi, Arabic and Urdu

- `/fa/`, `/ar/`, `/ur/articles/khutbat-al-muttaqin/2/` (Moderation in dress and conduct — the story of Salman al-Farisi), word for word from the posts (`muttaqin_src/part02.<lang>.txt`); the Bihar al-Anwar reference is in a Sources list. Series pages in the three languages now list Parts 1–2; hreflang / sitemap / feed updated. The page-title subtitles («میانه‌روی در پوشش و رفتار», «مَلْبَسُهُمُ الْاقْتِصَادُ», «لباس اور طرزِ زندگی میں اعتدال») are short forms of the posts' subtitle lines, not reviewed by a native speaker. The Urdu source repeats a sentence ("…کوئی فرق نہیں پڑتا…" twice); kept as supplied.

## [2026-10-14] — Sermon of Muttaqin, Part 1 in Farsi, Arabic and Urdu

- `/fa/`, `/ar/`, `/ur/articles/khutbat-al-muttaqin/1/` plus a series page in each language (listing only the parts that exist there, so far Part 1). Text word for word from the editor's posts (`tools/wix_import/muttaqin_src/part01.<lang>.txt`); only hashtags, separators and emoji bullets removed; sources moved into a *Sources* list. The English Part 1 and the English series page now list the other languages in their hreflang set; catalogue, sitemap and feed updated.
- Picture = the English Part 1 poster (shared). The English YouTube video is not repeated on the other languages' pages. Series names, one-line descriptions and the part subtitles in ar/fa/ur were written for this site and are **not reviewed by a native speaker**.
- Generator: `tools/wix_import/build_muttaqin_l10n.py` — add a part by dropping `part<NN>.<lang>.txt` files (+ `CHARS` / `DESC` entries) and re-running it, then `build_sitemap.py`, `build_taxo.py`.

## [2026-10-14] — General audit: links, social image, titles, descriptions, hreflang, sitemap

- **Nav/footer "Connect", "Subscribe", "Contact Us"** (all 329 pages, 4 languages) pointed at `/connect`, which never existed (404). They now go to https://www.misbah-inc.com/subscribe.
- **Default social image**: the homepages and About pages referenced `images/mosque-madinah-hero.jpg`, which was never committed (404 in every share preview). New `images/og-default.jpg` (1200×630, logo on dark green, no text) replaces it; `og:image:height` corrected to 630.
- **Titles**: 72 titles clipped with "…" now use the full H1; the four Biography chapters and the Ziyarat parts no longer share one title.
- **Meta descriptions**: 20 that were glued ("Chapter SixSweeter…"), Arabic on an English page (Ayatul Kursi), or identical (fa Ziyarat 1/2) rewritten from the page's own text; meta, OG, Twitter and JSON-LD all updated. `build_articles.py` now prevents the cause.
- **hreflang** no longer points at `noindex` filter pages (and those pages carry none); sitemap grew from 222 to 298 URLs: 72 indexable filter pages plus the four `rabi_al_awwal` pages. Every URL now has `<lastmod>` (`add_lastmod.py`).
- `rabi_al_awwal` pages: second `<h1>` (hero) demoted to `<p>`.
- Removed empty `assets/hero/biymnih.webp` (0 bytes, unreferenced). CLAUDE.md: old domain removed from the SEO checklist; rules above documented.

## [2026-10-12] — Articles list: pictures no longer cropped

- Cards on the Articles page (and the month / tag / type pages) cropped every picture to a squarish box: the `<img height="270">` attribute fixed the height at 270px, so the CSS `aspect-ratio: 16/9` was ignored and wide pictures were cut at the sides (Ziyarat, Biography, Virtues of the Messenger, Letter of Imam Sadiq…). Added `height: auto`; all 43 cards now measure exactly 16:9.

## [2026-10-12] — Homepage: this month's occasions above Featured

- New first section right after the hero in all four languages: **Shia Calendar — Month of Jumada al-Ula**, a card with the wide poster (square on phones), the post's opening line and a Read button to the new article. Built by `build_home_featured.py` (idempotent); the Featured section follows it.

## [2026-10-12] — New article: Occasions of the Month of Jumada al-Ula (4 languages)

- `/articles/occasions-of-jumada-al-ula/` (+ `/ar/`, `/fa/`, `/ur/`): the Shia-calendar post of 12 Oct 2026 (#تقویم_شیعه #مناسبت_های_ماه #جمادی_الأولی), word for word from the four channels (fa #22933, en #23724, ar #469, ur #509); the five occasions are a numbered list. Filed under Jumada al-Awwal, type *Shia calendar announcement*; new tag **Lady Zaynab al-Kubra (p)** (ar/fa/ur names unreviewed by a native speaker) plus Lady Fatimah al-Zahra, Imam Hasan, the Holy Prophet.
- Picture: the wide image is the banner (and OG / thumbnail crop); phones get the supplied square image through `<picture>`. Same picture in all four languages (it has no text).
- Sitemap (hreflang alternates), feed and the month / tag pages updated. Generator: `tools/wix_import/build_occasions_jumada.py <dir with wide.* and square.*>`; the posts are kept in `work/tg/jumada1-posts.json`. check_site: 198 pages, 0 issues.

## [2026-10-11] — Phone number in Arabic / Farsi / Urdu footers

- The footer phone number was reordered by right-to-left text rules (the "+" and the brackets jumped around). It is now isolated as left-to-right on every page.

## [2026-10-11] — Khadijah series pages: whole picture on part cards

- On the three Lady Khadijah series pages the part cards stretched the 16:9 cover to the card's full height and cropped it to a narrow slice. The picture now keeps its 16:9 shape, centred in its column.

## [2026-10-11] — Arabic-script hero title

- Homepage title in Farsi / Arabic / Urdu: removed letter-spacing (it split joined letters), raised line-height 1.08 → 1.5 (the descender of ح touched the next line) and dropped the pale text shadow that smeared the dots.

## [2026-10-11] — Own picture for the Biography series

- New poster (`images/lady-khadijah-biography-poster.jpg`): home card `feat-khadijah-biography-v5.jpg` (square crop keeping the figure and the caravan); series cover/OG/thumbnail in all four languages use a 1.9:1 crop. All three Khadijah series now have their own pictures.

## [2026-10-11] — Own picture for the Poems series

- New poster (`images/lady-khadijah-poems-poster.jpg`, square): home card `feat-khadijah-poems-v5.jpg` shows it whole; series cover/OG/thumbnail (all four languages) use a 1.9:1 crop. Only the Biography card still uses the shared illustration.

## [2026-10-10] — Clearer glass bar on iPhone / Safari / Firefox

- Only Chromium can bend the picture behind the bar (SVG refraction), so on phones the bar was frosted plastic. In browsers without it the bar now uses far less blur and tint (5px blur, strong saturation, bright rim), so the image behind reads as under glass. Chromium (laptop, Android Chrome) is unchanged.

## [2026-10-10] — Khadijah cards: square pictures

- Card pictures are now square (1:1) so the Ziyarat poster shows in full with its border. Poems/biography show the whole illustration on a blurred fill until their own posters arrive. Files are `feat-khadijah-*-v4.jpg`.

## [2026-10-10] — Own picture for the Ziyarat series

- The Ziyarat-explanation series now has its own poster (`images/lady-khadijah-ziyarat-poster.jpg`, square, framed «يا أم المؤمنين»). Homepage card: `feat-khadijah-ziyarat-v3.jpg` (16:9 crop that keeps all the calligraphy and the dome); series page cover/OG/thumbnail in all four languages use the same crop. Poems and biography still use the shared illustration until their posters arrive.

## [2026-10-10] — Lady Khadijah cards: whole picture

- The three Featured cards used tight crops that cut the calligraphy mid-word and showed bare fabric. They now show the whole illustration (16:9, 640×360) with the verse and both figures intact.

## [2026-10-10] — Light-theme contrast fixes; footer WhatsApp / Telegram menus

- **Text that vanished in the (new default) light theme.** Several pages styled their text with `var(--white)` on `var(--dark-bg)`; in the light palette `--dark-bg` is cream, so it came out white on cream: the whole **About** page (all four languages) and the title/subtitle banner of the **Articles, month, tag and type** pages. Fixed with light-theme colours. Also darkened labels that were under 3:1 on cream (reading time, month, "Read in", gold references and "next/previous part" captions). An automated contrast check (every text element, 16 page types × light and dark) now reports 0 problems.
- **Footer social icons:** the WhatsApp and Telegram icons in the footer were single links (one channel). They now open the same four-channel menus as the top of the homepage (EN/AR/FA/UR names in the page's language, opening upward), on all 315 pages — added by `fix_header.py`, which also runs after every build.

---

## [2026-10-10] — Homepage: Featured section moved up, with the three Lady Khadijah series

- The **Featured** section now sits straight after the hero on all four homepages (it was fourth). Order: hero → Featured → Latest series (English) → Topics → Al-Kawthar → Morning & Evening Mourning → YouTube.
- Under the featured article: "More on Lady Khadijah (p)" with three cards — **Biography**, **Poems**, **Ziyarat explanation** — using each language's own series titles and descriptions and linking to that language's series page (cards in `/ar/`, `/fa/`, `/ur/` point at the translated series). Pictures: three different crops of the Lady Khadijah illustration (`images/home/feat-khadijah-*.jpg`).
- Generator: `tools/wix_import/build_home_featured.py` (idempotent); `build_home_topics.py` now places Topics before the Al-Kawthar section instead of before Featured.

---

## [2026-10-10] — iOS-style liquid glass top bar

- **Refraction:** script.js draws a displacement map for the bar's exact size (rounded-rect distance field, strongest at the rim) and uses it as a backdrop filter, so text and pictures passing under the bar bend near its edge like a lens. Redrawn on resize; mobile pill included. Chromium-based browsers only — Safari and Firefox do not allow SVG backdrop filters, so they keep the thin frost, saturation boost, bright rim and highlight below.
- **Every browser:** thinner frost so the content stays recognisable; a bright conic rim; a specular highlight that follows the pointer over the bar and drifts as the page scrolls; more transparent when the page is scrolled. **The bar itself never moves** (an earlier version stretched/squashed it while scrolling, which read as shaking): instead the refraction of what is seen through the glass grows with scroll speed (rim displacement about 34 → 78 px at a fast flick, plus a little extra frost, which is the cue Safari gets) and eases back to the resting amount in about 0.9 s after the page stops. Light theme keeps enough white for the logo/menu to stay readable over photos. Off for `prefers-reduced-motion` / `prefers-reduced-transparency`.

---

## [2026-10-10] — Light is the default theme; broken social icons in ar / fa / ur

- **Default theme = light.** Every page now ships `<html … data-theme="light">` (set by `fix_header.py`, so it survives rebuilds); a visitor's saved choice (`misbah-theme` in localStorage) still wins, and the theme button's label is set correctly when nothing is saved. Sections that sit on a photo (Morning & Evening Mourning, Latest series) keep light text in the light theme — their headings had turned dark green on a dark picture.
- **Social icons:** the Facebook icon (and three more in the same row) had its SVG path data cut off at the start in `ar/`, `fa/` and `ur/` (`d="6.627-5.373…"` instead of `d="M24 12.073c0-6.627…"`), so the circle was empty. Repaired from the English page on the three homepages and the Urdu About page (12 + 12 paths); no other malformed paths remain on the site.

---

## [2026-10-10] — Featured card in ar / fa / ur on phones

- On phones and small tablets (≤ 768 px) the Featured article card was broken in Arabic, Farsi and Urdu: a tall empty box above a squeezed picture. The generic phone rule that stacks the card was overridden by the later `[dir="rtl"] .featured-card { flex-direction: row-reverse }`. The phone layout now also wins for RTL pages, and the picture is cropped to fill its box on phones.

---

## [2026-10-10] — Header fixes on every page: language links, theme button, mobile glass menu

- **Language switcher was wrong on 302 of 315 pages**: the generators copy the Lady Khadijah article's header into every page they write, so EN / AR / FA / UR all linked to `/…/articles/rabi_al_awwal/`. New `tools/wix_import/fix_header.py` rewrites the switcher on every page: each language links to the same page in that language (the page's own hreflang alternate, else the same path if it exists, else that language's articles index or home for English-only content), the current language is marked active. It also adds the **theme (light/dark) button**, which was missing from 158 pages. It runs at the end of `build_sitemap.py` and `build_taxo.py`; `check_site.py` now fails if a header regresses (headers wrong: 0). `script.js` now marks the active language by `hreflang` (it used to un-mark it on every page but the homepages).
- **Audit of ar / fa / ur:** every page has the right `lang`/`dir`, a canonical equal to its own URL, reciprocal hreflang and the right `og:locale` (one Arabic page had a different locale: fixed). English 158 pages, Arabic 57, Farsi 50, Urdu 50 — the difference is English-only articles, which now send AR/FA/UR to that language's articles index.
- **Mobile menu (≤ 768px):** the open menu was a flat white block under the bar. It is now a floating rounded pane of frosted glass under the pill (blur, bright edge, springy open/close), with glass buttons, a glass language switcher and the theme button in the last row; works in light/dark and right-to-left. The hamburger is a glass button.

---

## [2026-10-10] — Three Lady Khadijah series from the Telegram channels, in four languages

- **`/articles/lady-khadijah-poems/`** (8 poems), **`/articles/lady-khadijah-biography/`** (4 weekly chapters) and **`/articles/lady-khadijah-ziyarat/`** (4 Friday parts of the ziyarat commentary), each with parts `/1/`…, mirrored under `/ar/`, `/fa/`, `/ur/` — 3 series pages + 16 part pages per language, 76 pages. Part N is the same part in every language; every page links to its three siblings (language switcher + hreflang `en`, `ar`, `fa`, `ur`, `x-default`).
- **Source:** the channels @misbah110 (fa), @misbah110_en, @misbah110_ar, @misbah110_ur — text word for word. Only Telegram furniture is removed (hashtag header, ✦━✦ dividers, the @channel footer, bullet emoji); a post split over two messages is joined; the repeated "🌸 Biography of Lady Khadijah… 🌸" title line (the series name) is not repeated on each page. Generator: `tools/wix_import/build_khadijah.py` (+ `tg_collect.py`, `tg_scan.py`); scans are cached in `work/tg/`. The 17 early daily "Introducing Lady Khadijah" parts (26 Aug–12 Sep) are intentionally not included.
- **SEO per language:** `<html lang dir>`, canonical, hreflang for all four + x-default, Open Graph (`og:locale` en_US/ar_AR/fa_IR/ur_PK) and Twitter tags, `Article` + `BreadcrumbList` + `CreativeWorkSeries` JSON-LD with `inLanguage`, one h1, a title tag of the form "<heading> | <series> | <brand>" (≤ 70 chars) and a description from the part's own first paragraphs. All 76 pages audited, 0 issues; `check_site.py` 194 pages, 0 issues.
- Filed under Rabi' al-Thani, type Series; tags Lady Khadijah (+ Holy Prophet for the poems, Ziyarat for the commentary). Series appear on the articles index, the Rabi' al-Thani / Series / Lady Khadijah tag pages, the sitemap (19 new URLs per language) and `feed.xml` (rebuilt: 63 items).
- Cover: the existing Lady Khadijah illustration for all three series (one shared picture per series and language). New CSS: `.tg-ref` (reference lines).

---

## [2026-10-09] — Liquid-glass theme, site-wide; inner pages follow the light/dark choice

- **Liquid glass** (end of `assets/style.css`, filters in `assets/script.js`): the top bar is a floating frosted pill; menu pills, slider buttons, gold buttons, cards (articles, series parts, poster cards, topics, featured), quote and source panels, tags and chips are glass with a bright top edge, soft inner glow and springy hover. On Chromium-class browsers a faint wavy refraction is added (SVG displacement, set up by `script.js`); other browsers keep the frosted blur. The "Latest series" card sits on the poster scene as a glass pane. Respects `prefers-reduced-motion` and `prefers-reduced-transparency`.
- **Light/dark now apply to article-style pages too** (article, series, booklet, index, tag/month/type, ar/fa/ur): they used to stay cream whatever the theme. Dark is the default (like the homepage); explicit light keeps the cream look. Light theme also fixed: the hero is cream with dark text and calligraphy (it stayed dark green with unreadable text), and there is no white box behind the nav pills.
- Tag pills: the glass edge is on the pill itself, not on the link inside it (it had drawn a box within each pill).

---

## [2026-10-09] — Homepage "Latest on YouTube" now follows the channel's newest Shorts

- New `tools/update_youtube.py` reads the channel's public feed, recognises Shorts (canonical URL under `/shorts/`), and rewrites the five video cards on all four homepages: each language gets the newest Shorts whose title is in that language, topped up with the newest other Shorts, then normal videos. Titles are written into the HTML (no runtime lookup needed). A browser cannot do this itself — YouTube's feed blocks cross-origin requests — so it must be run before each deploy (or on a schedule). Standard library only.
- Run: `python3 tools/update_youtube.py` (add `--dry-run` to only list the picks), then `python3 tools/deploy_s3.py …`.

---

## [2026-10-09] — Topics slider: arrows moved off the cards, plus motion

- The previous/next buttons now sit in their own side gutters (about 18 px clear of the cards); on phones they move under the slider, one at each end with the page dots between.
- Motion: buttons grow and glow on hover, press down on click, and the arrow nudges toward its direction; the active dot stretches into a pill; cards scrolled out of view dim and shrink slightly and settle as they slide in; the "next" button gets a soft pulsing ring until the first use. All of it is off under `prefers-reduced-motion`.

---

## [2026-10-09] — Homepage Topics became a slider; "Latest series" has a picture background

- **Topics** now lists every main topic in a scroll-snap slider, 4 cards at a time on desktop (3 on tablets, 2 on small tablets, one with a peek of the next on phones), with previous/next buttons and page dots; the buttons and dots only appear when something is off-screen, so a language with few topics shows a plain row. Works right-to-left (buttons and scrolling mirror), keyboard-focusable, no library. English shows 10: Sermon of Muttaqin, Al-Kawthar, The Recognition of Arbaeen, Morning & Evening Mourning, the three Booklets series, Lady Khadijah, Imam al-Hussain, the Holy Prophet. ar/fa/ur keep the topics that have pages in their language. Code: `build_home_topics.py` (markup), `style.css` (`.topic-carousel`), `script.js` (slider).
- **"Latest series" (Sermon of Muttaqin) section** uses a wide scene cut from the series poster instead of the plain green (`images/home/muttaqin-section.jpg` + a mobile crop), with a dark layer for legibility.
- Topic-card images fixed to a true 16:9 (the `height` attribute had stretched them).
- New card images in `images/topics/` (registered in `images/CATALOG.md`).

---

## [2026-10-08] — Booklets, second batch: the Arabic-heavy ones, Arabic kept as images

- Added to the two series and a third: **Muharram & Safar 10–18** (Ziyārat Nāḥiyah excerpts, The Reality of Weeping for Hussain, Ziarat of Imam Ali ibn al-Hussain / Hadith of the Tablet, Shared Traits of Ali Akbar and Ruqayyah, Sermon of Imam al-Hasan on the Peace Treaty, Ziarat Lady Umm al-Banin, School of Umm al-Banin summary, The Final Lament of Reyḥānat al-Ḥusayn, Walking Path of Hussain), **Ghadir 6–9** (Sermon of Mufākharah, Excerpt from Ziyārat Ghadīriyya, Ziyārat of Ali Akbar, Spring of Love) and **Ramadan Booklets 1** (Ziyārat of Khadija). 29 booklets are now live in total; about 380 Arabic lines are pictures cropped from the PDF pages.
- Extractor now works line by line (a block can mix Arabic and English), joins runs that share a baseline, attaches stray quotes/brackets, and drops text-layer debris (lone footnote numbers and transliterations whose letters were lost, e.g. "ā humma b ā rik li"). The picture beside such a line already carries the text.
- **Still not built:** Treasures of the Family of Muhammad (599 pages), the full School of Umm al-Banin book (108 pages), the Ramadan Workbook (91 MB), three image-only Ramadan PDFs (no text layer), Ziyarat Lady Fatima (2 pages, Arabic only).

---

## [2026-10-08] — Booklets from misbah-inc.com/book as article series (first batch, not yet deployed)

- Two series from the PDF booklets, English only: **`/articles/muharram-safar-booklets/`** (1–9: the Nights of Loyalty, Repentance, Reunion, the Witness, Patience, Longing, Labbayk, Perfection + Heartfelt Writings for Lady Ruqayyah) and **`/articles/ghadir-booklets/`** (1–5: The Sun, The Successor, Wali, The Conqueror, The Uncle). Each page: the booklet's cover as banner, its English text (unchanged, from the PDF's text layer), its illustrations in order, Arabic lines as **cropped images** (the PDF's Arabic text layer is scrambled), and a link to the original PDF on misbah-inc.com.
- Generator: `tools/wix_import/build_booklets.py` + `booklet_extract.py`; `booklet_review.py` writes `work/arabic-review.html` (all 23 Arabic crops, for human review). The PDFs are kept out of the repo.
- **Not built yet** (19 of the 35 PDFs): the long Arabic-heavy books (Ziyārat Nāḥiyah excerpts, Reality of Weeping, Ziarat of Imam al-Sajjad, Shared Traits, Sermon of Imam Hasan, School of Umm al-Banin 108 pp, Treasures 599 pp, Sermon of Mufākharah, Ziyārat Ghadīriyya, Spring of Love, Ziyārat of Umm al-Banin/Fatima/Ali Akbar/Khadija, Ramadan Workbook 91 MB) need clean Arabic text; plus 3 image-only Ramadan PDFs (no text layer). Held back for scrambled text: The Final Lament of Reyḥānat al-Ḥusayn, Walking Path of Hussain. The site links "The Cosmic Blueprint" to the Night of Qadr file (a Wix mislink), so that booklet is missing.
- `check_site.py`: 103 pages, 0 issues.

---

## [2026-10-08] — "The Recognition of Arbaeen" is now one series

- The two stand-alone articles `recognition-of-arbaeen-part-1` / `-2` are merged into a series: **`/articles/recognition-of-arbaeen/`** with chapters **`/1/`** and **`/2/`** (English only; same Wix posts and text, covers and in-article images moved to the new names). Filed under Safar, type **Series**, tags Imam al-Hussain + Arbaeen.
- **Old URLs removed** (`/articles/recognition-of-arbaeen-part-1/`, `-part-2/`): dropped from the sitemap, indexes and tag/month pages, and deleted from the bucket by the deploy. They were never on a public domain.
- Generator: `tools/wix_import/build_arbaeen.py` (reuses `build_mourning.series_page`); `batch2.json` no longer lists the two old slugs. Part 2's Wix title is spelled "Arabeen" and is kept as published. `check_site.py`: 87 pages, 0 issues.

---

## [2026-10-07] — Sermon of Muttaqin: supplied posters

- Series cover = the supplied landscape poster; parts 1–13 = their own portrait posters (banner 720×1280 on the part page; OG 1200×630 and card thumbs show the poster centred on a blurred copy of itself). Part 14 still uses the generated card until its poster arrives. `build_muttaqin.py --posters <dir>` rebuilds them (file `2.*` = part 1 … `14.*` = part 13).

---

## [2026-10-07] — New series: Sermon of Muttaqin (Khutbat al-Muttaqin), parts 1–14

- **`/articles/khutbat-al-muttaqin/`** (series page) + **`/1/` … `/14/`**, English only. Each part opens with its YouTube video (click-to-load via youtube-nocookie, `VideoObject` JSON-LD), then the text. Filed under **Rabi' al-Awwal**, type **Series**, tag **Imam Ali (p)**.
- **Source:** the channel's own video descriptions (text kept word for word; hashtags, emoji bullets and separators removed; Arabic lines of the sermon set as Arabic). Parts 12 and 13 carried the same passage twice (a rough draft and a clean version); only the clean copy is shown — the dropped lines are listed in `tools/wix_import/muttaqin_content.py`.
- **Languages:** no Arabic, Farsi or Urdu version of this series exists yet, so no `/ar|fa|ur/` pages were created (hreflang lists `en` + `x-default` only; the series is absent from the other-language indexes and homepages).
- **Homepage (EN):** new "Latest series" card above Topics, with a button per part. Articles index, `month/rabi-al-awwal`, `tag/imam-ali`, `type/series` and the sitemap were regenerated.
- **Covers** are generated (Pillow): `images/articles/khutbat-al-muttaqin-{1..14}-en.jpg`, `og-…`, `thumb-…`, plus `khutbat-al-muttaqin-cover-en.jpg` for the series. `build_index.py` now prefers `<slug>-cover-<lang>.jpg` for a series card.
- Generator: `tools/wix_import/build_muttaqin.py` (re-runnable; add a part by extending `PARTS` in `muttaqin_content.py`, adding `muttaqin_src/<id>.txt` and a `DESC` line, then run `build_sitemap.py`, `build_taxo.py`, `check_site.py`). `check_site.py`: 86 pages, 0 issues.

---

## [2026-10-07] — Mobile fixes: series cards and the Mourning section

- Series part/chapter cards (`.kw-part-card`, `.kw-home-card`): on phones the image ran down behind the title and text; it now sits above the text at its natural shape (whole banner visible). Affects Al-Kawthar and Morning & Evening Mourning in all languages.
- Homepage Morning & Evening Mourning section on phones: even dark overlay and near-opaque panels so the label, title, description and chapter buttons are readable over the picture (also in the light theme).

---

## [2026-10-07] — Homepage topics section; Calendar moves to the menu

- **New "Topics" section** right after the hero on all four homepages: three cards (Al-Kawthar series · Lady Khadijah · Imam al-Hussain & Mourning) linking to the series page or the existing `/articles/tag/…` pages. Each language shows only topics that have a page in it; fa/ur have no Imam Hussain pages yet, so they show the Holy Prophet card instead. Card images: `images/topics/`.
- **"Through the Year" month grid removed** from the homepages (with its "this month" script). The months are now a **Calendar** dropdown in the top menu on every page (192 pages), linking to `/articles/month/<month>/`; months with no page in that language are muted "coming soon", never a dead link.
- Generator: `tools/wix_import/build_home_topics.py` (run after `build_taxo.py`; re-run whenever month/tag pages appear). `build_taxo.py` no longer rewrites homepage month cards.
- SEO: no URLs removed (month pages unchanged); sitemap unaffected. Topic card images have empty `alt` (decorative, the card text names the topic). Homepage meta/JSON-LD in ar/fa/ur not touched; `check_site.py` passes (71 pages).

---

## [2026-10-07] — First deploy to AWS

- Bucket `article-misbah-inc` + CloudFront `E2N0F3SGBTA0UD` created; 461 files uploaded with `tools/deploy_s3.py`; tested on the CloudFront address (pages, 404 returns a real 404, sitemap, gzip, correct image types).
- `deploy_s3.py` fix: the cache-header pass reset image content types to `binary/octet-stream`; it now sets `--content-type` per extension.
- Still to do: the Wix CNAME `article` → `d1ispgyfziwqwx.cloudfront.net` to make `article.misbah-inc.com` live.

---

## [2026-10-07] — Four posts re-typed as Shia calendar announcements

- "The Month of Rabi al-Akhir", "Hadrat Abdul Azim Hasani" (4 Rabi al-Thani birth anniversary), "Rabi al-Awwal" (month introduction) and "The Second Ghadir" (9 Rabi al-Awwal) were typed Article; they are calendar occasion posts, so they are now **Shia calendar announcement**. The announcement type page lists 19 entries (in English).

---

## [2026-10-07] — Tags, filters and the Shia-calendar announcements

- **Master tag list** (`tools/wix_import/taxonomy.py`): every article has exactly one **month** (12 Hijri months, or "Any time of year"), one **type** (Article · Series · **Shia calendar announcement**), and any number of **person** and **topic** tags — each with an English, Arabic, Farsi and Urdu name. Wix's own categories (with their duplicates and "Latest") are no longer shown.
- **Articles page rebuilt in all four languages:** filter bar (month, type, tag, free-text search; state in the URL so a view can be shared), card grid, and crawlable "Browse by month / type / tag" links. The old English month-card modal is gone; the homepage's "Through the Year" cards remain and link to month pages.
- **Static filter pages** `/articles/month/<m>/`, `/articles/type/<t>/`, `/articles/tag/<t>/` (89 pages, per language that has entries). Pages with a single entry are `noindex,follow` and left out of the sitemap (26 of them); the rest are in it (sitemap now 158 URLs).
- Every article page shows its month, type and tags as links (tags also feed `article:tag` and JSON-LD keywords).
- **15 announcements imported** (English only): Muharram 1448 programme, majalis for Imam al-Baqir / al-Jawad / al-Sadiq / Nights of Qadr / Umm al-Banin / Fatima al-Zahra (x2) / Prophet, Hasan, Ridha / Arbaeen / Ruqayyah / Imam al-Sajjad, the Muharram 1447 food drive, the Ghadir 2025 thank-you, the Safar notice. Flyer images are the cover; the Ghadir photo gallery (about 40 photos) was **not** imported.
- Months were inferred from each occasion's Hijri date; the following are guesses and should be reviewed: Fatima al-Zahra announcements (Jumada al-Awwal), Muhsin ibn Ali (Safar), the Elegy of Imam Hussain's Thirst (Muharram), the Mourning series (Muharram).
- ar/fa/ur tag, type, month and interface names were written for this site and are unreviewed.

---

## [2026-10-07] — Morning & Evening Mourning series (10 chapters)

- **New:** series page `/articles/morning-and-evening-mourning/` and chapters at `…/1/` to `…/10/` (the URLs the homepage already linked to — its ten dead chapter buttons now work). Chapters are English; **chapters 1 and 2 also have Arabic** (`/ar/articles/morning-and-evening-mourning/`, listing just those two) — the Wix blog has no fa/ur versions. Text verbatim; each chapter's "Chapter N" line and subtitle are shown as the lead.
- Arabic chapter titles are the Wix series title plus the chapter label from the post ("العزاء صباحًا ومساءً — الفصل الأول"), because both Arabic posts are titled only with the series name and would otherwise have identical titles.
- Series cards for the articles indexes (en, ar); the ar/fa/ur homepages' chapter buttons go to the Arabic page where one exists and the English page otherwise.
- Importer: `tools/wix_import/build_mourning.py`. Sitemap now 80 URLs.
- Known, pre-existing: the nav's "Connect" menu links to `/connect` (Subscribe / Contact), which has no page, on every page.

---

## [2026-10-07] — Ten English-only articles from the Wix blog

- **Imported (10 pages, English only — the Wix blog has no ar/fa/ur versions of these):** Virtues of the Messenger of Allah · Imam Hasan al-Askari: Keeper of God's Knowledge · The Second Ghadir · Rabi al-Awwal · Martyrdom of Muhsin ibn Ali · Husn al-Hassan in the Qur'an · Ayatul Kursi · The Recognition of Arbaeen (Parts 1 and 2) · The Elegy of Imam Hussain's Thirst. hreflang lists only English (+ x-default); no placeholder pages were made for the missing languages.
- Article-body images are copied off Wix's CDN into `images/articles/<slug>/`. Ayatul Kursi has no cover on Wix, so it uses a branded placeholder (`images/articles/*fallback.jpg`).
- Safar's card on the English homepage is live (the two Arbaeen parts). `tools/wix_import/build_sitemap.py` regenerates the sitemap block (66 URLs).
- Wix source typo kept verbatim: Arbaeen Part Two is titled "The Recognition of Arabeen".

---

## [2026-10-07] — Eight more articles from the Wix blog (EN/AR/FA/UR) + localized article indexes

- **Imported (32 pages):** Virtues of the Ziarat of Lady Fatimah Ma'soumah · Hadrat Abdul Azim Hasani · The Month of Rabi al-Akhir · Supplications of Salawat · Letter of Imam al-Sadiq to the Shia · The Blessed Title "al-Sadiq" · Blessed Marriage of Lady Khadijah and the Prophet · 30 Names and Titles of the Messenger of God. Each language is built from its own Wix post, text verbatim; embedded YouTube videos are click-to-load.
- **Articles index** now exists in all four languages (`/ar|fa|ur/articles/`, card grid). The English index keeps its month picker but lists only real articles, adds an "All articles" grid and opens a month via `?month=N`; its cards use small thumbnails instead of the 2 MB originals.
- **Homepages:** Rabi' al-Awwal and Rabi' al-Thani cards are live; ar/fa/ur nav and "Articles" links point to their own index.
- **Importer** saved as `tools/wix_import/` (see its README) — fetches slowly, builds pages, runs `check_site.py` (title/description/canonical/hreflang/JSON-LD/alt/og checks on every page).
- Sitemap now has 56 URLs.
- Not imported by decision: Morning & Evening Mourning (10 chapters) and the event announcements. Pending: 10 English-only articles.

---

## [2026-10-06] — New home: article.misbah-inc.com (AWS), misbah128.com retired

- Every `misbah128.com` URL (canonical, hreflang, OG/Twitter, JSON-LD, sitemap, robots) is now `article.misbah-inc.com`; the Library link is `library.misbah-inc.com`. No redirect from the old domain (retired by decision).
- Added `404.html` (noindex, four languages) and `tools/deploy_s3.py` (S3 + CloudFront deploy, with excludes, per-type cache headers and one invalidation).
- **Not live yet:** the AWS bucket, certificate, CloudFront distribution and Wix CNAME still have to be created. Until then these URLs do not resolve.

---

## [2026-10-06] — Al-Kawthar series (imported from the Wix blog)

- **New:** `/articles/al-kawthar/` (series page) and `/part-1/`, `/part-2/` — each in EN, AR, FA, UR (12 pages), at `/ar|fa|ur/articles/al-kawthar/…`. Text copied verbatim from the published posts at misbah-inc.com; each language is built from its own post, not translated.
- **Embedded video:** every part has its own YouTube video per language (public, embeddable, Misbah channel). Click-to-load via `youtube-nocookie.com`, so nothing is requested from YouTube until the reader presses play. `VideoObject` JSON-LD included.
- **Images:** the posts' own banners (`images/kawthar/part{1,2}-{lang}.jpg`, 1400 px wide, ~140–210 KB) plus 1200×630 social cards (`og-part*.jpg`).
- **SEO:** per-language title/description (≤160)/canonical/hreflang (all 4 + x-default)/OG/Twitter, `Article` + `BreadcrumbList` + `CreativeWorkSeries` JSON-LD, 12 sitemap entries.
- **Homepage:** new "New series" card linking to the series.
- Not in the article text: UI labels (Series, Sources, Previous/Next part, Watch the video…) in AR/FA/UR were written for the site and are unreviewed.

---

## [2026-10-06] — Refocus on articles

- **Removed** the Hijri calendar and moonsighting pages (all four languages), `assets/moonsighting.js`, the homepage prayer-times bar, Shia calendar and donation widget, and every nav/footer/sitemap link to them. The Donate link is gone from all pages.
- **New homepage section "Through the Year"** (`#through-the-year`, all four languages): twelve Hijri-month cards from 480×640 thumbnails in `images/months/` (≈40 KB each, from the 2 MB originals). Only month 3 has a published article, so it is the one live card; the rest read "Coming soon". The current Hijri month is tagged client-side.
- Hero, featured article, Morning & Evening Mourning series, YouTube row, About Us and footer are unchanged.
- `assets/script.js` lost its prayer-times and donation code. The moonsighting/donation/calendar CSS in `style.css` is now dead and can be pruned.
- `tools/` is untouched — `gen_visibility_map.py` is still the reference for the app's `moonsighting.ts`.

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
