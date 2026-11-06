# ML Problem Definition — AreaGuard

## Research Direction

Primary research direction: **Kerala landslide susceptibility mapping**.

This document defines the proposed machine learning problem. No models have been trained and no predictions have been generated. The problem definition is a proposal to be refined after datasets are downloaded and validated.

---

## 1. Landslide Susceptibility Mapping

Landslide susceptibility mapping estimates the likelihood that a landslide will occur in a given location based on terrain, environmental, and historical factors. It is typically formulated as a classification problem over spatial units (e.g., pixels, slope units, or grid cells).

AreaGuard proposes to build such a map for Kerala using real landslide inventory data plus terrain and rainfall features.

---

## 2. Problem Formulation: Binary Classification

- **Positive class (1):** Locations (pixels/cells) where a landslide occurred (from inventory).
- **Negative class (0):** Locations where no landslide is recorded/observed.

Goal: Learn a function that predicts the probability of landslide occurrence for each spatial unit, given its features.

---

## 3. Positive and Negative Samples

- **Positive samples:** Landslide locations from a validated inventory (e.g., Kerala Landslide Inventory 2018; possibly supplemented by NRSC event-based entries).
- **Negative samples:** Non-landslide locations sampled from areas without recorded landslides, with care to avoid bias (e.g., sampling from stable terrain, ensuring spatial representativeness).
- **Important:** Negative sampling strategy must be documented and justified; class imbalance is expected and must be handled (e.g., stratified sampling, class weights).

No synthetic samples should be fabricated. Any sampling will be performed only after real data is available.

---

## 5. Proposed ML Algorithms (Candidates)

To be compared during modeling (not trained yet):
- Logistic Regression (baseline, interpretable)
- Random Forest
- Gradient Boosting (e.g., XGBoost/LightGBM, if available)
- Support Vector Machine
- (Optional) Neural networks for spatial data

Algorithm choice will be justified by data size, feature types, and interpretability needs.

---

## 6. Evaluation Metrics

Because landslide data is typically imbalanced and spatial, evaluation should include:
- Accuracy (with caution due to imbalance)
- Precision, Recall, F1-score
- ROC-AUC and PR-AUC
- Confusion matrix
- Spatial cross-validation (to reduce spatial leakage)
- Calibration of predicted probabilities

Metrics will be reported with clear train/validation/test splits.

---

## 7. Spatial Data Integration

- Align all raster/vector layers to a common coordinate reference system (CRS) and grid resolution.
- Combine landslide points with terrain and rainfall rasters via spatial joins/extraction.
- Handle resolution mismatches (resampling) and document choices.
- Preserve spatial metadata for reproducibility and mapping outputs.

---

## 8. Data Leakage Risks

- **Spatial leakage:** Nearby train/test samples may be spatially correlated; use spatial cross-validation.
- **Temporal leakage:** Using future rainfall/land-use to predict past events; ensure features precede the event.
- **Target leakage:** Features derived from the landslide itself (e.g., post-event imagery) must be excluded.
- **Duplicate/near-duplicate samples:** Same landslide represented multiple times.
- **Sampling bias:** Negative samples chosen only from easy (flat) areas.

Mitigations will be documented during modeling.

---

## 9. Limitations of the Proposed System

- Depends on availability and quality of real datasets.
- Single-event inventories (e.g., 2018) may not generalize.
- Susceptibility is not the same as hazard/risk (timing not predicted).
- Resolution and accuracy of terrain/rainfall data constrain output quality.
- Model performance claims must be based on validated experiments, not assumptions.

---

## Status

Day 2 — Problem definition proposed. No data downloaded, no models trained, no predictions made.

## 4. Candidate Features (Proposed)

Terrain features (from elevation data such as SRTM, to be verified):
- Elevation
- Slope
- Aspect
- Curvature (plan/profile)
- Topographic Wetness Index (TWI)
- Terrain Ruggedness Index (TRI)

Environmental features:
- Rainfall intensity/duration (from GPM IMERG, to be verified)
- Land use / land cover (from inventory attributes or external sources, to be verified)
- Distance to roads/rivers (if data available, to be verified)
- Soil type (if data available, to be verified)

Historical features:
- Past landslide occurrence in the area (from inventory)
- Land-use change (2010 vs 2018, from Kerala inventory attributes)

All features are candidates; final feature set depends on data availability and validation.

---
