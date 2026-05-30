# GitHub Issues — Phase 0 bis Phase 3

**Projekt:** `euro-air-quality-pipeline`  
**Strukturentscheidung:** Notebook-only  
**Phasen:**  
- Phase 0 — Notebook-only Repository Refactor  
- Phase 1 — Source Spike & Cluster Check  
- Phase 2 — City Reference Model  
- Phase 3 — EEA Batch Ingestion  

**Ziel dieses Dokuments:**  
Dieses Markdown-Dokument enthält GitHub-Issues für die ersten vier Projektphasen nach dem neuen Notebook-only-Umsetzungsplan. Die Issues sind so formuliert, dass sie direkt in GitHub kopiert werden können.

---

# Phase 0 — Notebook-only Repository Refactor

## Phase 0 Ziel

Das bestehende Repository wird auf eine Notebook-only-Struktur umgebaut. Die Notebooks sind die zentrale Implementierungs- und Dokumentationsform. `src/` und `tests/` werden nicht als primäre Projektstruktur verwendet. Falls bereits nützlicher Code vorhanden ist, muss er vor dem Entfernen oder Archivieren in die passenden Notebooks migriert werden.

## Phase 0 Deliverables

```text
README.md
requirements.txt
.env.example
.env.cluster.example
.gitignore
LICENSE

notebooks/
docs/
data/
presentation/
```

---

# Issue 0.1 — Audit existing repository and preserve useful logic

## Title

`Phase 0.1 — Audit existing repository and preserve useful implementation logic`

## Objective

Inspect the current repository before restructuring it. Identify existing files, folders, notebooks, scripts, tests and documentation. Preserve all useful logic before changing the structure.

## Context

The project is being refactored into a notebook-only implementation because the course requires documentation of each project step in Jupyter notebooks and sharing notebooks in a public GitHub repository.

However, useful existing code must not be lost. If `src/`, `tests/` or previous notebooks contain working logic, that logic must be migrated or documented before removal.

## Requirements

- [ ] Inspect the complete current repository structure.
- [ ] List existing top-level files and folders.
- [ ] Identify whether the repository contains:
  - `src/`
  - `tests/`
  - old notebooks
  - previous documentation
  - data files
  - generated outputs
  - environment files
- [ ] Identify useful code or documentation that should be migrated.
- [ ] Create a short migration note under:

```text
docs/archive/legacy_repo_audit.md
```

- [ ] Do not delete code before documenting what is being removed or migrated.
- [ ] Do not implement new pipeline functionality in this issue.

## Technical Scope

### Included

- Repository inspection
- Migration note
- Preservation of useful logic
- Risk check before refactor

### Excluded

- Full notebook implementation
- Pipeline development
- Kafka/Spark execution
- API calls
- Data downloads

## Acceptance Criteria

- [ ] `docs/archive/legacy_repo_audit.md` exists.
- [ ] Existing relevant files/folders are listed.
- [ ] Useful logic to migrate is identified.
- [ ] Unneeded files are clearly marked as removable or archive-worthy.
- [ ] No useful implementation was deleted without documentation.
- [ ] No unrelated scope was introduced.

## Definition of Done

- [ ] Repository audit completed.
- [ ] Migration decisions are documented.
- [ ] Repository is ready for notebook-only restructuring.

## Recommended labels

```text
phase-0
refactor
repository
qa
priority-high
```

---

# Issue 0.2 — Create notebook-only repository structure

## Title

`Phase 0.2 — Create notebook-only repository structure`

## Objective

Create the target repository structure for the notebook-only project.

## Context

The final project must be documented through Jupyter notebooks. Therefore, the repository must clearly communicate that notebooks are the primary implementation and documentation artifacts.

## Requirements

- [ ] Create or verify the following structure:

```text
notebooks/
docs/
docs/decisions/
docs/qa/
docs/diagrams/
docs/archive/
data/
data/bronze/
data/bronze/eea/
data/bronze/wikipedia_html/
data/bronze/open_meteo_raw/
data/silver/
data/gold/
data/checkpoints/
data/samples/
presentation/
presentation/figures/
```

- [ ] Add `.gitkeep` files to empty data and presentation folders where needed.
- [ ] Ensure generated data folders exist but are ready to be ignored by Git.
- [ ] Do not create `src/` or `tests/` as primary structure.
- [ ] If `src/` or `tests/` already exist, do not delete them until Issue 0.1 is complete.

## Target structure

