"""Lightweight AreaGuard dashboard server.

Serves the static frontend and a GeoJSON API derived from the real Kerala
Landslide Inventory 2018 shapefile (original files are not modified).

Run from project root:
    python src/dashboard_server.py
Then open http://127.0.0.1:8000
"""

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import json
import os

_terrain_cache = None


def _num(value):
    if value is None or value == "":
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if v != v:
        return None
    return v


def load_terrain():
    global _terrain_cache
    if _terrain_cache is not None:
        return _terrain_cache
    if not TERRAIN_CSV.exists():
        _terrain_cache = {}
        return _terrain_cache
    result = {}
    with TERRAIN_CSV.open("r", encoding="utf-8", newline="") as f:
        import csv
        for row in csv.DictReader(f):
            try:
                idx = int(row["record_index"])
            except (TypeError, ValueError, KeyError):
                continue
            result[idx] = {
                "elevation_m": _num(row.get("elevation_m")),
                "slope_deg": _num(row.get("slope_deg")),
                "aspect_deg": _num(row.get("aspect_deg")),
                "terrain_status": row.get("coverage_status") or None,
                "dem_source": row.get("dem_source") or None,
            }
    _terrain_cache = result
    return _terrain_cache
import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SHAPEFILE = PROJECT_ROOT / "data" / "raw" / "kerala_landslide_2018" / "Kerela landslide.shp"
TERRAIN_CSV = PROJECT_ROOT / "data" / "processed" / "terrain_features.csv"
WEB_DIR = PROJECT_ROOT / "web"

_geojson_cache = None


def load_geojson():
    global _geojson_cache
    if _geojson_cache is not None:
        return _geojson_cache
    if not SHAPEFILE.exists():
        raise FileNotFoundError(f"Dataset not found: {SHAPEFILE}")
    gdf = gpd.read_file(SHAPEFILE)
    if gdf.crs is None or gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs("EPSG:4326")
    _geojson_cache = json.loads(gdf.to_json())
    terrain = load_terrain()
    for i, feat in enumerate(_geojson_cache["features"]):
        props = feat["properties"]
        t = terrain.get(i, {})
        props["elevation_m"] = t.get("elevation_m")
        props["slope_deg"] = t.get("slope_deg")
        props["aspect_deg"] = t.get("aspect_deg")
        props["terrain_status"] = t.get("terrain_status")
        props["dem_source"] = t.get("dem_source")
    return _geojson_cache


def filter_features(geojson, params):
    district = params.get("district", [None])[0]
    types = params.get("type", [None])[0]
    type_set = set(types.split(",")) if types else None
    features = geojson["features"]
    if district and district != "all":
        features = [f for f in features if f["properties"].get("District") == district]
    if type_set:
        features = [f for f in features if f["properties"].get("Type_of_sl") in type_set]
    return {"type": "FeatureCollection", "features": features}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/landslides":
            try:
                geojson = load_geojson()
                params = parse_qs(parsed.query)
                data = filter_features(geojson, params)
                body = json.dumps(data, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as exc:  # pylint: disable=broad-except
                body = json.dumps({"error": str(exc)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            return
        if parsed.path == "/api/health":
            body = json.dumps({"status": "ok"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/api/terrain":
            terrain = load_terrain()
            available = TERRAIN_CSV.exists()
            if available:
                records = []
                with TERRAIN_CSV.open("r", encoding="utf-8", newline="") as f:
                    import csv
                    for row in csv.DictReader(f):
                        records.append(row)
                body = json.dumps({"available": True, "records": records}, ensure_ascii=False).encode("utf-8")
            else:
                body = json.dumps({"available": False, "records": []}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, format, *args):
        # keep console output minimal
        pass


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"AreaGuard dashboard running at http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
