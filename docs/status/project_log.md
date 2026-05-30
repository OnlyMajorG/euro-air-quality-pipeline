# Project Log

## 2026-05-30

### Phase 0 QA Report Created

- Created `docs/qa/phase0_qa_report.md`.
- Result: PASS WITH MAJOR ISSUES.
- Major finding: notebooks are present but invalid JSON.
- Scope creep assessment: no pipeline implementation or optional platform
  expansion found.

### Agent And Documentation Infrastructure Added

- Added local `agents/` operating instructions for project-specific AI agents.
- Added agent memory and project soul files to keep future AI work aligned.
- Added `agents/` to `.gitignore` because agent memory is local working context.
- Added project status documentation under `docs/status/`.
- Added implementation documentation under `docs/implementation/`.

No data pipeline logic was implemented.

### Phase 0 Notebook Gate Blocker Resolved

- Removed invalid trailing literal `\n` text from all seven placeholder
  notebooks.
- Re-ran notebook JSON validation successfully.
- Did not add notebook execution outputs or pipeline logic.
- Phase 0 gate status changed to Approved for Phase 1.

### Phase 1 Pilot Scope Defined

- Documented Vienna and Berlin as the two Phase 1 pilot cities.
- Documented PM2.5, PM10, and NO2 as the target pollutant scope.
- Updated `docs/data_sources.md` and `notebooks/00_project_scope_and_sources.ipynb`.
- Did not create data files, city reference outputs, station matching, or
  ingestion logic.

### Open-Meteo Phase 1 Feasibility Checked

- Ran one limited Open-Meteo Air Quality API request for Vienna and one for
  Berlin.
- Saved small local JSON evidence files under `data/bronze/open_meteo_raw/`.
- Documented observed fields, units, timestamp assumptions, risks, and source
  status in `docs/data_sources.md`.
- Did not implement a reusable client, Kafka event schema, producer, scheduler,
  or streaming path.

### EEA Phase 1 Feasibility Checked

- Queried EEA station metadata for Vienna and Berlin pilot areas.
- Verified metadata-level availability of at least one target pollutant for both
  pilot cities.
- Documented EEA access paths, expected fields, timestamp uncertainty,
  station-to-city mapping risks, and source status in `docs/data_sources.md`.
- Did not download full EEA historical data, implement ingestion, create
  station matching, run Spark, or write Bronze/Silver/Gold outputs.

### Wikipedia Phase 1 Feasibility Checked

- Fetched Wikipedia HTML for Vienna and Berlin.
- Saved small infobox HTML evidence files under `data/bronze/wikipedia_html/`.
- Documented parseable metadata candidates, HTML structure risks, fallback
  strategy, and source status in `docs/data_sources.md`.
- Added `data/**/*.html` to `.gitignore` so raw/source-spike HTML samples stay
  local unless a later policy explicitly allows committing them.
- Did not implement a production scraper, parser module, crawler, or metadata
  Parquet output.

### Phase 1 Sample Data Hygiene Policy Defined

- Documented allowed local sample types, naming patterns, size expectations,
  and Git policy in `docs/data_sources.md`.
- Verified `.gitignore` protects JSON, HTML, Parquet, CSV, and checkpoint data
  artifacts while preserving `.gitkeep`.
- Did not perform new source requests, downloads, scraping, or pipeline code
  changes.

### Phase 1 Source Feasibility Matrix Created

- Consolidated Open-Meteo, EEA, and Wikipedia findings into one feasibility
  matrix in `docs/data_sources.md`.
- Recorded source formats, key fields, risks, decisions, and Phase 2 readiness.
- Added a small Mermaid source-flow diagram.
- Did not implement city reference data, parser/client code, Kafka, Spark, or
  analytics logic.

### Phase 1 QA Report Created

- Created `docs/qa/phase1_qa_report.md`.
- Phase 1 result: PASS WITH MINOR ISSUES.
- Final decision: Approved for Phase 2.
- Updated project status and phase gate register.
- Did not implement Phase 2 city reference data or any Kafka/Spark/full
  ingestion logic.

### Phase 1 QA Follow-Up Corrections

- Re-reviewed Phase 1 documentation, notebook state, sample hygiene, and scope.
- Updated README to reflect that Phase 1 is complete and Phase 2 may start.
- Replaced corrupted repository tree characters in README with an ASCII tree.
- Updated BDENG requirement mapping wording to distinguish validated
  feasibility from planned later implementation artifacts.
- Did not change source modules, tests, data model outputs, Kafka, Spark, or
  ingestion logic.

### Phase 2.1 City Reference Scope Defined

- Documented exactly 8 starter cities for the Phase 2 city reference model.
- Included Vienna and Berlin from Phase 1.
- Added city names, country codes, coordinates, and selection rationale in
  `docs/data_model.md` and `notebooks/01_city_mapping.ipynb`.
- Did not create city reference output files, download data, call APIs, scrape
  Wikipedia, run Kafka, run Spark, or implement analytics.

