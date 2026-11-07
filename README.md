# AreaGuard

**AI-Based Area-Specific Human & Environmental Threat Prediction and Advisory System**

AreaGuard is a Machine Learning project that aims to estimate potential human and environmental threats for selected geographical areas using real geographical, environmental, and historical data. The system is intended to support data-driven risk awareness and advisory insights for specific locations.

> Status: Day 1 — Project initialization only. No datasets have been collected yet and no machine learning models have been trained.

---

## Problem Statement

Communities and decision-makers often lack a localized, data-driven view of potential human and environmental threats for a given area. Threats such as natural hazards, environmental degradation, and human-related risks can vary significantly by location, but available information is frequently fragmented, historical, or not area-specific.

AreaGuard addresses this gap by proposing a system that aggregates geographical, environmental, and historical information for a selected area and uses Machine Learning to estimate potential risks, then presents the results as clear, area-specific advisories.

---

## Project Objectives

- Collect and validate real geographical, environmental, and historical datasets relevant to area-specific threats.
- Explore and understand the data through exploratory data analysis (EDA).
- Define and validate threat categories based on the available data rather than assumptions.
- Engineer meaningful features that capture location, environment, and historical patterns.
- Train and evaluate Machine Learning models to estimate potential risks for selected areas.
- Provide clear, area-specific risk predictions and advisory outputs.
- Keep the workflow reproducible, documented, and beginner-friendly.

---

## Proposed System Workflow

The intended end-to-end workflow (to be implemented in later stages) is:

1. **Data Collection** — Gather real geographical, environmental, and historical data from reliable sources.
2. **Data Validation** — Check data quality, completeness, consistency, and suitability before any modeling.
3. **Data Preprocessing** — Clean, transform, and prepare data for analysis and modeling.
4. **Exploratory Data Analysis (EDA)** — Understand distributions, correlations, and patterns.
5. **Feature Engineering** — Create features that represent area-specific risk factors.
6. **Threat Category Definition** — Finalize threat categories based on validated data.
7. **Model Training & Evaluation** — Train and evaluate ML models; compare approaches.
8. **Risk Prediction** — Generate area-specific risk estimates.
9. **Advisory Output** — Present results as human-readable, area-specific advisories.

> Note: Steps beyond data collection and validation are planned and will be implemented in future development days.

---

## Planned Technology Stack

- **Language:** Python
- **Data Handling:** pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Machine Learning:** scikit-learn
- **Notebooks:** Jupyter
- **Version Control:** Git / GitHub
- **Documentation:** Markdown

Additional tools (e.g., for data acquisition, backend services, or frontend dashboards) may be added later as the project evolves. No frontend, chatbot, or backend is built at this stage.

---

## Planned Project Structure

```
AreaGuard/
├── data/
│   ├── raw/            # Original, unmodified downloaded datasets (not committed if large)
│   └── processed/      # Cleaned and transformed datasets
├── notebooks/          # Jupyter notebooks for EDA and experiments
├── src/                # Reusable Python source code (data loading, features, models)
├── models/             # Saved/trained model artifacts (created later)
├── reports/            # Generated reports, figures, and analysis outputs
├── docs/               # Project documentation
├── requirements.txt    # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## Current Development Status

- **Day 1 — Project Initialization (current):** Repository reviewed, project structure created, documentation drafted, and dependency list defined.
- No datasets have been collected or validated yet.
- No threat categories have been finalized.
- No machine learning models have been trained and no predictions have been generated.
- No frontend, chatbot, or backend has been built.

Future days will focus on data collection, validation, exploratory analysis, and (later) modeling.

---

## Day 2 Progress — Dataset Research & ML Problem Definition

- Primary research direction set to **Kerala landslide susceptibility mapping**.
- Candidate datasets researched and documented in `docs/DATASET_RESEARCH.md`.
- ML problem defined (binary classification, features, metrics, leakage risks) in `docs/ML_PROBLEM_DEFINITION.md`.
- Dataset selection and verification status documented in `docs/DATASET_SELECTION.md`.
- No datasets downloaded, no models trained, no predictions generated.
## Day 3 Progress — Dataset Inspection

- Inspected the real Kerala Landslide Inventory 2018 shapefile (`data/raw/kerala_landslide_2018/`).
- Confirmed 4,728 point records, CRS EPSG:4326, 21 attribute columns.
- Checked missing values, duplicates, invalid/empty geometries (none invalid/empty; 2 columns have many missing values).
- Extracted and summarized metadata from `metadata.pdf` (attribute definitions, land-use and reason codes).
- Generated a point map: `reports/figures/kerala_landslide_locations.png`.
- Findings documented in `docs/DATASET_INSPECTION.md`.
- Inspection script: `src/inspect_dataset.py`.
- No original dataset files modified; no models trained; no predictions generated.

---


---

---

## Getting Started

1. Clone the repository.
2. Create/activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch Jupyter:
   ```bash
   jupyter notebook
   ```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

