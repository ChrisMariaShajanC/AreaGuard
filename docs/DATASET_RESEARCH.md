# Dataset Research — AreaGuard (Day 2)

## Purpose

This document records candidate datasets considered for the AreaGuard project's primary research direction: **Kerala landslide susceptibility mapping**. It summarizes what is currently known (verified from source pages where possible) and what still requires download/verification.

No datasets have been downloaded, and no models have been trained. Details that could not be verified are explicitly marked as **"to be verified"** rather than invented.

---

## 1. Kerala Landslide Inventory 2018

- **Source URL:** https://research.utwente.nl/en/datasets/landslide-inventory-of-the-2018-monsoon-rainfall-in-kerala-india/
- **Dataset purpose:** Landslide inventory for the 2018 monsoon rainfall event in Kerala, India; intended to study whether triggered landslides relate to recent land-use changes.
- **Geographic coverage:** State of Kerala, India (geospatial point reported: 9.364058, 76.629618).
- **Temporal coverage:** 1 Jun 2018 – 26 Aug 2018 (event period); dataset made available 2 Apr 2020.
- **Reported size (verified):** 4,728 landslides.
- **Available attributes (verified):** district, data source, landslide type, landslide area, land use in 2010, land use in 2018, etc.
- **Spatial/temporal resolution:** Not explicitly stated on the source page; to be verified from the downloaded data/metadata.
- **Access method:** Dataset hosted via DANS (DATA Archiving and Networked Services); persistent identifier (DOI 10.17026/dans-x6c-y7x2) and access link provided on the source page.
- **Potential ML usefulness:** Provides labeled landslide locations (positive samples) for the target region; attributes support feature engineering (land use change, district, landslide type/area).
- **Limitations:** Covers a single extreme event period; spatial/temporal resolution not stated on the page; may need merging with other inventories for broader coverage; license/terms to be confirmed.

---

## 2. NRSC/ISRO Landslide Atlas

- **Source URL:** https://www.nrsc.gov.in/nrscnew/resources_atlas_landslide.php
- **Dataset purpose:** Geospatial landslide inventory database and atlas for landslide provinces of India, including damage assessment at specific locations and district-level exposure ranking.
- **Geographic coverage:** Landslide-vulnerable regions in 17 states and 2 UTs of India (Himalayas and Western Ghats).
- **Temporal coverage:** 1998–2022 (seasonal, event-based, and route-wise inventories).
- **Reported size (verified):** Approximately 80,000 landslides.
- **Available attributes (verified):** Three inventory types — seasonal (2014 and 2017 rainy seasons, pan-India), event-based (major triggering events such as Kedarnath, Kerala disasters, Sikkim earthquake, valley-blocking landslides), and route-wise (selected tourist/pilgrimage routes). District-level exposure ranking for 147 districts using socio-economic parameters. Satellite/aerial imagery sources used for mapping listed on the page.
- **Spatial/temporal resolution:** Mapping used high to very high resolution satellite data (IRS-1D PAN+LISS-III, Resourcesat-1/2/2A LISS-IV Mx, Cartosat-1/2S, Sentinel-1&2, Pleiades, WorldView) and aerial images; landslide feature resolution not quantified on the page. To be verified from downloadable data.
- **Access method:** Informational atlas page; "Click here to view Landslide Atlas" link on the page. Download/access terms to be confirmed.
- **Potential ML usefulness:** Larger, multi-year inventory could supplement the Kerala 2018 inventory; event-based entries relevant to Kerala disasters.
- **Limitations:** Access/download format not specified on the page; coverage is broader than Kerala; validation methods (field/mobile app and news reports) noted but details limited; data terms to be confirmed.
---

## 3. NASA GPM IMERG (Rainfall)