### Phase 2.2 City Reference Schema Designed

- Documented the canonical city reference schema in `docs/data_model.md`.
- Defined required and optional fields, data types, nullability, identifier
  convention, and validation constraints for later tests.
- Reviewed `docs/decisions/ADR-003-city-reference-model.md`; the ADR decision
  remains unchanged.
- Did not create city reference output files, download data, call APIs, scrape
  Wikipedia, run Kafka, run Spark, or implement analytics.

### Phase 2.3 Deterministic City Reference Builder Implemented

- Implemented `src/city_mapping/build_city_reference.py` using local Phase 2
  city constants only.
- Added explicit functions to build, validate, and write
  `data/silver/city_reference.csv` and `data/silver/city_reference.parquet`.
- Generated the local CSV and Parquet outputs by explicitly running the module;
  these files remain ignored by the repository data policy.
- Added focused tests in `tests/test_city_mapping.py` for schema, identifiers,
  coordinates, duplicate rejection, and CSV/Parquet write/read.
- Did not call APIs, scrape Wikipedia, download EEA data, run Kafka, run Spark,
  or implement analytics.

### Phase 2.4 City Reference Validation Tests Added

- Expanded `tests/test_city_mapping.py` into integrity tests for required
  columns, required join keys, unique `city_id` values, normalized name
  consistency, country code format, coordinate ranges, minimum city count, and
  Parquet readback.
- Adjusted city reference validation order so malformed country codes and
  normalized names produce precise validation errors before derived `city_id`
  checks.
- Verified tests run locally without internet access, Kafka, Spark, EEA files,
  or Wikipedia HTML.
- Did not call APIs, scrape Wikipedia, download EEA data, run Kafka, run Spark,
  or implement analytics.

### Phase 2.5 EEA Station-To-City Mapping Strategy Documented

- Added an EEA Station Mapping Strategy section to `docs/data_model.md`.
- Documented candidate selection criteria: distance to city reference
  coordinate, PM2.5/PM10/NO2 pollutant coverage, time coverage,
  representativeness, and country/city context consistency.
- Listed required future station mapping fields and fallback behavior.
- Updated `notebooks/01_city_mapping.ipynb` with a concise EEA mapping summary.
- Reinforced that downstream EEA processing must join through `city_id`, not
  free-text city names or station names.
- Did not download EEA files, implement station-radius matching, run Spark, or
  aggregate measurements.

### Phase 2.6 Wikipedia Metadata Join Rules Documented

- Added Wikipedia Metadata Join Rules to `docs/data_model.md`.
- Documented planned contextual metadata fields: population, area, population
  density, page title, URL, coordinates, country context, and metadata notes.
- Defined `city_id` as the join key and free-text Wikipedia fields as
  traceability only.
- Documented null handling and ambiguity handling for missing, conflicting,
  redirected, or disambiguated Wikipedia values.
- Updated `notebooks/01_city_mapping.ipynb` with a concise summary.
- Did not implement an HTML parser, scraping, metadata Parquet output,
  dashboards, or analysis.

### Phase 2.7 Open-Meteo Mapping Rules Documented

- Added Open-Meteo Mapping Rules to `docs/data_model.md`.
- Documented that future Open-Meteo requests must use city reference
  `latitude` and `longitude` for each `city_id`.
- Documented pollutant field mapping: PM2.5 to `pm2_5`, PM10 to `pm10`, and
  NO2 to `nitrogen_dioxide`.
- Documented the Phase 1 UTC timezone assumption and Phase 5 handoff boundary.
- Updated `notebooks/01_city_mapping.ipynb` with a concise summary.
- Did not implement an API client, event schema, Kafka producer, Spark
  streaming job, or API calls.

### Phase 2.8 City Mapping Notebook Updated

- Reworked `notebooks/01_city_mapping.ipynb` into a readable Phase 2
  documentation trail.
- Added sections for Phase 2 scope, deliverables, city reference scope,
  canonical schema, EEA/Wikipedia/Open-Meteo mapping rules, validation
  approach, Phase 2 Definition of Done, and local Parquet readback.
- Kept notebook outputs empty.
- Did not call external services, implement ingestion, run Kafka, run Spark, or
  add large outputs.

### Phase 2 QA Report Created

- Created `docs/qa/phase2_qa_report.md`.
- Phase 2 result: PASS.
- Final decision: Approved for Phase 3.
- Verified P2-AC1 through P2-AC6 from the implementation plan.
- Confirmed `city_reference.parquet` is a stable input for following phases.
- Confirmed no full EEA ingestion, production Wikipedia scraper, Open-Meteo
  client implementation, Kafka producer, Spark Structured Streaming, Gold
  tables, dashboards, or final analytics were implemented in Phase 2.

### Phase 3 Agent Infrastructure — `agents/soul.md` Created

- Created `agents/` directory with `soul.md` — the authoritative operating
  contract for AI agents working on this repository.