```text
euro-air-quality-pipeline/
│
├── README.md
├── requirements.txt
├── .env.example
├── .env.cluster.example
├── .gitignore
├── LICENSE
│
├── notebooks/
│   ├── 00_project_scope_and_requirements.ipynb
│   ├── 01_source_spike_and_cluster_check.ipynb
│   ├── 02_city_reference_model.ipynb
│   ├── 03_eea_batch_ingestion.ipynb
│   ├── 04_wikipedia_web_scraping.ipynb
│   ├── 05_open_meteo_api_and_kafka_producer.ipynb
│   ├── 06_spark_structured_streaming_kafka_to_parquet.ipynb
│   ├── 07_gold_layer_and_data_quality.ipynb
│   └── 08_analysis_visualization_and_storytelling.ipynb
│
├── docs/
│   ├── architecture.md
│   ├── data_sources.md
│   ├── cluster_setup.md
│   ├── limitations.md
│   ├── decisions/
│   ├── qa/
│   ├── diagrams/
│   └── archive/
│
├── data/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── checkpoints/
│   └── samples/
│
└── presentation/
    ├── final_storyline.md
    ├── presentation_outline.md
    └── figures/
```

## Acceptance Criteria

- [ ] Target folders exist.
- [ ] Empty folders are preserved with `.gitkeep`.
- [ ] Folder names match the new implementation plan.
- [ ] No unnecessary software package structure is introduced.
- [ ] Structure is clear for a notebook-first project.

## Definition of Done

- [ ] Repository structure is ready for notebook creation.
- [ ] Data folders exist locally but generated data will not be committed.
- [ ] Phase 0 can continue with notebook and documentation creation.

## Recommended labels

```text
phase-0
repository-structure
notebook-only
priority-high
```

---

# Issue 0.3 — Create notebook skeletons 00 to 08

## Title

`Phase 0.3 — Create notebook skeletons for the complete notebook-only pipeline`

## Objective

Create all planned notebooks with consistent headings and placeholders.

## Context

Every relevant project step must be documented in a Jupyter notebook. The notebook order must map directly to the course requirements and the technical pipeline stages.

## Requirements

- [ ] Create the following notebooks:

```text
notebooks/00_project_scope_and_requirements.ipynb
notebooks/01_source_spike_and_cluster_check.ipynb
notebooks/02_city_reference_model.ipynb
notebooks/03_eea_batch_ingestion.ipynb
notebooks/04_wikipedia_web_scraping.ipynb
notebooks/05_open_meteo_api_and_kafka_producer.ipynb
notebooks/06_spark_structured_streaming_kafka_to_parquet.ipynb
notebooks/07_gold_layer_and_data_quality.ipynb
notebooks/08_analysis_visualization_and_storytelling.ipynb
```

- [ ] Each notebook must include these markdown sections:
  - Purpose
  - Inputs
  - Outputs
  - Technologies used
  - Configuration
  - Implementation
  - Validation / Quality Checks
  - Results
  - Limitations
  - Next step

- [ ] Add a short placeholder text to each section.
- [ ] Do not implement the full pipeline yet.
- [ ] Do not call APIs.
- [ ] Do not start Kafka or Spark.
- [ ] Keep notebooks lightweight.

## Acceptance Criteria

- [ ] All nine notebooks exist.
- [ ] All notebooks are valid `.ipynb` files.
- [ ] All notebooks use the same section structure.
- [ ] Notebook names match the implementation plan.
- [ ] Notebooks contain placeholders only, unless useful existing logic was safely migrated.

## Definition of Done

- [ ] Notebook sequence is ready for Phase 1.
- [ ] Each notebook has a clear purpose and expected outputs.
- [ ] A reviewer can understand the project flow from notebook names alone.

## Recommended labels

```text
phase-0
notebooks
documentation
priority-high
```

---

# Issue 0.4 — Rewrite README for notebook-only project

## Title

`Phase 0.4 — Rewrite README for notebook-only BDENG project`

## Objective

Rewrite the README so it accurately describes the notebook-only structure, the project topic, the BDENG requirements and the execution strategy.

## Requirements

README must include:

- [ ] Project title.
- [ ] Executive summary.
- [ ] Guiding question.
- [ ] Core scope.
- [ ] Non-goals.
- [ ] Data sources overview:
  - EEA file/batch source
  - Wikipedia web scraping source
  - Open-Meteo REST API source
- [ ] Technology stack.
- [ ] Notebook execution order.
- [ ] Requirement mapping table.
- [ ] Execution modes:
  - `local_project`
  - `fh_cluster_connectivity`
  - `fh_cluster_shared_storage`
- [ ] FH cluster findings:
  - Spark connectivity works
  - HDFS/shared storage not confirmed
  - Spark `local[*]` used for Parquet-producing pipeline runs
- [ ] Setup instructions.
- [ ] Data policy:
  - no large generated data in Git
  - `.gitkeep` preserves folder structure
- [ ] Limitations.
- [ ] Presentation notes.

## Acceptance Criteria

- [ ] README is consistent with notebook-only implementation.
- [ ] README does not describe `src/` or `tests/` as primary artifacts.
- [ ] README maps all MUST-HAVE course requirements to notebooks.
- [ ] README does not claim completed functionality that does not exist.
- [ ] README does not falsely claim cluster Parquet output works.
- [ ] README is written in clear professional English.

## Definition of Done

- [ ] README is ready for public GitHub viewing.
- [ ] README aligns with the target repository structure.
- [ ] README supports Phase 1 implementation.

