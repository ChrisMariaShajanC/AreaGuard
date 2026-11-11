"""Extract terrain features (elevation, slope, aspect) from SRTM 3-arc-second HGT tiles.

Usage:
    python src/extract_terrain_features.py --dem-dir data/raw/srtm --output data/processed/terrain_features.csv

The --dem-dir must contain SRTM .hgt files (big-endian 16-bit, 1201x1201 or
3601x3601 samples). No elevation values are fabricated; missing tiles or
nodata cells become NaN.
"""

from pathlib import Path
import argparse
import math
import re

import numpy as np
import pandas as pd
import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = PROJECT_ROOT / "data" / "raw" / "kerala_landslide_2018" / "Kerela landslide.shp"
SRTM_NODATA = -32768


def parse_hgt(path):
    path = Path(path)
    m = re.match(r"([NS])(\d{2})([EW])(\d{3})\.hgt", path.name, re.IGNORECASE)
    if not m:
        raise ValueError(f"Unrecognised HGT tile name: {path.name}")
    ns, lat_s, ew, lon_s = m.groups()
    lat = int(lat_s)
    lon = int(lon_s)
    if ns.upper() == "S":
        lat = -lat
    if ew.upper() == "W":
        lon = -lon
    south = lat
    west = lon
    size = path.stat().st_size
    if size == 1201 * 1201 * 2:
        n = 1201
    elif size == 3601 * 3601 * 2:
        n = 3601
    else:
        raise ValueError(f"Unexpected HGT size for {path.name}: {size} bytes")
    raw = np.fromfile(path, dtype=">i2")
    if raw.size != n * n:
        raise ValueError(f"Corrupt HGT file: {path.name}")
    arr = raw.reshape((n, n)).astype("float64")
    arr[arr == SRTM_NODATA] = np.nan
    return south, west, n, arr


def load_hgt_directory(directory):
    directory = Path(directory)
    files = sorted(directory.glob("*.hgt")) + sorted(directory.glob("*.HGT"))
    if not files:
        raise FileNotFoundError(f"No .hgt files found in {directory}")
    tiles = {}
    for f in files:
        south, west, n, arr = parse_hgt(f)
        tiles[(south, west)] = (n, arr)
    ns = {v[0] for v in tiles.values()}
    if len(ns) != 1:
        raise ValueError("Mixed SRTM resolutions in tile set")
    n = ns.pop()
    lats = sorted({k[0] for k in tiles})
    lons = sorted({k[1] for k in tiles})
    step = 1.0 / (n - 1)
    lats_desc = sorted(lats, reverse=True)
    rows = (len(lats_desc) - 1) * (n - 1) + n
    cols = (len(lons) - 1) * (n - 1) + n
    mosaic = np.full((rows, cols), np.nan, dtype="float64")
    for (south, west), (nn, arr) in tiles.items():
        r0 = (lats_desc[0] - south) * (n - 1)
        c0 = (west - lons[0]) * (n - 1)
        r0 = int(round(r0))
        c0 = int(round(c0))
        mosaic[r0:r0 + n, c0:c0 + n] = arr
    north = lats_desc[0] + 1.0
    west0 = lons[0]
    return mosaic, north, west0, step, n
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dem-dir", required=True, help="Directory containing SRTM .hgt tiles")
    parser.add_argument("--output", default=str(PROJECT_ROOT / "data" / "processed" / "terrain_features.csv"))
    args = parser.parse_args()

    if not INVENTORY.exists():
        raise FileNotFoundError(f"Inventory not found: {INVENTORY}")

    gdf = gpd.read_file(INVENTORY)
    if gdf.crs is None or gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs("EPSG:4326")

    mosaic, north, west0, step_deg, n = load_hgt_directory(args.dem_dir)

    centre_lat = north - (mosaic.shape[0] * step_deg) / 2.0
    m_per_deg_lat = 111139.0
    m_per_deg_lon = 111139.0 * math.cos(math.radians(centre_lat))
    dx = step_deg * m_per_deg_lon
    dy = step_deg * m_per_deg_lat

    elev = mosaic
    rows, cols = elev.shape
    slope = np.full_like(elev, np.nan)
    aspect = np.full_like(elev, np.nan)
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            a = elev[i - 1, j - 1]; b = elev[i - 1, j]; c = elev[i - 1, j + 1]
            d = elev[i, j - 1];     e = elev[i, j];     f = elev[i, j + 1]
            g = elev[i + 1, j - 1]; h = elev[i + 1, j]; k = elev[i + 1, j + 1]
            if np.isnan([a, b, c, d, e, f, g, h, k]).any():
                continue
            dzdx = ((c + 2 * f + k) - (a + 2 * d + g)) / (8.0 * dx)
            dzdy = ((a + 2 * b + c) - (g + 2 * h + k)) / (8.0 * dy)
            slope[i, j] = math.degrees(math.atan(math.hypot(dzdx, dzdy)))
            asp = math.degrees(math.atan2(dzdy, -dzdx))
            if asp < 0:
                asp += 360.0
            aspect[i, j] = asp

    records = []
    for idx, row in gdf.iterrows():
        lon = float(row["POINT_X"])
        lat = float(row["POINT_Y"])
        if not (west0 <= lon < west0 + cols * step_deg and
                north - rows * step_deg < lat <= north):
            records.append((idx, row.get("No"), lon, lat, np.nan, np.nan, np.nan, "outside_dem_coverage"))
            continue
        c = int(round((lon - west0) / step_deg))
        r = int(round((north - lat) / step_deg))
        if r < 0 or r >= rows or c < 0 or c >= cols:
            records.append((idx, row.get("No"), lon, lat, np.nan, np.nan, np.nan, "outside_dem_coverage"))
            continue
        el = elev[r, c]
        sl = slope[r, c]
        asp = aspect[r, c]
        status = "ok" if not (np.isnan(el) or np.isnan(sl) or np.isnan(asp)) else "nodata"
        records.append((idx, row.get("No"), lon, lat, el, sl, asp, status))

    out = pd.DataFrame(records, columns=[
        "record_index", "No", "POINT_X", "POINT_Y",
        "elevation_m", "slope_deg", "aspect_deg", "coverage_status",
    ])
    out["dem_source"] = "SRTMGL3 90m (HGT)"
    out["dem_resolution_m"] = 90
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    print(f"Wrote {len(out)} records to {out_path}")
    print("Valid elevation:", int(out["elevation_m"].notna().sum()))
    print("Valid slope:", int(out["slope_deg"].notna().sum()))
    print("Valid aspect:", int(out["aspect_deg"].notna().sum()))
    print("Coverage status counts:")
    print(out["coverage_status"].value_counts().to_string())


if __name__ == "__main__":
    main()