- The soul file documents project identity, canonical source-of-truth files,
  absolute rules (scope discipline, gate discipline, repository hygiene,
  `city_id` join discipline, core cities/pollutants, batch/live data separation,
  no import side effects), architecture summary, tech stack, phase map,
  per-phase allowed scope, source file map, notebook map, test map, issue/QA
  conventions, and a list of common agent mistakes.
- `agents/` is already git-ignored by repository policy.

### Phase 3.1 EEA Batch Source Access And Data Policy

- Added `Phase 3 EEA Source Access` section to `docs/data_sources.md`.
- Documented accepted EEA source access paths (download web app, ArcGIS REST
  station service, station-specific Parquet links).
- Documented raw-data policy: large raw EEA files must not be committed; files
  live under `data/bronze/eea/` which is git-ignored.
- Documented naming convention for local EEA files:
  `eea_<station_id>_<pollutant_key>_<year_start>_<year_end>.<ext>`.
- Documented reproducibility contract: station ID, pollutant, year range, and
  download endpoint must be recorded in `docs/data_sources.md` so any reviewer
  can re-download the same source files.
- Documented git-ignore verification command and expected output.
- Updated `notebooks/02_eea_batch_ingestion.ipynb` with Phase 3 scope
  declaration, Issue 3.1 source access summary, and a pending-work table for
  Issues 3.2–3.8.
- Verified all 20 existing tests still pass.
- Verified `git check-ignore -v data/bronze/eea/sample_test.csv` returns the
  expected ignore rule.
- Verified notebook 02 is valid JSON with 0 code outputs.
- Did not download EEA data, implement the EEA loader, run Spark, create Silver
  or Gold outputs, or implement any Wikipedia, Open-Meteo, Kafka, or streaming
  work.

### Phase 3.2 EEA Input Schema And Silver Output Schema

- Added `Phase 3 EEA Batch Ingestion Data Model` section to `docs/data_model.md`.
- Documented EEA source input field expectations: station identity
  (`AirQualityStation`, `AirQualityStationEoICode`), measurement timestamp
  (`DatetimeBegin`, `DatetimeEnd`), pollutant label (`AirPollutant`),
  measured value (`Concentration`), unit (`Unit`), validity flag (`Validity`),
  and station coordinates (for mapping review only).
- Documented pollutant normalisation table: source labels for PM2.5, PM10,
  and NO2 mapped to canonical internal names; all other pollutants excluded.
- Documented Silver output schema for `data/silver/eea_city_daily.parquet`
  with 10 fields: `city_id`, `date`, `pollutant`, `mean_value`, `min_value`,
  `max_value`, `observation_count`, `unit`, `source`, `processing_time_utc`.
- Documented schema constraints and validation rules (non-negative values,
  `city_id` must exist in `city_reference.parquet`, `source = 'eea'` always).
- Added Mermaid data-flow diagram for the EEA Bronze → Silver transformation.
- Documented historical vs. live data separation table and prohibition on
  mixing EEA Silver with Open-Meteo Silver in Phase 3.
- Updated `notebooks/02_eea_batch_ingestion.ipynb` with Issue 3.2 Markdown
  cell covering input fields, pollutant normalisation, Silver schema, and
  separation rule.
- Verified all 20 existing tests still pass.
- Verified notebook 02 is valid JSON with 0 code outputs.
- Did not implement EEA loader, station matching, Spark, Silver Parquet
  output, Open-Meteo client, Kafka, or Gold tables.
### Phase 3.3 EEA Station-To-City Mapping Table

- Created src/city_mapping/build_station_mapping.py with deterministic,
  side-effect-free builder from local constants.
- Implemented uild_station_mapping(), alidate_station_mapping(),
  write_station_mapping(), and _haversine_km() helper.
- Seeded mapping from Phase 1 EEA station metadata observations:
  - ienna_at: AT90TAB (selected), AT90AKC and AT9STEF (candidate).
  - erlin_de: DEBE068 (selected); PM2.5 coverage constraint 2020+ documented.
  - All 6 remaining cities: placeholder entries with candidate status and
    explicit instructions for real station review before Issue 3.4.
- Added 14 new station mapping tests to 	ests/test_city_mapping.py.
  All 29 city mapping tests pass (32 total across all test files).
- Updated docs/data_model.md with Phase 3.3 section: mapping table fields,
  current mapping status per city, unresolved decisions, Berlin PM2.5
  constraint, and scope boundary.
- Updated 
otebooks/02_eea_batch_ingestion.ipynb with Issue 3.3 Markdown
  cell covering mapping structure, station status table, constraints, and DoD.
- Verified: uild_station_mapping() produces 10 rows, 8 cities covered,
  2 selected stations (AT90TAB for vienna_at, DEBE068 for berlin_de).
- Did not download EEA station metadata, implement loader, run Spark, produce
  Silver air quality output, implement Kafka, or build Gold tables.