## Recommended labels

```text
phase-0
readme
documentation
priority-high
```

---

# Issue 0.5 — Create configuration templates and Git ignore policy

## Title

`Phase 0.5 — Create environment templates and Git ignore policy`

## Objective

Create safe configuration templates and ensure secrets, generated data and checkpoints are not committed.

## Requirements

- [ ] Create `.env.example`.
- [ ] Create `.env.cluster.example`.
- [ ] Update `.gitignore`.
- [ ] Ensure real `.env` files are ignored.
- [ ] Ensure generated data is ignored.
- [ ] Ensure `.gitkeep` files are not ignored.

## Required `.env.example`

```env
EXECUTION_ENV=local_project

SPARK_MASTER_URL=local[*]
CLUSTER_SPARK_MASTER_URL=spark://<fh-spark-master-host>:7077

KAFKA_BOOTSTRAP_SERVERS=<kafka-host>:9092
KAFKA_TOPIC_AIR_QUALITY_LIVE=bdeng_gXX_air_quality_live

DATA_DIR=data
CHECKPOINT_DIR=data/checkpoints

PROJECT_TIMEZONE=UTC
LOG_LEVEL=INFO
```

## Required `.env.cluster.example`

```env
EXECUTION_ENV=fh_cluster_shared_storage

SPARK_MASTER_URL=spark://<fh-spark-master-host>:7077
KAFKA_BOOTSTRAP_SERVERS=<fh-kafka-broker-host>:9092
KAFKA_TOPIC_AIR_QUALITY_LIVE=bdeng_gXX_air_quality_live

DATA_DIR=<confirmed_shared_storage_path>/euro-air-quality-pipeline/data
CHECKPOINT_DIR=<confirmed_shared_storage_path>/euro-air-quality-pipeline/checkpoints
```

## Required `.gitignore`

```gitignore
__pycache__/
*.py[cod]

.venv/
venv/
.env
.env.*
!.env.example
!.env.cluster.example

.ipynb_checkpoints/

.DS_Store
Thumbs.db
.vscode/
.idea/

*.log
tmp/
temp/

data/**/*.parquet
data/**/*.csv
data/**/*.json
data/**/*.html
data/checkpoints/

!data/**/.gitkeep
```

## Acceptance Criteria

- [ ] `.env.example` exists and contains placeholders only.
- [ ] `.env.cluster.example` exists and contains placeholders only.
- [ ] `.gitignore` protects secrets and generated data.
- [ ] `.gitkeep` files remain trackable.
- [ ] No real credentials are committed.
- [ ] No personal absolute paths are used.

## Definition of Done

- [ ] Configuration policy is safe.
- [ ] Repo can be shared publicly without secrets.
- [ ] Generated runtime data will not pollute Git history.

## Recommended labels

```text
phase-0
configuration
security
gitignore
priority-high
```

---

# Issue 0.6 — Create ADRs and architecture documentation

## Title

`Phase 0.6 — Create architecture documentation and ADRs`

## Objective

Document the main architectural decisions and prepare the architecture documentation.

## Requirements

Create or update:

```text
docs/architecture.md
docs/data_sources.md
docs/cluster_setup.md
docs/limitations.md
docs/decisions/ADR-001-scope-freeze.md
docs/decisions/ADR-002-notebook-only-implementation.md
docs/decisions/ADR-003-parquet-bronze-silver-gold.md
docs/decisions/ADR-004-execution-environment-and-storage-strategy.md
docs/diagrams/architecture.mmd
docs/diagrams/dataflow.mmd
```

## ADR requirements

Each ADR should include:

```text
Status
Context
Decision
Consequences
```

## Required decisions

- [ ] Scope is fixed to EEA, Wikipedia, Open-Meteo, Kafka, Spark, Parquet.
- [ ] Implementation is notebook-only.
- [ ] Parquet Bronze/Silver/Gold is used as storage pattern.
- [ ] Spark `local[*]` is standard for Parquet-producing runs.
- [ ] FH Spark cluster is documented as connectivity/compute evidence.
- [ ] Cluster Parquet output is optional only if shared storage is confirmed.

## Acceptance Criteria

- [ ] All required docs exist.
- [ ] ADRs are specific and consistent.
- [ ] Diagrams are present as Mermaid files.
- [ ] Documentation does not overclaim.
- [ ] Documentation matches README and notebooks.

## Definition of Done

- [ ] Architecture decisions are auditable.
- [ ] A reviewer understands why notebook-only and Spark `local[*]` were chosen.
- [ ] Phase 0 documentation is complete.

## Recommended labels

```text
phase-0
architecture
adr
documentation
priority-high
```

---

# Issue 0.7 — Phase 0 QA and readiness check

## Title

`Phase 0.7 — Run Phase 0 QA and confirm readiness for Phase 1`

## Objective

Verify that the notebook-only refactor is complete and that Phase 1 can begin.

## Requirements

