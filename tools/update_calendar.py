"""
update_calendar.py — Refresh the homepage calendar section for the current Hijri month.

Usage:
    python tools/update_calendar.py

Requires:
    pip install hijri-converter beautifulsoup4

What it does:
1. Computes the Gregorian date for each Hijri event day in the current month.
2. Rewrites the Gregorian date badges (<span class="event-greg">) in index.html.
3. Updates the month name and Hijri year badge in the calendar header.

Run this once per Hijri month (roughly once per Gregorian month) to keep the
calendar accurate. Commit the result to git — no server needed.
"""

import re
import sys
from pathlib import Path
from hijri_converter import convert

# ── Configuration ──────────────────────────────────────────────────────────

# Events: list of (hijri_day, gregorian_label_format)
# Add / remove events here as needed.
EVENTS = [
    (8,  "Martyrdom of Imam Hasan al-Askari"),
    (9,  "Second Ghadir"),
    (10, "Marriage of Lady Khadijah"),
    (17, "Birth of Prophet / Imam al-Sadiq"),
    (24, "Arrival of Lady Fatima al-Ma'suma in Qom"),
    (26, "Laylat al-Mabit"),
]

HIJRI_MONTH_NAMES = [
    "", "Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani",
    "Jumada al-Ula", "Jumada al-Akhirah", "Rajab", "Sha'ban",
    "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah",
]

GREG_MONTH_SHORT = [
    "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

INDEX_HTML = Path(__file__).parent.parent / "index.html"

# ── Compute current Hijri month ─────────────────────────────────────────────

from datetime import date
today_g = date.today()
today_h = convert.Gregorian(today_g.year, today_g.month, today_g.day).to_hijri()
hijri_year  = today_h.year
hijri_month = today_h.month
month_name  = HIJRI_MONTH_NAMES[hijri_month]

print(f"Current Hijri date: {today_h.day} {month_name} {hijri_year}")
print(f"Updating calendar for: {month_name} {hijri_year}\n")

# ── Build day → Gregorian label map ────────────────────────────────────────

def hijri_to_greg_label(h_day):
    """Return e.g. 'Aug 21' for a given Hijri day in the current month."""
    try:
        g = convert.Hijri(hijri_year, hijri_month, h_day).to_gregorian()
        return f"{GREG_MONTH_SHORT[g.month]} {g.day}"
    except Exception as e:
        print(f"  Warning: could not convert {h_day} {month_name}: {e}")
        return "?"

day_to_greg = {day: hijri_to_greg_label(day) for day, _ in EVENTS}
for day, label in day_to_greg.items():
    print(f"  {day:2d} {month_name} → {label}")

# ── Patch index.html ────────────────────────────────────────────────────────

html = INDEX_HTML.read_text(encoding="utf-8")

# 1. Update the Hijri year + month badge
html = re.sub(
    r'Hijri \d+ · [^<]+',
    f"Hijri {hijri_year} · {month_name}",
    html,
)

# 2. Update the section heading
html = re.sub(
    r'(<h2 class="section-title"[^>]*>)[^<]+(</h2>)',
    rf'\g<1>{month_name}\g<2>',
    html,
)

# 3. Update each event-day span
def replace_greg(m):
    day_num = int(re.search(r'(\d+)', m.group(0)).group(1))
    new_label = day_to_greg.get(day_num, "")
    return f'<div class="event-day">{day_num}<span class="event-greg">{new_label}</span></div>'

html = re.sub(
    r'<div class="event-day">\d+<span class="event-greg">[^<]*</span></div>',
    replace_greg,
    html,
)

INDEX_HTML.write_text(html, encoding="utf-8")
print(f"\n✓ index.html updated for {month_name} {hijri_year}")
