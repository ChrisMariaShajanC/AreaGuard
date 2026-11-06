# Dataset Selection — AreaGuard (Day 2)

## Recommendation

### Primary Dataset (Recommended)
**Kerala Landslide Inventory 2018** (University of Twente / DANS)
- Source: https://research.utwente.nl/en/datasets/landslide-inventory-of-the-2018-monsoon-rainfall-in-kerala-india/
- Reason: Directly matches the target region (Kerala) and provides 4,728 labeled landslide locations with attributes (district, landslide type, area, land use 2010/2018). Suitable as the core positive-sample source for Kerala landslide susceptibility mapping.
- Status: **Proposed/confirmed available via source page; not yet downloaded.**

### Supplementary Datasets (Recommended)
1. **NRSC/ISRO Landslide Atlas** (~80,000 landslides, 1998–2022)
   - Use: Supplement with additional landslide locations, especially event-based entries relevant to Kerala disasters; support multi-year coverage.
   - Status: **Proposed; download/access terms to be confirmed.**

2. **USGS SRTM (Elevation/Terrain)**
   - Use: Terrain features (elevation, slope, aspect, curvature, TWI, TRI).
   - Status: **Proposed; resolution/access to be verified.**

3. **NASA GPM IMERG (Rainfall)**
   - Use: Rainfall triggering features.
   - Status: **Proposed; product details to be verified.**

4. **Global Flood Database v1 (Alternative/Secondary)**
   - Use: Multi-hazard context; flood extent/duration features if relevant.
   - Status: **Confirmed available via Google Earth Engine (requires account); not yet downloaded.**

---

## Confirmed Availability vs. Proposed Verification

- **Confirmed available (per source page):** Kerala Landslide Inventory 2018 (DANS access link provided); Global Flood Database v1 (Earth Engine).
- **Proposed, requiring download and verification:** NRSC/ISRO Landslide Atlas (access terms unclear), USGS SRTM (page not rendered in this pass), NASA GPM IMERG (page not fetched in this pass).

No datasets have been downloaded. No models trained. Threat categories remain to be validated against real data.

---

## Next Steps (Future Days)

1. Download and inspect the Kerala Landslide Inventory 2018 (with approval).
2. Verify NRSC access and extract Kerala-relevant entries.
3. Verify and acquire terrain and rainfall sources.
4. Validate data quality before defining final threat categories and features.