- [ ] Check repository structure.
- [ ] Check all notebooks exist and are valid.
- [ ] Check README consistency.
- [ ] Check `.gitignore`.
- [ ] Check environment templates.
- [ ] Check ADRs.
- [ ] Check docs and diagrams.
- [ ] Check no generated data or secrets are staged.
- [ ] Create QA report:

```text
docs/qa/phase0_qa_report.md
```

## Acceptance Criteria

- [ ] All Phase 0 deliverables exist.
- [ ] No critical issues remain.
- [ ] Notebook-only structure is clear.
- [ ] No false implementation claims exist.
- [ ] Phase 1 can begin.

## Definition of Done

- [ ] `docs/qa/phase0_qa_report.md` exists.
- [ ] Status is at least `PASS WITH MINOR ISSUES`.
- [ ] Phase 1 is approved.

## Recommended labels

```text
phase-0
qa
readiness
priority-high
```

---

# Phase 1 — Source Spike & Cluster Check

## Phase 1 Ziel

Quellen und Infrastruktur werden geprüft, bevor die eigentliche Pipeline implementiert wird.

## Phase 1 Main Notebook

```text
notebooks/01_source_spike_and_cluster_check.ipynb
```

---

# Issue 1.1 — Build Phase 1 notebook structure

## Title

`Phase 1.1 — Build source spike and cluster check notebook structure`

## Objective

Prepare the Phase 1 notebook with all required sections and define the checks for data sources and infrastructure.

## Requirements

- [ ] Update `notebooks/01_source_spike_and_cluster_check.ipynb`.
- [ ] Add sections:
  - Purpose
  - Inputs
  - Outputs
  - Technologies used
  - Configuration
  - Source checks
  - Cluster checks
  - Validation / Quality Checks
  - Results
  - Limitations
  - Next step
- [ ] Explain that this notebook is a spike, not the final pipeline.
- [ ] Define outputs:
  - source feasibility table,
  - cluster check summary,
  - storage decision.

## Acceptance Criteria

- [ ] Notebook structure exists.
- [ ] Notebook clearly separates data source checks from infrastructure checks.
- [ ] Notebook does not implement full ingestion.
- [ ] Expected outputs are documented.

## Definition of Done

- [ ] Phase 1 notebook is ready for actual source checks.

## Recommended labels

```text
phase-1
notebook
source-spike
priority-high
```

---

# Issue 1.2 — Validate Open-Meteo REST API access

## Title

`Phase 1.2 — Validate Open-Meteo Air Quality API access`

## Objective

Verify that Open-Meteo can provide relevant air quality data for selected pilot cities.

## Requirements

- [ ] Select 1–2 pilot cities from the planned city list.
- [ ] Build Open-Meteo API request.
- [ ] Request relevant air quality variables:
  - PM2.5
  - PM10
  - NO2 if available
- [ ] Inspect JSON structure.
- [ ] Save a tiny sample response locally under:

```text
data/bronze/open_meteo_raw/
```

- [ ] Document available fields and limitations.
- [ ] Do not build the final Kafka event schema yet.

## Acceptance Criteria

- [ ] API request succeeds or failure is clearly documented.
- [ ] Response format is inspected.
- [ ] Relevant pollutant fields are identified.
- [ ] Sample response is stored locally.
- [ ] Notebook documents whether Open-Meteo is usable.

## Definition of Done

- [ ] Open-Meteo feasibility status is known.
- [ ] Phase 5 can later build on this finding.

## Recommended labels

```text
phase-1
rest-api
open-meteo
source-spike
priority-high
```

---

# Issue 1.3 — Validate Wikipedia HTML access

## Title

`Phase 1.3 — Validate Wikipedia HTML access for pilot cities`

## Objective

Verify that Wikipedia city pages can be accessed and that HTML content can be stored for later parsing.

## Requirements

- [ ] Select 1–2 pilot cities.
- [ ] Define Wikipedia URLs.
- [ ] Fetch HTML using `requests`.
- [ ] Store tiny sample HTML files under:

```text
data/bronze/wikipedia_html/
```

- [ ] Inspect whether the page contains useful city metadata.
- [ ] Document potential parsing risks.

## Acceptance Criteria

- [ ] HTML request succeeds or failure is documented.
- [ ] Raw HTML sample is stored locally.
- [ ] The notebook documents whether metadata appears extractable.
- [ ] Wikipedia is confirmed as feasible web scraping source or risk is documented.

## Definition of Done

- [ ] Wikipedia feasibility status is known.
- [ ] Phase 4 can later build on this finding.

## Recommended labels

```text
phase-1
web-scraping
wikipedia
source-spike
priority-high
```

---

# Issue 1.4 — Validate EEA file/batch data source

## Title

`Phase 1.4 — Validate EEA historical air quality data source`

## Objective

Verify that EEA historical air quality data can serve as the required file/batch data source.

## Requirements

- [ ] Research the EEA historical air quality data source.
- [ ] Identify available formats:
  - CSV
  - JSON
  - Parquet
  - ZIP download
  - API-backed file download
