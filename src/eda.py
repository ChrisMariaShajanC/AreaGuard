"""Exploratory Data Analysis (EDA) for the Kerala Landslide Inventory 2018.

Reads the real downloaded shapefile (no synthetic data), computes summary
statistics, and saves charts to reports/figures/.

Run from the project root:
    python src/eda.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SHAPEFILE = PROJECT_ROOT / "data" / "raw" / "kerala_landslide_2018" / "Kerela landslide.shp"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

LANDUSE_NAMES = {
    "BRO": "Bare Rock", "BRG": "Bare Rock with isolated grass",
    "BRS": "Bare Rock with isolated shrubs", "BRF": "Bare Rock with isolated forests",
    "BSL": "Bare farmland", "BSO": "Bare soil", "BSG": "Bare soil with isolated grass",
    "BSS": "Bare soil with isolated shrubs", "BSF": "Bare soil with isolated trees",
    "GNA": "Natural Grass land", "GMC": "Meadows (cultivated grassland)",
    "SNA": "Natural shrub land", "SPL": "Shrub plantation",
    "FNO": "Open Natural Forest", "FDN": "Dense Natural Forest",
    "FCP": "Forest plantation", "FMP": "Mixed forest plantation",
    "TEA": "Tea Plantation", "RUB": "Rubber plantation",
    "CSB": "Bare cut slopes", "CSV": "Vegetated cut slopes",
    "BUI": "Buildings", "ROA": "Road", "QUU": "Quarry in use",
    "QUA": "Quarry (undefined in metadata)",
}

TYPE_NAMES = {"DF": "Debris flow", "SS": "Surficial slide", "RF": "Rock fall"}


def load_data():
    if not SHAPEFILE.exists():
        raise FileNotFoundError(f"Dataset not found: {SHAPEFILE}")
    gdf = gpd.read_file(SHAPEFILE)
    df = pd.DataFrame(gdf.drop(columns="geometry"))
    return gdf, df


def ensure_figures_dir():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def save_fig(fig, name):
    ensure_figures_dir()
    out = FIGURES_DIR / name
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved chart: {out}")
    return out


def plot_district_counts(df):
    counts = df["District"].value_counts().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(9, 7))
    bars = ax.barh(counts.index, counts.values, color="#4C78A8")
    ax.set_title("Kerala Landslide Inventory 2018 - Landslides by District")
    ax.set_xlabel("Number of landslides")
    ax.set_ylabel("District")
    for bar, v in zip(bars, counts.values):
        ax.text(v + 5, bar.get_y() + bar.get_height() / 2, str(v), va="center", fontsize=8)
    fig.tight_layout()
    return save_fig(fig, "landslide_count_by_district.png")


def plot_type_distribution(df):
    counts = df["Type_of_sl"].value_counts().sort_values(ascending=False)
    labels = [f"{c} ({TYPE_NAMES.get(c, c)})" for c in counts.index]
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(labels, counts.values, color=["#E45756", "#4C78A8", "#72B7B2"])
    ax.set_title("Distribution of Landslide Types (Kerala 2018)")
    ax.set_xlabel("Landslide type")
    ax.set_ylabel("Number of landslides")
    total = len(df)
    for bar, v in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 20, f"{v}\n({v/total:.1%})", ha="center", fontsize=9)
    fig.tight_layout()
    return save_fig(fig, "landslide_type_distribution.png")
def plot_area_distribution(df):
    area = df.loc[df["Area"] > 0, "Area"]
    n_zero = int((df["Area"] == 0).sum())
    bins = np.logspace(np.log10(area.min()), np.log10(area.max()), 40)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(area, bins=bins, color="#F58518", edgecolor="black", alpha=0.8)
    ax.set_xscale("log")
    ax.set_title("Distribution of Landslide Area (m^2) - non-zero records")
    ax.set_xlabel("Area (m^2), log scale")
    ax.set_ylabel("Number of landslides")
    ax.text(0.98, 0.95, f"n = {len(area)}\nArea = 0 in {n_zero} records",
            transform=ax.transAxes, ha="right", va="top",
            bbox=dict(boxstyle="round", fc="white", alpha=0.8))
    fig.tight_layout()
    return save_fig(fig, "area_distribution.png")


def plot_length_width_distribution(df):
    length = df.loc[df["Length"] > 0, "Length"]
    width = df.loc[df["Width"] > 0, "Width"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for ax, data, title in [
        (axes[0], length, "Landslide Length (m)"),
        (axes[1], width, "Landslide Width (m)"),
    ]:
        bins = np.logspace(np.log10(data.min()), np.log10(data.max()), 40)
        color = "#54A24B" if "Length" in title else "#B279A2"
        ax.hist(data, bins=bins, color=color, edgecolor="black", alpha=0.8)
        ax.set_xscale("log")
        ax.set_title(f"Distribution of {title} (non-zero)")
        ax.set_xlabel(f"{title}, log scale")
        ax.set_ylabel("Number of landslides")
    fig.tight_layout()
    return save_fig(fig, "length_width_distribution.png")


def plot_landuse_comparison(df):
    codes = sorted(set(df["LU_2010"]).union(set(df["LU_2018"])))
    c10 = df["LU_2010"].value_counts()
    c18 = df["LU_2018"].value_counts()
    v10 = [int(c10.get(c, 0)) for c in codes]
    v18 = [int(c18.get(c, 0)) for c in codes]
    x = np.arange(len(codes))
    w = 0.4
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.bar(x - w / 2, v10, w, label="LU_2010", color="#4C78A8")
    ax.bar(x + w / 2, v18, w, label="LU_2018", color="#F58518")
    ax.set_xticks(x)
    ax.set_xticklabels(codes, rotation=60, ha="right", fontsize=8)
    ax.set_title("Land-Use Category Counts: 2010 vs 2018 (at landslide locations)")
    ax.set_xlabel("Land-use code")
    ax.set_ylabel("Number of landslides")
    ax.legend()
    fig.tight_layout()
    return save_fig(fig, "landuse_comparison.png")
def plot_source_distribution(df):
    labels = ["NRSC-mapped", "GSI-mapped", "Newly mapped (authors)"]
    y_counts = [int((df["NRSC"] == "Y").sum()),
                int((df["GSI"] == "Y").sum()),
                int((df["New"] == "Y").sum())]
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(labels, y_counts, color=["#4C78A8", "#72B7B2", "#E45756"])
    ax.set_title("Landslide Records by Mapping Source (Y counts)")
    ax.set_ylabel("Number of landslides")
    for bar, v in zip(bars, y_counts):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 20, str(v), ha="center", fontsize=10)
    fig.tight_layout()
    return save_fig(fig, "data_source_distribution.png")


def plot_geographic_by_type(gdf):
    type_colors = {"DF": "#E45756", "SS": "#4C78A8", "RF": "#54A24B"}
    fig, ax = plt.subplots(figsize=(7, 9))
    for t in ["DF", "SS", "RF"]:
        sub = gdf[gdf["Type_of_sl"] == t]
        ax.scatter(sub["POINT_X"], sub["POINT_Y"], s=6, alpha=0.6,
                   color=type_colors[t],
                   label=f"{t} - {TYPE_NAMES[t]} (n={len(sub)})")
    ax.set_title("Geographic Distribution of Landslides by Type (Kerala 2018)")
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")
    ax.legend(markerscale=3, fontsize=8)
    ax.set_aspect("equal", adjustable="box")
    fig.tight_layout()
    return save_fig(fig, "kerala_landslide_by_type.png")


def print_summary(gdf, df):
    print("=== EDA Summary - Kerala Landslide Inventory 2018 ===")
    print(f"Records: {len(df)} | Columns: {len(df.columns)} | CRS: {gdf.crs}")
    print(f"Geometry: {gdf.geom_type.value_counts().to_dict()}")
    print(f"Bounds: lon {gdf.total_bounds[0]:.4f}-{gdf.total_bounds[2]:.4f}, "
          f"lat {gdf.total_bounds[1]:.4f}-{gdf.total_bounds[3]:.4f}")
    print("\nMissing values:")
    miss = df.isna().sum()
    print(miss[miss > 0].to_string())
    print("\nDistrict counts:")
    print(df["District"].value_counts().to_string())
    print("\nLandslide types:")
    print(df["Type_of_sl"].value_counts().to_string())
    print("\nArea: zero =", int((df["Area"] == 0).sum()),
          "non-zero =", int((df["Area"] > 0).sum()))
    print("Length/Width: zero =", int((df["Length"] == 0).sum()))
    print("\nSources (Y counts):")
    for c in ["NRSC", "GSI", "New"]:
        print(f"  {c}: Y={(df[c]=='Y').sum()}, N={(df[c]=='N').sum()}")
    print("\nLand use changed 2010->2018:",
          int((df["LU_2010"] != df["LU_2018"]).sum()))


def main():
    gdf, df = load_data()
    print_summary(gdf, df)
    plot_district_counts(df)
    plot_type_distribution(df)
    plot_area_distribution(df)
    plot_length_width_distribution(df)
    plot_landuse_comparison(df)
    plot_source_distribution(df)
    plot_geographic_by_type(gdf)
    print("\nEDA complete.")


if __name__ == "__main__":
    main()
