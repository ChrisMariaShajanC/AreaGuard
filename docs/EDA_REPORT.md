# Exploratory Data Analysis Report - Kerala Landslide Inventory 2018 (Day 4)

All findings below come from the real downloaded dataset at
`data/raw/kerala_landslide_2018/`. No synthetic data, fake labels, or
predictions were created. Original dataset files were not modified, and no
records were removed.

## 1. Dataset Overview

- **Source file:** `data/raw/kerala_landslide_2018/Kerela landslide.shp`
- **Records:** 4,728
- **Geometry:** Point (all 4,728 records)
- **CRS:** EPSG:4326 (WGS 84, decimal degrees)
- **Encoding:** UTF-8
- **Attribute columns (21, incl. geometry):**
  `No, District, NRSC, GSI, New, Type_of_sl, Length, Width, Area, Building_I,
  Road_impac, Impact_Agr, LU_2010, LU_2018, Specific_r, Remarks, POINT_X,
  POINT_Y, Reclass_Sl, RASTERVALU, geometry`
- **Spatial bounds:** longitude 75.0154-77.3963; latitude 8.4745-12.6550
  (within Kerala).
- **Reusable script:** `src/eda.py`
- **Charts:** `reports/figures/` (see Section 4)

Verified against Day 3 inspection: record count (4,728), column list (21),
CRS (EPSG:4326), geometry (Point), and missing-value counts (Specific_r 3,864;
Remarks 3,698) all match.

## 2. Analysis Findings

### 2.1 Landslide counts by district

| District | Count | Share |
|---|---:|---:|
| Idukki | 2,223 | 47.0% |
| Palakkad | 793 | 16.8% |
| Malappuram | 429 | 9.1% |
| Wayanad | 331 | 7.0% |
| Thrissur | 256 | 5.4% |
| Kozhikode | 228 | 4.8% |
| Kannur | 141 | 3.0% |
| Ernakulam | 107 | 2.3% |
| Pathanamthitta | 106 | 2.2% |
| Kottayam | 76 | 1.6% |
| Kasaragod | 24 | 0.5% |
| Kollam | 10 | 0.2% |
| Thiruvananthapuram | 4 | 0.1% |
| **Total** | **4,728** | **100%** |

Idukki alone contributes 47.0% of all recorded landslides.

### 2.2 Distribution of landslide types

| Type_of_sl | Meaning | Count | Share |
|---|---|---:|---:|
| DF | Debris flow | 2,816 | 59.6% |
| SS | Surficial slide | 1,760 | 37.2% |
| RF | Rock fall | 152 | 3.2% |
| **Total** | | **4,728** | **100%** |

Rock falls are concentrated in Idukki (123 of 152).
"""
### 2.3 Area, length and width distributions

**Area (m^2):** 4,308 records have Area > 0; 420 have Area = 0.

| Statistic | All records (n=4,728) | Non-zero (n=4,308) |
|---|---:|---:|
| Min | 0.00 | 16.00 |
| 25th percentile | 479.38 | 633.45 |
| Median | 1,162.79 | 1,341.08 |
| Mean | 8,121.06 | 8,912.81 |
| 75th percentile | 2,768.61 | 3,089.89 |
| 90th percentile | - | 7,367.70 |
| 99th percentile | - | 33,413.26 |
| Max | 23,887,853.00 | 23,887,853.00 |
| Std. dev. | 347,449.33 | 363,986.50 |

Distribution is strongly right-skewed; one NRSC polygon record in Palakkad
has Area = 23,887,853 m^2 (approx. 23.9 km^2), which dominates district area
totals.

**Length (m), non-zero records (n=1,659):** min 4, median 65, mean 131.6,
95th pct 434.4, max 3,138.

**Width (m), non-zero records (n=1,659):** min 2, median 13, mean 17.4,
95th pct 42.0, max 306.

### 2.4 Zero-valued measurements

- `Area == 0`: 420 records (8.9%).
- `Length == 0` and `Width == 0`: 3,069 records (64.9%).
- Every `Area == 0` record also has `Length == 0` and `Width == 0`.
- No record has `Area == 0` while `Length > 0`.
"""
### 2.5 Missing values in all columns

| Column | Missing | Present |
|---|---:|---:|
| Specific_r | 3,864 | 864 |
| Remarks | 3,698 | 1,030 |
| All other 19 columns | 0 | 4,728 |

### 2.6 Land-use categories in 2010 and 2018