- [ ] Identify relevant fields:
  - timestamp/date
  - pollutant
  - value
  - unit
  - station/location
  - country/city mapping information
- [ ] Check whether PM2.5, PM10, NO2 are available.
- [ ] Document access approach in:

```text
docs/data_sources.md
```

- [ ] Optionally store a tiny local sample if legally and technically acceptable.
- [ ] Do not process full EEA data yet.

## Acceptance Criteria

- [ ] EEA source is documented.
- [ ] File/batch nature is clear.
- [ ] Relevant pollutant availability is checked.
- [ ] Mapping risks are documented.
- [ ] Phase 3 can build on this source.

## Definition of Done

- [ ] EEA feasibility status is documented.
- [ ] The project has a viable file/batch source.

## Recommended labels

```text
phase-1
eea
batch-source
source-spike
priority-high
```

---

# Issue 1.5 — Document FH Spark cluster connectivity and storage findings

## Title

`Phase 1.5 — Document FH Spark cluster connectivity and storage findings`

## Objective

Document the already tested FH Spark cluster findings and confirm the execution strategy.

## Requirements

- [ ] Add a cluster check section to `notebooks/01_source_spike_and_cluster_check.ipynb`.
- [ ] Document:
  - Spark Master reachable,
  - Spark version,
  - Spark DataFrame action works,
  - Spark UI visible,
  - HDFS not available,
  - `fs.defaultFS = file:///`,
  - local Jupyter path not shared reliably with executors,
  - Spark `local[*]` chosen for Parquet-producing notebooks.
- [ ] Create or update:

```text
docs/qa/cluster_connectivity_check.md
docs/cluster_setup.md
```

- [ ] Do not claim cluster Parquet output works unless shared storage is confirmed.

## Acceptance Criteria

- [ ] Cluster connectivity findings are documented.
- [ ] Storage limitations are documented.
- [ ] Execution strategy is explicit.
- [ ] README and ADR-004 are consistent with this finding.

## Definition of Done

- [ ] FH environment is documented honestly.
- [ ] Project can proceed with Spark `local[*]` for Parquet pipeline.

## Recommended labels

```text
phase-1
cluster
spark
qa
priority-high
```

---

# Issue 1.6 — Create source feasibility summary and Phase 1 decision

## Title

`Phase 1.6 — Create source feasibility summary and Phase 1 decision`

## Objective

Summarize all source and infrastructure findings and decide whether Phase 2 can begin.

## Requirements

- [ ] Create a summary table in Notebook 01:

```text
Source
Type
Status
Format
Relevant fields
Risks
Decision
```

- [ ] Include:
  - EEA
  - Wikipedia
  - Open-Meteo
  - FH Spark
  - FH Kafka if already checked
- [ ] Update `docs/data_sources.md`.
- [ ] Add limitations to `docs/limitations.md`.
- [ ] State whether Phase 2 can begin.

## Acceptance Criteria

- [ ] All three required data sources are evaluated.
- [ ] Infrastructure findings are summarized.
- [ ] Risks are explicit.
- [ ] No unresolved critical blocker remains for Phase 2.
- [ ] Phase 2 start decision is documented.

## Definition of Done

- [ ] Phase 1 is complete.
- [ ] City Reference Model work can begin.

## Recommended labels

```text
phase-1
qa
source-spike
decision
priority-high
```

---

# Phase 2 — City Reference Model

## Phase 2 Ziel

Ein stabiler Stadt-Referenzdatensatz wird erstellt. Dieser Datensatz ist der zentrale Join-Anker für alle späteren Datenquellen.

## Phase 2 Main Notebook

```text
notebooks/02_city_reference_model.ipynb
```

---

# Issue 2.1 — Build city reference notebook structure

## Title

`Phase 2.1 — Build city reference model notebook structure`

## Objective

Prepare the Phase 2 notebook for creating the central city reference dataset.

## Requirements

- [ ] Update `notebooks/02_city_reference_model.ipynb`.
- [ ] Add standard sections:
  - Purpose
  - Inputs
  - Outputs
  - Technologies used
  - Configuration
  - Implementation
  - Validation / Quality Checks
  - Results
  - Limitations
  - Next step
- [ ] Explain why `city_id` is the central join key.
- [ ] Define output files:
  - `data/silver/city_reference.csv`
  - `data/silver/city_reference.parquet`

## Acceptance Criteria

- [ ] Notebook structure exists.
- [ ] Notebook explains the purpose of the city reference model.
- [ ] Expected output schema is documented.
- [ ] No final city data needs to be complete yet.

## Definition of Done

- [ ] Notebook is ready for city selection and data creation.

## Recommended labels

```text
phase-2
city-reference
notebook
priority-high
```

---

# Issue 2.2 — Select final city list and define city IDs

## Title

`Phase 2.2 — Select target cities and define stable city_id values`

## Objective

Define the initial list of selected European cities and assign stable technical identifiers.

## Requirements

