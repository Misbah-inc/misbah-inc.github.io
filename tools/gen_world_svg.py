"""Download Natural Earth 110m countries GeoJSON and output SVG <path> elements."""
import urllib.request, json, sys

URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
W, H = 800, 400

def xy(lon, lat):
    return (lon + 180) / 360 * W, (90 - lat) / 180 * H

def ring_d(ring):
    pts = []
    for i, coord in enumerate(ring):
        lon, lat = coord[0], coord[1]
        x, y = xy(lon, lat)
        pts.append(f"{'M' if i==0 else 'L'}{x:.2f},{y:.2f}")
    pts.append('Z')
    return ''.join(pts)

def geom_d(geom):
    t = geom['type']
    parts = []
    if t == 'Polygon':
        for ring in geom['coordinates']:
            parts.append(ring_d(ring))
    elif t == 'MultiPolygon':
        for poly in geom['coordinates']:
            for ring in poly:
                parts.append(ring_d(ring))
    return ''.join(parts)

print("Fetching Natural Earth 110m…", file=sys.stderr)
with urllib.request.urlopen(URL, timeout=30) as r:
    data = json.loads(r.read())
print(f"Loaded {len(data['features'])} countries.", file=sys.stderr)

paths = []
for feat in data['features']:
    d = geom_d(feat['geometry'])
    if d:
        paths.append(f'<path d="{d}"/>')

out = '\n'.join(paths)
with open('world_paths.svg.txt', 'w', encoding='utf-8') as f:
    f.write(out)
print(f"Written {len(paths)} paths to world_paths.svg.txt", file=sys.stderr)
print(f"Total chars: {len(out)}", file=sys.stderr)