24 distinct codes occur in `LU_2010`; 25 in `LU_2018` (the extra code `QUA`
appears once in 2018 and is **not defined** in the metadata PDF).

Most common categories (counts):

| Code | Meaning | LU_2010 | LU_2018 |
|---|---|---:|---:|
| FMP | Mixed forest plantation | 1,227 | 1,185 |
| FDN | Dense Natural Forest | 1,142 | 1,103 |
| SPL | Shrub plantation | 424 | 422 |
| BRF | Bare Rock with isolated forests | 382 | 387 |
| BUI | Buildings | 258 | 334 |
| FNO | Open Natural Forest | 231 | 243 |

- Records whose land use changed between 2010 and 2018: **707 (14.9%)**.
- Top transitions: FMP->SPL (70), SPL->FMP (69), FMP->BUI (44),
  FDN->FNO (39), GMC->SPL (34).
- Net changes: Buildings (BUI) +76; Mixed forest plantation (FMP) -42;
  Dense natural forest (FDN) -39; Forest plantation (FCP) -27.
- `Impact_Agr` (agriculture impact) values: N (no impact) 2,534; FMP 1,194;
  SPL 433; TEA 176; FCP 162; GMC 101; BSL 72; RUB 56.
"""
### 2.7 NRSC, GSI and newly mapped source distributions

| Source flag | Y (mapped) | N (not mapped) |
|---|---:|---:|
| NRSC | 2,899 | 1,829 |
| GSI | 1,395 | 3,333 |
| New (authors) | 856 | 3,872 |

The three flags form four mutually exclusive groups:

| NRSC | GSI | New | Count | Interpretation |
|---|---|---|---:|---|
| Y | N | N | 2,477 | NRSC only |
| N | Y | N | 973 | GSI only |
| Y | Y | N | 422 | NRSC + GSI overlap |
| N | N | Y | 856 | Newly mapped by authors |

### 2.8 Geographic distribution of landslide points

- 4,728 points spread across 13 Kerala districts; bounds above.
- Idukki has the largest count (2,223) and the most rock falls (123).
- Palakkad has the largest summed landslide area (approx. 26.75 million m^2),
  driven by one very large NRSC polygon (23.89 million m^2).
- Type-colored point map: `reports/figures/kerala_landslide_by_type.png`.

Additional per-district detail (counts of types) is available in the EDA
script output.
"""
## 3. Data Quality Observations

### 3.1 Why Area is zero in 420 records

All 420 `Area == 0` records are in the **GSI-only** group
(NRSC = N, GSI = Y, New = N) and also have `Length = Width = 0`.

Per the metadata PDF, `Area` (m^2) is either the area of an **NRSC polygon**
or **Length x Width**. For these 420 GSI-only records there is no NRSC
polygon and no length/width measurement, so no area can be computed; the
value is recorded as 0. This is therefore best interpreted as a **missing /
not-computed measurement**, not a genuine zero-area landslide (a landslide
cannot have zero area).

Caveat: the metadata PDF does **not** explicitly define 0 as a sentinel for
missing. Additionally, 84 GSI-only records have `Area > 0` despite
`Length = Width = 0`, which suggests either a GSI-provided area not
described in the metadata or inconsistent data entry. The exact convention
cannot be established from the available metadata, so this remains
**partially unresolved**.

### 3.2 Why Length and Width are zero in 3,069 records

`Length` and `Width` are defined in the metadata as the maximum length/width
measured by **GSI or the authors** using Google Earth's measure tool.

The zero values occur in groups where such measurements were not taken:

| Group | Zero L/W count | Total in group |
|---|---:|---:|
| NRSC only | 2,188 | 2,477 |
| NRSC + GSI overlap | 366 | 422 |
| GSI only | 504 | 973 |
| Newly mapped (authors) | 11 | 856 |
| **Total** | **3,069** | **4,728** |