- [ ] Select 8 European cities.
- [ ] Use clear selection criteria:
  - relevance,
  - data availability,
  - geographic spread,
  - recognizability,
  - feasibility.
- [ ] Define stable `city_id` values.
- [ ] Recommended format:

```text
vienna_at
berlin_de
paris_fr
madrid_es
rome_it
amsterdam_nl
warsaw_pl
prague_cz
```

- [ ] Avoid spaces, special characters and unstable naming.
- [ ] Document why 8 cities are used.

## Acceptance Criteria

- [ ] At least 8 cities are selected.
- [ ] Each city has a unique `city_id`.
- [ ] City list is documented.
- [ ] City IDs are stable and machine-friendly.

## Definition of Done

- [ ] Final city list for initial implementation is fixed.
- [ ] Later phases can use the city IDs.

## Recommended labels

```text
phase-2
city-reference
data-model
priority-high
```

---

# Issue 2.3 — Add coordinates and country metadata

## Title

`Phase 2.3 — Add coordinates and country metadata to city reference`

## Objective

Add the fields required for API calls, mapping and downstream joins.

## Requirements

- [ ] Add columns:
  - `city_id`
  - `city_name`
  - `city_name_normalized`
  - `country_code`
  - `latitude`
  - `longitude`
- [ ] Ensure coordinates are decimal degrees.
- [ ] Ensure `country_code` uses a consistent format, preferably ISO-style two-letter country codes.
- [ ] Add optional `wikipedia_url` if available.
- [ ] Document coordinate source or assumption.

## Acceptance Criteria

- [ ] Each city has latitude and longitude.
- [ ] Each city has country code.
- [ ] No missing values in required fields.
- [ ] Coordinates are plausible.
- [ ] Optional Wikipedia URL is present or derivable.

## Definition of Done

- [ ] City reference contains all minimum fields for Open-Meteo and Wikipedia.

## Recommended labels

```text
phase-2
city-reference
metadata
priority-high
```

---

# Issue 2.4 — Validate city reference model

## Title

`Phase 2.4 — Validate city reference model`

## Objective

Add validation cells to ensure the city reference model is usable as the central join model.

## Requirements

Validate:

- [ ] `city_id` is unique.
- [ ] `city_id` is not null.
- [ ] `city_name` is not null.
- [ ] `country_code` is not null.
- [ ] `latitude` and `longitude` are not null.
- [ ] latitude is between -90 and 90.
- [ ] longitude is between -180 and 180.
- [ ] there are at least 8 cities.
- [ ] no duplicate city names with conflicting country codes.

## Suggested validation code

```python
assert city_reference_df["city_id"].is_unique
assert city_reference_df["city_id"].notna().all()
assert city_reference_df["latitude"].between(-90, 90).all()
assert city_reference_df["longitude"].between(-180, 180).all()
assert len(city_reference_df) >= 8
```

## Acceptance Criteria

- [ ] Validation cells exist.
- [ ] Validation checks pass.
- [ ] Validation output is visible in the notebook.
- [ ] Any limitations are documented.

## Definition of Done

- [ ] City reference is validated and ready for persistence.

## Recommended labels

```text
phase-2
validation
data-quality
priority-high
```

---

# Issue 2.5 — Write city_reference.csv and city_reference.parquet

## Title

`Phase 2.5 — Write city reference dataset to CSV and Parquet`

## Objective

Persist the city reference model in CSV and Parquet format.

## Requirements

- [ ] Write:

```text
data/silver/city_reference.csv
data/silver/city_reference.parquet
```

- [ ] Read both files back.
- [ ] Compare row counts.
- [ ] Display schema and sample rows.
- [ ] Explain that generated data files are ignored by Git unless intentionally committed as tiny samples.

## Acceptance Criteria

- [ ] CSV output exists locally.
- [ ] Parquet output exists locally.
- [ ] Parquet output can be read back.
- [ ] Row count matches original DataFrame.
- [ ] Output path is relative, not hardcoded absolute path.

## Definition of Done

- [ ] City reference model is persisted and ready for Phase 3 and Phase 4.

## Recommended labels

```text
phase-2
parquet
silver-layer
priority-high
```

---

# Issue 2.6 — Phase 2 QA and handoff

## Title

`Phase 2.6 — Run Phase 2 QA and prepare handoff to ingestion phases`

## Objective

Verify that the city reference model is complete and ready for Phase 3, Phase 4 and Phase 5.

## Requirements

- [ ] Restart kernel and rerun `notebooks/02_city_reference_model.ipynb`.
- [ ] Verify output files exist.
- [ ] Verify `city_reference.parquet` is readable.
- [ ] Verify validation cells pass.
- [ ] Update `docs/data_sources.md` if city source assumptions are relevant.
- [ ] Add Phase 2 readiness note to:

```text
docs/qa/final_readiness_check.md
```

or create:

```text
docs/qa/phase2_city_reference_check.md
```

## Acceptance Criteria

