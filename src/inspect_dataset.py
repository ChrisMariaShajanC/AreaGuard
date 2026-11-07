"""Inspect the Kerala Landslide Inventory 2018 shapefile.

This script reads the real downloaded dataset (no synthetic data) and reports
basic structural information, data quality checks, and saves a simple map.

Run from the project root:
    python src/inspect_dataset.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SHAPEFILE = PROJECT_ROOT / "data" / "raw" / "kerala_landslide_2018" / "Kerela landslide.shp"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


def main():
    if not SHAPEFILE.exists():
        raise FileNotFoundError(f"Dataset not found: {SHAPEFILE}")

    gdf = gpd.read_file(SHAPEFILE)

    print("=== Kerala Landslide Inventory 2018 — Inspection ===")
    print(f"Source file: {SHAPEFILE}")
    print(f"Record count: {len(gdf)}")
    print(f"Geometry type(s): {gdf.geom_type.value_counts().to_dict()}")
    print(f"CRS: {gdf.crs}")
    print(f"Columns ({len(gdf.columns)}): {list(gdf.columns)}")
    print()

    print("=== Attribute dtypes ===")
    print(gdf.dtypes.to_string())
    print()

    print("=== Missing values per column ===")
    print(gdf.isna().sum().to_string())
    print()

    # Duplicate rows (all attributes + geometry)
    dup_count = gdf.duplicated().sum()
    print(f"Duplicate rows (full row): {dup_count}")
    # Duplicate geometries
    geom_dup = gdf.geometry.duplicated().sum()
    print(f"Duplicate geometries: {geom_dup}")
    print()

    # Invalid geometries
    invalid_mask = ~gdf.geometry.is_valid
    invalid_count = int(invalid_mask.sum())
    print(f"Invalid geometries: {invalid_count}")
    if invalid_count > 0:
        print("Invalid geometry indices (first 20):", list(gdf.index[invalid_mask][:20]))
    print()

    # Empty geometries
    empty_count = int(gdf.geometry.is_empty.sum())
    print(f"Empty geometries: {empty_count}")
    print()

    # Bounds
    print("=== Spatial bounds (minx, miny, maxx, maxy) ===")
    print(tuple(float(x) for x in gdf.total_bounds))
    print()

    # Basic numeric summary for non-geometry columns
    numeric_cols = gdf.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        print("=== Numeric column summary ===")
        print(gdf[numeric_cols].describe().to_string())
        print()

    # Save a simple map
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 8))
    gdf.plot(ax=ax, markersize=2, color="red", alpha=0.6)
    ax.set_title("Kerala Landslide Inventory 2018 — Landslide Locations")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    out_path = FIGURES_DIR / "kerala_landslide_locations.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Map saved to: {out_path}")


if __name__ == "__main__":
    main()
