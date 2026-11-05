# Project Scope — AreaGuard

## Overview

AreaGuard is an AI-based area-specific human and environmental threat prediction and advisory system. Its goal is to estimate potential risks for selected geographical areas by combining real geographical, environmental, and historical data with Machine Learning techniques, and to present the results as clear, area-specific advisories.

This document describes the proposed project scope as of Day 1 (initialization). It is a living document and will be refined as data is collected and validated.

## Problem Context

- Threats (natural, environmental, and human-related) vary by location.
- Available information is often fragmented, generic, or not area-specific.
- Decision-makers benefit from localized, data-driven risk awareness.

## Proposed Scope (Planned)

The project intends to cover, in later stages:

1. **Data Collection** — Acquire real geographical, environmental, and historical datasets from reliable sources.
2. **Data Validation** — Assess quality, completeness, consistency, and suitability before any modeling.
3. **Data Preprocessing** — Clean and prepare data for analysis.
4. **Exploratory Data Analysis (EDA)** — Understand distributions, correlations, and patterns.
5. **Feature Engineering** — Build features representing area-specific risk factors.
6. **Threat Category Definition** — Finalize threat categories based on validated data.
7. **Model Development & Evaluation** — Train and evaluate ML models; compare approaches.
8. **Risk Prediction & Advisory** — Generate and present area-specific risk estimates.

## Out of Scope for Day 1

- No datasets have been collected or validated.
- No threat categories have been finalized.
- No machine learning models have been trained.
- No predictions or risk scores have been generated.
- No frontend, chatbot, or backend has been built.

## Important: Dataset Validation Before Threat Categories

Threat categories must NOT be assumed or invented in advance. They should be defined only after:

- Real datasets have been collected.
- Data quality and coverage have been validated.
- Exploratory analysis has revealed which threat-related signals are actually present and reliable.

Prematurely fixing threat categories risks building models on unsupported assumptions. Therefore, threat category selection is explicitly deferred until datasets are validated.

## Data Handling Notes

- Raw (original, unmodified) datasets belong in `data/raw/`.
- Cleaned/transformed datasets belong in `data/processed/`.
- Large downloaded datasets should not be committed to version control (see `.gitignore`).
- No fake or synthetic datasets should be generated for this project.

## Status

Day 1 — Project initialization only. Documentation and structure are in place; no data or models exist yet.