- **Source URL:** https://gpm.nasa.gov/data/directory (IMERG-specific page could not be fetched in this pass)
- **Dataset purpose:** Precipitation/rainfall data intended as an environmental feature source for AreaGuard (e.g., rainfall intensity/duration as landslide triggers).
- **Geographic coverage:** Global (planned).
- **Temporal coverage:** To be verified from source documentation.
- **Reported size:** Not applicable / to be verified.
- **Available attributes:** Precipitation estimates (details to be verified).
- **Spatial/temporal resolution:** To be verified from source documentation (not confirmed in this pass).
- **Access method:** To be confirmed from the source (NASA GPM data portal). Not downloaded.
- **Potential ML usefulness:** Rainfall is a key triggering factor for landslides; supports feature engineering.
- **Limitations:** Resolution, latency, format, and access terms not verified in this pass. Requires download and verification before use. Do not assume specific resolution values.

> Note: The IMERG product page could not be fetched during this research pass. Only the source URL is recorded; all product details must be verified later.

---

## 4. USGS SRTM (Elevation/Terrain)

- **Source URL:** https://www.usgs.gov/faqs/where-can-i-get-global-elevation-data
- **Dataset purpose:** Global elevation data intended for terrain feature engineering (slope, aspect, elevation, etc.) for landslide susceptibility.
- **Geographic coverage:** Global (planned).
- **Temporal coverage:** Static terrain product (not time-series); to be confirmed.
- **Reported size:** Not applicable / to be verified.
- **Available attributes:** Elevation (and derived terrain metrics to be computed by us).
- **Spatial/temporal resolution:** To be verified from source documentation (not confirmed in this pass).
- **Access method:** To be confirmed from the source (USGS EarthExplorer / LP DAAC). Not downloaded.
- **Potential ML usefulness:** Elevation and derived slope/aspect are standard landslide susceptibility features.
- **Limitations:** Resolution, coverage gaps, and access terms not verified in this pass. Requires download and verification before use. Do not assume specific resolution values.

> Note: The USGS page could not be rendered during this research pass (JavaScript required). Only the source URL is recorded.

---

## 5. Global Flood Database (Alternative Flood-Related Dataset)

- **Source URL:** https://developers.google.com/earth-engine/datasets/catalog/GLOBAL_FLOOD_DB_MODIS_EVENTS_V1
- **Dataset purpose:** Maps of flood extent and inundation duration for flood events; considered as an alternative/secondary environmental hazard dataset.
- **Geographic coverage:** Global (-90 to 90 lat, -180 to 180 lon).
- **Temporal coverage:** 2000-02-17 to 2018-12-10.
- **Reported size (verified):** 913 flood events; 12,719 MODIS scenes (Terra and Aqua) used.
- **Available attributes (verified):** maximum flood extent ("flooded" band), duration of inundation in days ("duration" band), permanent water ("jrc_perm_water" band), clear-view counts ("clear_views"), clear percentage ("clear_perc"). Properties include flood severity, cause, and impact; filterable by date, country, or Dartmouth Flood Observatory ID.
- **Spatial resolution (verified):** 250-meter classification resolution (catalog table lists 30-meter pixel size). To be reconciled/verified on download.
- **Access method:** Google Earth Engine (`ee.ImageCollection("GLOBAL_FLOOD_DB/MODIS_EVENTS/V1")`); Earth Engine account required; free for research/education/nonprofit use per page.
- **Potential ML usefulness:** Could support multi-hazard analysis; flood extent/duration as environmental features.
- **Limitations:** Flood-focused (not landslide); global coverage but event-based; requires Earth Engine access; resolution discrepancy to verify; not yet downloaded.

---

## Summary of Verification Status

| Source | Reported size verified? | Attributes verified? | Resolution verified? | Downloaded? |
|---|---|---|---|---|
| Kerala Landslide Inventory 2018 | Yes (4,728) | Partial (listed) | No | No |
| NRSC/ISRO Landslide Atlas | Yes (~80,000) | Partial (inventory types) | Partial | No |
| NASA GPM IMERG | No | No | No | No |
| USGS SRTM | No | Partial (elevation) | No | No |
| Global Flood Database v1 | Yes (913 events) | Yes | Partial | No |

All sources remain un-downloaded. No synthetic or fake data has been created.

