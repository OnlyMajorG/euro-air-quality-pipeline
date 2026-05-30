# Phase 1 QA Report

## Executive Summary

Overall status: **PASS WITH MINOR ISSUES**

Phase 1 successfully completed the required source spike and feasibility work.
Open-Meteo, EEA, and Wikipedia were each checked for the two pilot cities,
Vienna and Berlin. The findings are consolidated in `docs/data_sources.md`,
including source status, formats, key fields, risks, and a Phase 2 readiness
decision.

Final decision: **Approved for Phase 2**

Phase 2 may start as City Mapping and Reference Model work only. It must not
skip into full ingestion, Kafka producer implementation, Spark Structured
Streaming, or Gold-layer analytics.

## Audit Scope

This QA review covers Phase 1 source feasibility only:

- pilot city and pollutant scope,
- Open-Meteo API feasibility,
- EEA historical data availability feasibility,
- Wikipedia HTML feasibility,
- sample data hygiene,
- consolidated source feasibility matrix,
- Phase 2 gate readiness.

It does not assess actual ingestion, parsing production logic, Kafka runtime,
Spark processing, Bronze/Silver/Gold transformations, or analysis results.

## Checks Performed

- Reviewed `docs/data_sources.md`.
- Reviewed `notebooks/00_project_scope_and_sources.ipynb`.
- Validated all notebooks with Python `json.loads`.
- Validated local Open-Meteo sample JSON files.
- Validated local Wikipedia sample HTML files.
- Checked `data/` folder contents and sample file sizes.
- Checked git ignored files with `git status --short --ignored`.
- Searched for secrets, production claims, optional technologies, and scope
  creep indicators.
- Attempted to run `python -m pytest`.

## Requirement Checklist

| Area | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Pilot scope | PASS | `docs/data_sources.md` defines Vienna and Berlin with coordinates and target pollutants PM2.5, PM10, NO2. | Scope is small and reviewable. |
| Open-Meteo feasibility | PASS | `docs/data_sources.md` documents Open-Meteo as `usable`; local ignored JSON evidence exists for both pilot cities. | Fields include `time`, `pm10`, `pm2_5`, and `nitrogen_dioxide`. |
| EEA feasibility | PASS | `docs/data_sources.md` documents EEA as `usable with constraints`. | Station-to-city mapping is correctly called out as Phase 2 risk. |
| Wikipedia feasibility | PASS | `docs/data_sources.md` documents Wikipedia as `usable with constraints`; local ignored HTML infobox samples exist. | Parser instability and fallback strategy are documented. |
| Source feasibility matrix | PASS | `docs/data_sources.md` contains `Phase 1 Source Feasibility Matrix`. | Includes Source, Status, Format, Key Fields, Risks, and Decision. |
| Phase 2 readiness | PASS | `docs/data_sources.md` states `Go for Phase 2 with constraints`. | Correctly limits Phase 2 to city mapping and reference model. |
| Notebook evidence | PASS | `notebooks/00_project_scope_and_sources.ipynb` is valid JSON with 0 code outputs. | Notebook contains Markdown evidence only. |
| Sample data hygiene | PASS | `.gitignore` ignores `data/**/*.json` and `data/**/*.html`; samples appear as ignored files. | `.gitkeep` files remain trackable. |
| Secrets and credentials | PASS | Repository search did not find hardcoded secrets. | Matches documented hygiene rules. |
| Scope consistency | PASS | Source modules remain placeholders; no Kafka producer, Spark job, full ingestion, parser/client production logic, or Gold layer was implemented. | Mentions of Kafka/Spark are documentation or future-phase placeholders. |
| Tests | MINOR ISSUE | `python -m pytest` failed because `pytest` is not installed in the active interpreter. | Dependency exists in `requirements.txt`; local environment is not prepared. |

## Findings

### Critical

None.

### Major

None.

### Minor

- `python -m pytest` could not run in the active interpreter because `pytest`
  is not installed. Evidence: `No module named pytest`. This is an environment
  readiness issue, not a Phase 1 source feasibility defect.
- Local source-spike evidence files exist under `data/bronze/`. They are small
  and ignored by git as intended, but reviewers should remember that a fresh
  clone will rely on Markdown documentation unless samples are regenerated.

### Positive Observations

- All three required source categories were checked and documented.
- The source matrix is strict about constraints instead of overstating
  readiness.
- EEA is correctly treated as station-based data requiring Phase 2 mapping.
- Wikipedia is correctly treated as unstable contextual metadata, not an
  authoritative statistical source.
- Open-Meteo field naming risks are documented before schema design.
- Phase 1 did not silently expand into Kafka, Spark, ingestion, dashboards, ML,
  or production infrastructure.

## Scope Creep Assessment

Phase 1 remained within scope.

No evidence was found of:

- Kafka producer implementation,
- Spark Structured Streaming implementation,
- full EEA ingestion,
- production Wikipedia scraper,
- reusable Open-Meteo client,
- City Reference model output,
- Bronze/Silver/Gold transformations,
- dashboard framework,
- PostgreSQL, Airflow, dbt, cloud deployment, or ML.

The local JSON and HTML files are small feasibility evidence samples and are
ignored by git. They are not production data assets.

## Data Engineering Readiness Assessment

The repository is ready to begin Phase 2: City Mapping and Reference Model.

The next phase should focus on:

- defining stable `city_id` values,
- deciding the pilot-to-final city list,
- documenting station-to-city mapping rules for EEA,
- carrying forward Open-Meteo field names,
- defining how Wikipedia metadata will be attached or left null.

Phase 2 should not implement full EEA ingestion, Wikipedia parser production
logic, Kafka producer behavior, Spark jobs, or Gold-layer analytics.

## Final Decision

**Approved for Phase 2**

Approval is constrained to Phase 2 City Mapping and Reference Model work.
