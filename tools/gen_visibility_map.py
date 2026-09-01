"""
Yallop (1997) crescent moon visibility map generator — multiprocessed.
Runs one worker per CPU core; ~2 min for a 900×450 map on 16 cores.

Usage:
  python gen_visibility_map.py <new_moon_utc> <out_dir> [night]
  python gen_visibility_map.py "2026-08-12T17:37:11" "../moonsighting/maps" 1

Dependencies: pip install astronomy-engine Pillow numpy
"""

import sys, os, math, multiprocessing
from datetime import datetime
import math as _math
import numpy as np
from PIL import Image
import astronomy

ZONE_COLORS = {
    'A': (56,  184, 114),
    'B': (0,   200, 210),
    'C': (120, 120, 130),
    'D': (180,  50,  50),
    'E': (110,  25,  25),
    'F': (70,   10,  10),
    'G': (80,   15,  15),    # moonset before sunset — treat as not visible
    'H': (60,   10,  10),   # conjunction after sunset — treat as not visible
    'X': (7,    18,  32),
}

NEW_MOONS_1448 = [
    ("Muharram",     "2026-06-15T02:54:39"),
    ("Safar",        "2026-07-14T09:44:04"),
    ("Rabi I",       "2026-08-12T17:37:11"),
    ("Rabi II",      "2026-09-11T03:27:28"),
    ("Jumada I",     "2026-10-10T15:50:36"),
    ("Jumada II",    "2026-11-09T07:02:42"),
    ("Rajab",        "2026-12-09T00:52:31"),
    ("Shaban",       "2027-01-07T20:25:05"),
    ("Ramadan",      "2027-02-06T15:56:47"),
    ("Shawwal",      "2027-03-08T09:30:07"),
    ("Dhu al-Qadah", "2027-04-06T23:51:45"),
    ("Dhu al-Hijjah","2027-05-06T10:59:10"),
]


def _yallop_code(base_ut, lat, lon):
    """Return zone letter for one (lat, lon) point."""
    if lat < -60 or lat > 75:
        return 'X'
    observer = astronomy.Observer(lat, lon)
    t_search = astronomy.Time(base_ut - lon / 360.0)

    sunset  = astronomy.SearchRiseSet(astronomy.Body.Sun,  observer, astronomy.Direction.Set, t_search, 1)
    moonset = astronomy.SearchRiseSet(astronomy.Body.Moon, observer, astronomy.Direction.Set, t_search, 1)
    if sunset is None or moonset is None:
        return 'X'

    lag = (moonset.ut - sunset.ut) * 1440  # minutes
    if lag < 0:
        return 'G'

    best = astronomy.Time(sunset.ut + lag / 1440 * 4 / 9)

    nm_prev = astronomy.SearchMoonPhase(0, best, -35)
    nm_next = astronomy.SearchMoonPhase(0, best,  35)
    if nm_prev is None or nm_next is None:
        return 'X'
    nm = nm_prev if (best.ut - nm_prev.ut) <= (nm_next.ut - best.ut) else nm_next

    if sunset.ut < nm.ut:
        return 'H'

    moon_eq = astronomy.Equator(astronomy.Body.Moon, best, observer, True, True)
    moon_hor = astronomy.Horizon(best, observer, moon_eq.ra, moon_eq.dec, astronomy.Refraction.Airless)

    elong_ev = astronomy.Elongation(astronomy.Body.Moon, best)
    ARCL = elong_ev.elongation

    SD = astronomy.Libration(best).diam_deg * 60 / 2
    SD_topo = SD * (1 + math.sin(math.radians(moon_hor.altitude)) *
                        math.sin(math.radians(SD / 0.27245 / 60)))
    W_topo = SD_topo * (1 - math.cos(math.radians(ARCL)))

    # ARCV via equatorial vectors
    rot  = astronomy.Rotation_EQJ_EQD(best)
    gm   = astronomy.GeoVector(astronomy.Body.Moon, best, True)
    gs   = astronomy.GeoVector(astronomy.Body.Sun,  best, True)
    def hor(v):
        eq = astronomy.EquatorFromVector(astronomy.RotateVector(rot, v))
        return astronomy.Horizon(best, observer, eq.ra, eq.dec, astronomy.Refraction.Airless)
    ARCV = hor(gm).altitude - hor(gs).altitude

    q = (ARCV - (11.8371 - 6.3226*W_topo + 0.7319*W_topo**2 - 0.1018*W_topo**3)) / 10

    if   q >  0.216: return 'A'
    elif q > -0.014: return 'B'
    elif q > -0.160: return 'C'
    elif q > -0.232: return 'D'
    elif q > -0.293: return 'E'
    else:            return 'F'


def _compute_row(args):
    """Worker: compute one pixel row. Returns list of RGB tuples."""
    base_ut, py, H, W = args
    step_lat = 150 / H   # -75° to +75° span (150°)
    step_lon = 360 / W
    lat = 75 - (py + 0.5) * step_lat
    row = []
    for px in range(W):
        lon = -180 + (px + 0.5) * step_lon
        try:
            code = _yallop_code(base_ut, lat, lon)
        except Exception:
            code = 'X'
        row.append(ZONE_COLORS.get(code, ZONE_COLORS['X']))
    return py, row


def generate_map(nm_utc_str, out_dir, night=1, W=900, H=450):
    nm_dt = datetime.fromisoformat(nm_utc_str)
    nm_ut = astronomy.Time.Make(nm_dt.year, nm_dt.month, nm_dt.day,
                                 nm_dt.hour, nm_dt.minute, nm_dt.second)
    # Snap to UTC midnight of conjunction date + night offset.
    # Using nm_ut.ut directly carries the fractional NM time (e.g. 17:37 UT),
    # which pushes the search window past sunset in western longitudes.
    base_ut = math.floor(nm_ut.ut) + night

    print(f"Night {night} — {nm_utc_str}  ({W}×{H} px, {multiprocessing.cpu_count()} cores)")

    args = [(base_ut, py, H, W) for py in range(H)]

    pixels = np.zeros((H, W, 3), dtype=np.uint8)
    cores = max(1, multiprocessing.cpu_count() - 1)
    with multiprocessing.Pool(cores) as pool:
        for i, (py, row) in enumerate(pool.imap_unordered(_compute_row, args, chunksize=4)):
            pixels[py] = row
            if i % (H // 10) == 0:
                print(f"  {i*100//H}%…", flush=True)

    print("  100% — saving…")
    os.makedirs(out_dir, exist_ok=True)
    date_tag = f"{nm_dt.year:04d}{nm_dt.month:02d}{nm_dt.day:02d}"
    fname = os.path.join(out_dir, f"vis_n{night}_{date_tag}.png")
    Image.fromarray(pixels, 'RGB').save(fname)
    print(f"Saved: {fname}")
    return fname


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        generate_map(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) >= 4 else 1)
    else:
        # Default: Rabi I 1448 Night 1
        generate_map("2026-08-12T17:37:11",
                     "G:/My Drive/Misbah Library/Misbah Website/moonsighting/maps", 1)
