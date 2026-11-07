
# Dataset Inspection — Kerala Landslide Inventory 2018 (Day 3)

## 1. Dataset Location

`data/raw/kerala_landslide_2018/`

All findings below come from the actual downloaded files. No synthetic or fake data was created, and the original files were not modified.

---

## 2. Files Present

From `MANIFEST.TXT`, the dataset contains:

| File | Type | Size (bytes) |
|---|---|---|
| Kerela landslide.shp | Shapefile (geometry) | 208,132 |
| Kerela landslide.shx | Shapefile index | 37,924 |
| Kerela landslide.dbf | Attribute table | 13,811,162 |
| Kerela landslide.prj | CRS definition | 145 |
| Kerela landslide.cpg | Codepage (UTF-8) | 5 |
| Kerela landslide.sbn / .sbx | Spatial index | 46,068 / 1,532 |
| Kerela landslide.mif | MapInfo interchange | 247,043 |
| Kerela landslide.mid | MapInfo attributes | 661,853 |
| Kerela landslide.xml | ArcGIS metadata (lineage) | 1,356 |
| metadata.pdf | Attribute documentation | 161,350 |
| easy-migration.zip | Migration bundle | 20,019 |

**Formats identified:**
- **Shapefile** (`.shp/.shx/.dbf/.prj/.cpg/.sbn/.sbx`) — primary, read with geopandas.
- **MapInfo** (`.mif/.mid`) — alternative interchange format of the same data.
- **ArcGIS XML metadata** (`.xml`) — processing lineage (CalculateField steps), not a data dictionary.
- **PDF metadata** (`metadata.pdf`) — human-readable attribute documentation.
- **ZIP** (`easy-migration.zip`) — bundle; not extracted in this inspection.

---

## 3. Shapefile Inspection (via geopandas)

- **Record count:** 4,728 (matches the reported inventory size).
- **Geometry type:** Point (all 4,728 records).
- **CRS:** EPSG:4326 (WGS 84, geographic, decimal degrees) — confirmed from `.prj`.
- **Encoding:** UTF-8 (from `.cpg`).
- **Attribute columns (21):**
  `No, District, NRSC, GSI, New, Type_of_sl, Length, Width, Area, Building_I, Road_impac, Impact_Agr, LU_2010, LU_2018, Specific_r, Remarks, POINT_X, POINT_Y, Reclass_Sl, RASTERVALU, geometry`

---

## 4. Data Quality Checks

- **Missing values (NaN):**
  - `Specific_r`: 3,864 missing (864 present)
  - `Remarks`: 3,698 missing (1,030 present)
  - All other 19 columns: 0 missing.
- **Duplicate full rows:** 0
- **Duplicate geometries:** 0
- **Invalid geometries:** 0
- **Empty geometries:** 0
- **Zero-valued measurements:**
  - `Area == 0`: 420 records
  - `Length == 0`: 3,069 records
  - `Width == 0`: 3,069 records
  (These appear to be records where only NRSC polygon area is available or measurements were not taken; not treated as errors here.)
- **Spatial bounds:** longitude 75.0154 – 77.3963; latitude 8.4745 – 12.6550 (within Kerala).

---

## 5. Attribute Distributions (selected)

**District (top counts):** Idukki 2,223; Palakkad 793; Malappuram 429; Wayanad 331; Thrissur 256; Kozhikode 228; Kannur 141; Ernakulam 107; Pathanamthitta 106; Kottayam 76; Kasaragod 24; Kollam 10; Thiruvananthapuram 4.

**Landslide type (`Type_of_sl`):** DF (debris flow) 2,816; SS (surficial slide) 1,760; RF (rock fall) 152.

**Data sources:** NRSC Y/N = 2,899/1,829; GSI Y/N = 1,395/3,333; newly mapped by authors (New) Y/N = 856/3,872.

**Road impact (`Road_impac`):** N (no impact) 3,831; C (covers road) 625; D (destroys road) 272.

**Building impact (`Building_I`):** 0 for 4,083 records; values >0 for 645 records (max 23).

**Reclassified slope (`Reclass_Sl`):** values 1–9 (946/877/776/703/433/399/269/202/123).

**Slope (`RASTERVALU`, degrees):** min 0.0, max 87.87, mean 25.19.

**Land use 2010/2018:** 24 distinct codes (see metadata.pdf Table 1); mixed forest plantation (FMP) and dense natural forest (FDN) are the most common.

**Reason codes (`Specific_r`):** 10 categories (see metadata.pdf Table 2); mostly missing.

---

## 6. Metadata Summary (from metadata.pdf)

- **District:** Kerala district where landslide occurred.
- **NRSC/GSI/New:** data source flags (Y/N).
- **Type_of_sl:** DF = debris flow, SS = surficial slide, RF = rock fall.
- **Length/Width:** maximum length/width measured in Google Earth (meters).
- **Area:** m²; from NRSC polygon area or length×width.
- **Building_I:** number of buildings impacted.
- **Road_impac:** C = covers road, D = destroys road, N = no impact.
- **Impact_Agr:** agriculture impact; N = none; other codes match land-use codes.
- **LU_2010 / LU_2018:** land use code in 2010/2018.
- **Specific_r:** reason codes 1–10 (cutslope failure, road cutslope, inadequate drainage, reactivation, river undercutting, reservoir, deforestation, tea/rubber clearing, margin between land uses).
- **POINT_X/POINT_Y:** WGS 84 coordinates.
- **Reclass_Sl:** slope groups reclassified by slope degree.
- **RASTERVALU:** slope in degrees from ASTER GDEM via ArcGIS 3D Analyst.

**Land-use codes (Table 1):** BRO, BRG, BRS, BRF, BSL, BSO, BSG, BSS, BSF, GNA, GMC, SNA, SPL, FNO, FDN, FCP, FMP, TEA, RUB, CSB, CSV, BUI, ROA, QUU (24 codes).

The `.xml` file contains ArcGIS processing lineage (CalculateField operations dated 2020-02-17), not a data dictionary.

---

## 7. Map Output

A basic point map of all 4,728 landslide locations was generated from the real coordinates and saved to:

`reports/figures/kerala_landslide_locations.png`

(Generated with matplotlib using the EPSG:4326 coordinates; no data was altered.)

---

## 8. Notes / Limitations

- This is a single-event inventory (2018 monsoon) with point geometries; polygon footprints are not in this shapefile (area is an attribute).
- `Specific_r` and `Remarks` are largely missing; they are optional descriptive fields.
- 420 records have `Area = 0` and 3,069 have `Length/Width = 0`; these should be reviewed during preprocessing, not silently dropped.
- `Building_I` contains a few large values (e.g., 23, 12) and an unusual 0-heavy distribution; verify before modeling.
- No threat categories or ML targets have been defined yet; this inspection only documents the raw data.
- No models trained; no predictions generated.

---

## 9. Additional Dependencies Used in Day 3 Inspection

Beyond `requirements.txt` (Day 1), this inspection used:
- `geopandas` (reads the shapefile; pulls in shapely, pyogrio, pyproj)
- `pypdf` (extracts text from `metadata.pdf`)

`matplotlib` and `pandas` were already in `requirements.txt`.

Install them (if missing) with:
```bash
pip install geopandas pypdf
```

No changes were made to `requirements.txt` per Day 1 scope; consider adding these if the inspection script becomes part of the standard workflow.