- [ ] Notebook runs from top to bottom.
- [ ] City reference output exists.
- [ ] City reference is valid.
- [ ] Phase 3 and Phase 4 can use it.
- [ ] No scope creep introduced.

## Definition of Done

- [ ] Phase 2 is complete.
- [ ] Ingestion phases can begin.

## Recommended labels

```text
phase-2
qa
handoff
priority-high
```

---

# Phase 3 — EEA Batch Ingestion

## Phase 3 Ziel

Historische Luftqualitätsdaten werden als Datei-/Batch-Quelle verarbeitet und als Silver-Parquet-Dataset gespeichert.

## Phase 3 Main Notebook

```text
notebooks/03_eea_batch_ingestion.ipynb
```

---

# Issue 3.1 — Build EEA batch ingestion notebook structure

## Title

`Phase 3.1 — Build EEA batch ingestion notebook structure`

## Objective

Prepare the Phase 3 notebook and define the ingestion flow for the EEA file/batch source.

## Requirements

- [ ] Update `notebooks/03_eea_batch_ingestion.ipynb`.
- [ ] Add standard sections:
  - Purpose
  - Inputs
  - Outputs
  - Technologies used
  - Configuration
  - Implementation
  - Validation / Quality Checks
  - Results
  - Limitations
  - Next step
- [ ] Explain that EEA is the file/batch source.
- [ ] Define expected output:

```text
data/silver/eea_city_daily.parquet
```

- [ ] Explain relationship to Phase 2 city reference model.

## Acceptance Criteria

- [ ] Notebook structure exists.
- [ ] EEA source role is clear.
- [ ] Input/output contract is documented.
- [ ] No full ingestion implementation is required yet.

## Definition of Done

- [ ] Notebook is ready for EEA data loading.

## Recommended labels

```text
phase-3
eea
notebook
batch-ingestion
priority-high
```

---

# Issue 3.2 — Load or stage EEA source data

## Title

`Phase 3.2 — Load or stage EEA historical air quality data`

## Objective

Load or stage the EEA historical air quality source data for the selected cities and pollutants.

## Requirements

- [ ] Document the EEA data access method.
- [ ] Load a manageable EEA dataset or sample.
- [ ] Store raw/staged file locally under:

```text
data/bronze/eea/
```

if applicable.

- [ ] Inspect file format and columns.
- [ ] Identify fields for:
  - timestamp/date,
  - pollutant,
  - value,
  - unit,
  - station/location,
  - country/city mapping.
- [ ] Do not commit large EEA files to GitHub.

## Acceptance Criteria

- [ ] EEA source data is available locally or access is documented.
- [ ] Notebook can load the EEA data or documented sample.
- [ ] Relevant columns are identified.
- [ ] Source limitations are documented.

## Definition of Done

- [ ] EEA raw/staged data is ready for filtering and normalization.

## Recommended labels

```text
phase-3
eea
bronze-layer
data-source
priority-high
```

---

# Issue 3.3 — Filter pollutants and normalize fields

## Title

`Phase 3.3 — Filter PM2.5, PM10 and NO2 and normalize EEA fields`

## Objective

Filter the EEA dataset to the core pollutants and normalize the relevant fields.

## Requirements

- [ ] Filter to:
  - PM2.5
  - PM10
  - NO2
- [ ] Normalize timestamp/date field.
- [ ] Normalize pollutant naming.
- [ ] Normalize measurement value column.
- [ ] Preserve unit information.
- [ ] Remove or flag invalid values.
- [ ] Document handling of missing values.

## Suggested normalized columns

```text
timestamp
date
pollutant
value
unit
station_id
country_code
source
```

## Acceptance Criteria

- [ ] Only core pollutants remain.
- [ ] Timestamps/dates are usable.
- [ ] Numeric values are parsed correctly.
- [ ] Invalid values are handled.
- [ ] Normalization logic is visible in notebook.

## Definition of Done

- [ ] EEA data is normalized and ready for city mapping.

## Recommended labels

```text
phase-3
eea
data-cleaning
data-quality
priority-high
```

---

# Issue 3.4 — Map EEA data to city_id

## Title

`Phase 3.4 — Map EEA records to city_id`

## Objective

Map EEA records to the central `city_id` model from Phase 2.

## Requirements

- [ ] Load `data/silver/city_reference.parquet`.
- [ ] Define mapping strategy:
  - direct city field if available,
  - station-to-city mapping,
  - country/city filtering,
  - documented manual mapping if necessary.
- [ ] Add `city_id` to EEA records.
- [ ] Document ambiguous mappings.
- [ ] Exclude or flag records that cannot be mapped.
- [ ] Show mapping coverage.

## Acceptance Criteria

- [ ] EEA records include `city_id`.
- [ ] Mapping strategy is documented.
- [ ] Unmapped records are counted.
- [ ] At least selected project cities can be represented or limitations are documented.
- [ ] No hidden manual assumptions remain undocumented.

## Definition of Done

- [ ] EEA records are joinable with the project city model.

## Recommended labels