NRSC-mapped landslides carry an NRSC polygon area but no Google-Earth
length/width measurement, hence 0. These zeros represent **unmeasured**
dimensions, not genuine zero-sized landslides. A small number of exceptions
(11 newly mapped; 84 GSI-only with positive Area) indicate inconsistent
handling of missing measurements.
"""
### 3.3 Missing values in Specific_r and Remarks

- `Specific_r` (reason codes) is missing in 3,864 of 4,728 records (81.7%);
  only 864 present (18.3%), of which 782 (90.5% of present) are in Idukki.
- `Remarks` is missing in 3,698 (78.2%); 1,030 present (21.8%).
- Both are free-text / optional descriptive fields, so missingness is
  expected and should not be treated as an error.
- `Specific_r` raw values are not strictly single-coded: 53 of 864 present
  records contain multiple slash-separated codes (e.g. `1/2`, `3/10`).
  Single-code occurrence counts: code 2 (road cutslope failure) 305,
  code 1 (building cutslope failure) 292, code 10 (margin between land uses)
  147, code 5 (river undercutting) 66, code 4 (reactivation) 46,
  code 3 (inadequate drainage) 37, code 6 (reservoir) 11, code 8 (tea
  clearing) 6, code 7 (deforestation) 5, code 9 (rubber clearing) 2.

### 3.4 Other data-quality observations

- **`No` is not a unique identifier:** only 2,501 unique values among
  4,728 records (2,227 duplicates). It appears to be a local/sequence
  number, not a primary key. Do not use it as an ID.
- **Undefined land-use code:** `LU_2018` contains `QUA` (1 record) which is
  not defined in metadata Table 1 (defined code is `QUU` = Quarry in use).
  Likely a typo or an undocumented code.
- **Area outlier:** one NRSC polygon record (Palakkad, DF) has
  Area = 23,887,853 m^2, approx. 2,680x the median non-zero area. Verify
  before modeling.
- **`RASTERVALU` (slope, degrees):** mean 25.19, range 0.0-87.87;
  6 records have slope 0.0 (likely flat/interpolation artifacts).
- **`Building_I`:** 0 for 4,083 records (86.4%); positive for 645 (13.6%),
  max 23, mean 0.199. Heavy zero-inflation.
- **Correlation:** `Reclass_Sl` and `RASTERVALU` are nearly identical
  (r = 0.981); `POINT_X` and `POINT_Y` are strongly correlated (r = -0.939)
  due to Kerala's NW-SE orientation.
- **Source flags are mutually exclusive** in practice (four groups above);
  they may encode mapping source rather than physical susceptibility and
  should be used cautiously as ML features.

## 4. Charts Generated

Saved under `reports/figures/`:

1. `landslide_count_by_district.png` - district-wise landslide count (bar).
2. `landslide_type_distribution.png` - landslide type distribution (bar).
3. `area_distribution.png` - area distribution, log scale (histogram).
4. `length_width_distribution.png` - length and width distributions (histograms).
5. `landuse_comparison.png` - land-use category counts, 2010 vs 2018 (grouped bar).
6. `data_source_distribution.png` - records by mapping source (bar).
7. `kerala_landslide_by_type.png` - geographic distribution colored by type (scatter).
8. `kerala_landslide_locations.png` - all landslide points (from Day 3).
"""
## 5. Potentially Useful ML Features

- Location: `POINT_X`, `POINT_Y`, `District` (categorical), spatial bins.
- Landslide size: `Area`, `Length`, `Width` with missingness indicators
  (`Area == 0`, `Length == 0`) - do not silently impute.
- Impacts: `Building_I`, `Road_impac`, `Impact_Agr`.
- Land use: `LU_2010`, `LU_2018`, and a land-use-change flag.
- Topography: `Reclass_Sl`, `RASTERVALU` (slope).
- Source flags: `NRSC`, `GSI`, `New` (use cautiously; may reflect mapping
  coverage).
- Reason codes: `Specific_r` (sparse; multi-code; mostly Idukki).
- Target definition is not yet finalized; this dataset is a positive-only
  inventory (landslide points). Susceptibility mapping will require
  generating absence (non-landslide) samples in a later step.

## 6. Limitations and Unresolved Questions

- Single-event inventory (2018 monsoon); no multi-year temporal coverage.
- Point geometries only; polygon footprints are not in this shapefile
  (area is an attribute, partly NRSC-derived).
- No absence samples; cannot train a classifier without sampling non-landslide
  locations.
- Zero conventions for `Area`, `Length`, `Width` are not defined in the
  metadata PDF; interpreted here as missing/unmeasured based on source flags
  and field definitions, with noted exceptions.
- `Specific_r` and `Remarks` are largely missing and spatially biased
  (Idukki).
- Undefined `QUA` land-use code (1 record).
- `No` is not a reliable key.
- One extreme area outlier (23.89 million m^2) needs verification.
- Area is given in m^2 but coordinates are in degrees; no projection metadata
  for recomputing areas is available in this dataset.
- No models trained and no predictions generated in this step.
"""