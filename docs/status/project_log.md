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