```text
phase-3
eea
city-mapping
data-model
priority-high
```

---

# Issue 3.5 — Aggregate EEA data to city-day level

## Title

`Phase 3.5 — Aggregate EEA data to daily city-level air quality metrics`

## Objective

Aggregate normalized and mapped EEA data to daily city-level values.

## Requirements

- [ ] Group by:
  - `city_id`
  - `date`
  - `pollutant`
- [ ] Calculate:
  - mean value,
  - min value,
  - max value,
  - observation count.
- [ ] Add:
  - `source = eea`
  - `processing_time_utc`
- [ ] Display sample aggregated output.
- [ ] Explain aggregation choice.

## Target schema

| Column | Description |
|---|---|
| `city_id` | stable join key |
| `date` | daily date |
| `pollutant` | PM2.5, PM10, NO2 |
| `mean_value` | daily mean |
| `min_value` | daily minimum |
| `max_value` | daily maximum |
| `observation_count` | number of measurements |
| `unit` | measurement unit |
| `source` | `eea` |
| `processing_time_utc` | processing timestamp |

## Acceptance Criteria

- [ ] Daily aggregation is implemented.
- [ ] Output schema matches target.
- [ ] Observation count is included.
- [ ] Aggregation logic is explained.
- [ ] Sample rows are displayed.

## Definition of Done

- [ ] Aggregated EEA dataset is ready for Silver storage.

## Recommended labels

```text
phase-3
eea
aggregation
silver-layer
priority-high
```

---

# Issue 3.6 — Write EEA Silver Parquet and validate output

## Title

`Phase 3.6 — Write EEA Silver Parquet and validate output`

## Objective

Write the aggregated EEA dataset to Parquet and validate that it can be read back.

## Requirements

- [ ] Write output to:

```text
data/silver/eea_city_daily.parquet
```

- [ ] Read the Parquet file back.
- [ ] Validate:
  - file exists,
  - row count > 0,
  - required columns exist,
  - `city_id` has no nulls for mapped records,
  - pollutant values are limited to PM2.5, PM10, NO2,
  - measurement values are plausible.
- [ ] Show missing value counts.
- [ ] Show pollutant distribution.
- [ ] Document limitations.

## Acceptance Criteria

- [ ] `eea_city_daily.parquet` exists locally.
- [ ] Parquet output is readable.
- [ ] Required schema exists.
- [ ] Data quality summary is visible.
- [ ] Generated output is ignored by Git unless intentionally sampled.

## Definition of Done

- [ ] EEA Batch Ingestion output is ready for Gold Layer.

## Recommended labels

```text
phase-3
eea
parquet
data-quality
priority-high
```

---

# Issue 3.7 — Phase 3 documentation and QA handoff

## Title

`Phase 3.7 — Document Phase 3 and prepare EEA handoff`

## Objective

Document the EEA ingestion method, assumptions, limitations and readiness for downstream phases.

## Requirements

- [ ] Update `docs/data_sources.md` with EEA details.
- [ ] Update `docs/limitations.md` with EEA-specific limitations.
- [ ] Add EEA output description to README if appropriate.
- [ ] Add Phase 3 QA note to:

```text
docs/qa/final_readiness_check.md
```

or create:

```text
docs/qa/phase3_eea_batch_check.md
```

- [ ] Restart kernel and rerun `notebooks/03_eea_batch_ingestion.ipynb` if feasible.
- [ ] Confirm that Phase 7 can use `eea_city_daily.parquet`.

## Acceptance Criteria

- [ ] Documentation matches actual notebook behavior.
- [ ] EEA limitations are explicit.
- [ ] Output file path is documented.
- [ ] Notebook can be rerun or rerun limitations are documented.
- [ ] No unsupported analytical claims are made.

## Definition of Done

- [ ] Phase 3 is complete.
- [ ] EEA Silver dataset is available for Gold Layer work.
- [ ] Project has fulfilled the file/batch source requirement.

## Recommended labels

```text
phase-3
documentation
qa
handoff
priority-high
```

---

# Combined Milestone Recommendations

Create these GitHub milestones:

```text
Phase 0 — Notebook-only Repository Setup
Phase 1 — Source Spike & Cluster Check
Phase 2 — City Reference Model
Phase 3 — EEA Batch Ingestion
```

Recommended cross-phase labels:

```text
notebook-only
bdeng
data-engineering
phase-0
phase-1
phase-2
phase-3
qa
documentation
data-quality
priority-high
priority-medium
```

---

# Combined Dependency Map

```text
Phase 0
  └── repository structure, notebooks, README, config

Phase 1
  └── source feasibility and infrastructure findings

Phase 2
  └── city_reference.parquet

Phase 3
  └── eea_city_daily.parquet

Phase 4
  └── wikipedia city_metadata.parquet

Phase 5
  └── Open-Meteo events to Kafka

Phase 6
  └── Spark reads Kafka and writes Parquet

Phase 7
  └── Gold Layer

Phase 8
  └── Visualization and Storytelling
```
