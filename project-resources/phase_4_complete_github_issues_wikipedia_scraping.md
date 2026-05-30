# GitHub Issues — Gesamte Phase 4: Wikipedia Web Scraping

**Projekt:** `euro-air-quality-pipeline`  
**Strukturentscheidung:** Notebook-only  
**Phase:** Phase 4 — Wikipedia Web Scraping  
**Hauptnotebook:** `notebooks/04_wikipedia_web_scraping.ipynb`  
**Primäre Outputs:**

```text
data/bronze/wikipedia_html/*.html
data/silver/city_metadata.parquet
docs/data_sources.md
docs/limitations.md
```

---

## Phase 4 Ziel

Phase 4 erfüllt die BDENG-MUST-HAVE-Anforderung:

> 1 data source obtained by web scraping.

Wikipedia-Stadtseiten werden als Web-Scraping-Quelle verwendet, um urbane Kontextdaten für die ausgewählten europäischen Städte zu gewinnen. Diese Daten dienen später als Kontext für die Interpretation von Luftqualitätsmustern.

Die Phase ist abgeschlossen, wenn:

1. das Notebook `04_wikipedia_web_scraping.ipynb` vollständig strukturiert ist,
2. Wikipedia-HTML für alle Zielstädte abgerufen und im Bronze Layer gespeichert wurde,
3. relevante Metadaten extrahiert wurden,
4. die Metadaten normalisiert und validiert wurden,
5. `city_metadata.parquet` im Silver Layer erzeugt wurde,
6. Limitations und Datenqualitätsprobleme dokumentiert wurden,
7. der Output von späteren Notebooks verwendet werden kann.

---

## Phase 4 Dependencies

Phase 4 hängt ab von:

```text
Phase 2 — City Reference Model
```

Benötigter Input:

```text
data/silver/city_reference.parquet
```

Dieses File muss mindestens enthalten:

```text
city_id
city_name
country_code
latitude
longitude
```

Optional hilfreich:

```text
wikipedia_url
population
area_km2
population_density
```

---

## Phase 4 Scope

### Included

- Wikipedia als Web-Scraping-Quelle
- Abruf von HTML-Seiten
- Speicherung von Roh-HTML im Bronze Layer
- Parsing von Stadtmetadaten
- Normalisierung numerischer Werte
- Erstellung eines Silver-Parquet-Datasets
- Validierungszellen im Notebook
- Dokumentation von Limitationen

### Excluded

- Kafka
- Spark Structured Streaming
- REST API Open-Meteo
- EEA Batch Ingestion
- Gold Layer
- Visualisierung
- Dashboard
- Machine Learning
- Kausalanalyse

---

# Issue 4.1 — Create Phase 4 notebook structure and input contract

## Title

`Phase 4.1 — Create Wikipedia scraping notebook structure and input contract`

## Objective

Create the notebook foundation for Phase 4 and define the exact input/output contract for the web scraping step.

This issue does not yet implement the full scraper. It prepares a clean, reproducible and well-documented notebook structure.

## Context

The project uses a notebook-only implementation style. Therefore, Phase 4 must be implemented and documented directly inside:

```text
notebooks/04_wikipedia_web_scraping.ipynb
```

The notebook must clearly show how the Wikipedia web scraping source fits into the BDENG MUST-HAVE criteria.

## Requirements

- [ ] Create or update `notebooks/04_wikipedia_web_scraping.ipynb`.
- [ ] Add the required notebook sections:
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
- [ ] Explain that Wikipedia is the web scraping source.
- [ ] Load `data/silver/city_reference.parquet`.
- [ ] Validate that the city reference file contains the required columns:
  - `city_id`
  - `city_name`
  - `country_code`
  - `latitude`
  - `longitude`
- [ ] Define expected Phase 4 outputs:
  - `data/bronze/wikipedia_html/*.html`
  - `data/silver/city_metadata.parquet`
- [ ] Create needed directories if missing:
  - `data/bronze/wikipedia_html/`
  - `data/silver/`
- [ ] Add a markdown explanation of why the extracted metadata is contextual only and not causal evidence.

## Technical Scope

### Included

- Notebook setup
- Input contract
- Output contract
- Directory setup
- Basic input validation
- Documentation of web scraping role

### Excluded

- HTTP requests
- HTML parsing
- Parquet output creation
- Data analysis
- Kafka/Spark

## Suggested notebook code snippets

```python
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
CITY_REFERENCE_PATH = DATA_DIR / "silver" / "city_reference.parquet"
WIKIPEDIA_RAW_DIR = DATA_DIR / "bronze" / "wikipedia_html"
SILVER_DIR = DATA_DIR / "silver"

WIKIPEDIA_RAW_DIR.mkdir(parents=True, exist_ok=True)
SILVER_DIR.mkdir(parents=True, exist_ok=True)

city_reference_df = pd.read_parquet(CITY_REFERENCE_PATH)

required_columns = {"city_id", "city_name", "country_code", "latitude", "longitude"}
missing_columns = required_columns - set(city_reference_df.columns)

assert not missing_columns, f"Missing required columns: {missing_columns}"
assert city_reference_df["city_id"].is_unique
assert city_reference_df["city_id"].notna().all()
```

## Acceptance Criteria

- [ ] `notebooks/04_wikipedia_web_scraping.ipynb` exists.
- [ ] Notebook contains all required standard sections.
- [ ] Notebook reads `data/silver/city_reference.parquet`.
- [ ] Input columns are validated.
- [ ] Output directories are created.
- [ ] Notebook explains Wikipedia as the web scraping data source.
- [ ] No unrelated implementation is added.
- [ ] No hardcoded local machine paths are used.

## Definition of Done

- [ ] Notebook structure is complete.
- [ ] City reference input contract is validated.
- [ ] Phase 4 outputs are clearly defined.
- [ ] The notebook is ready for raw HTML retrieval in Issue 4.2.

## Recommended labels

```text
phase-4
notebook
web-scraping
setup
priority-high
```

---

# Issue 4.2 — Define Wikipedia URLs and fetch raw HTML into Bronze layer

## Title

`Phase 4.2 — Fetch Wikipedia raw HTML and store it in Bronze layer`

## Objective

Fetch Wikipedia HTML pages for all selected cities and store the raw HTML files in the Bronze layer.

## Context

The Bronze layer preserves raw source data before transformation. For the web scraping source, this means storing the raw HTML pages that were used for later parsing.

This ensures traceability and allows the parsing logic to be rerun without immediately repeating all HTTP requests.

## Requirements

- [ ] Continue in `notebooks/04_wikipedia_web_scraping.ipynb`.
- [ ] Define or derive one Wikipedia URL per selected city.
- [ ] Prefer explicit and reviewable URL mapping.
- [ ] Use `requests` to fetch HTML.
- [ ] Use a meaningful User-Agent.
- [ ] Use a timeout.
- [ ] Avoid aggressive request behavior.
- [ ] Store one raw HTML file per city under:

```text
data/bronze/wikipedia_html/
```

- [ ] Use `city_id` in the filename:

```text
data/bronze/wikipedia_html/vienna_at.html
```

- [ ] Record retrieval status per city:
  - `success`
  - `failed`
  - HTTP status code
  - file path
  - file size
- [ ] Failed requests must not silently disappear.
- [ ] Display a validation summary table.

## Technical Scope

### Included

- Wikipedia URL mapping
- HTTP requests
- raw HTML persistence
- retrieval status table
- basic error handling

### Excluded

- Metadata parsing
- numeric normalization
- Parquet Silver output
- visualizations

## Suggested code snippets

```python
import requests
import time
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "euro-air-quality-pipeline/1.0 educational project"
}

def fetch_html(url: str, timeout: int = 20) -> tuple[str | None, int | None, str | None]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        status_code = response.status_code
        response.raise_for_status()
        return response.text, status_code, None
    except Exception as exc:
        return None, None, str(exc)
```

```python
retrieval_results = []

for _, row in city_reference_df.iterrows():
    city_id = row["city_id"]
    city_name = row["city_name"]
    url = row.get("wikipedia_url") or f"https://en.wikipedia.org/wiki/{city_name.replace(' ', '_')}"

    html, status_code, error = fetch_html(url)

    output_path = WIKIPEDIA_RAW_DIR / f"{city_id}.html"

    if html:
        output_path.write_text(html, encoding="utf-8")
        file_size = output_path.stat().st_size
        status = "success"
    else:
        file_size = None
        status = "failed"

    retrieval_results.append({
        "city_id": city_id,
        "city_name": city_name,
        "url": url,
        "status": status,
        "http_status_code": status_code,
        "file_path": str(output_path) if html else None,
        "file_size_bytes": file_size,
        "error": error,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat()
    })

    time.sleep(1)
```

## Acceptance Criteria

- [ ] Wikipedia URLs are defined for all selected cities.
- [ ] Raw HTML is fetched for at least 8 cities or failures are documented.
- [ ] Raw HTML files are stored under `data/bronze/wikipedia_html/`.
- [ ] Filenames use `city_id`.
- [ ] Retrieval status table is displayed.
- [ ] Failed downloads are visible and explained.
- [ ] No credentials or secrets are used.
- [ ] Request behavior is not aggressive.
- [ ] Generated HTML files are covered by `.gitignore`.

## Definition of Done

- [ ] Bronze HTML archive exists locally.
- [ ] Retrieval results are documented in the notebook.
- [ ] Raw HTML is ready for parsing in Issue 4.3.

## Recommended labels

```text
phase-4
web-scraping
bronze-layer
notebook
priority-high
```

---

# Issue 4.3 — Parse Wikipedia metadata from raw HTML

## Title

`Phase 4.3 — Parse population, area and density from Wikipedia HTML`

## Objective

Parse the stored Wikipedia HTML files and extract structured city metadata.

## Context

The raw HTML files from Issue 4.2 must be transformed into structured data. The extracted metadata provides urban context for later air quality interpretation.

The parser does not need to be perfect, but it must be transparent, defensive and well documented.

## Requirements

- [ ] Read raw HTML files from:

```text
data/bronze/wikipedia_html/
```

- [ ] Parse metadata for each city.
- [ ] Extract where available:
  - population
  - area in square kilometers
  - population density
- [ ] Preserve:
  - `city_id`
  - `city_name`
  - `country_code`
  - `source_url`
  - `metadata_source`
  - `processed_at_utc`
- [ ] Add parser status fields:
  - `parse_status`
  - `parse_notes`
- [ ] Use BeautifulSoup and/or pandas table parsing.
- [ ] Do not crash if one city page has a different HTML structure.
- [ ] Mark uncertain or incomplete records as `partial`.
- [ ] Mark unusable records as `failed`.

## Technical Scope

### Included

- reading local raw HTML
- parser implementation in notebook
- infobox/table parsing
- defensive fallbacks
- parse status and notes

### Excluded

- HTTP fetching
- final Parquet write
- analysis
- visualization

## Suggested parser structure

```python
from bs4 import BeautifulSoup
import re

def clean_number(value: str):
    if value is None:
        return None

    value = re.sub(r"\[.*?\]", "", str(value))
    value = value.replace(",", "")
    value = value.replace("\xa0", " ")
    value = re.sub(r"[^0-9.]", "", value)

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None
```

```python
def parse_city_metadata(city_row: pd.Series, html: str) -> dict:
    city_id = city_row["city_id"]
    city_name = city_row["city_name"]
    country_code = city_row["country_code"]

    soup = BeautifulSoup(html, "lxml")

    # Implement extraction strategy here.
    # Prefer transparent, documented heuristics.
    # Do not assume identical page structure for all cities.

    return {
        "city_id": city_id,
        "city_name": city_name,
        "country_code": country_code,
        "population": None,
        "area_km2": None,
        "population_density": None,
        "metadata_source": "wikipedia",
        "parse_status": "partial",
        "parse_notes": "Parser fallback used; values need review."
    }
```

## Target intermediate schema

| Column | Required | Description |
|---|---:|---|
| `city_id` | yes | Stable join key |
| `city_name` | yes | City display name |
| `country_code` | yes | Country code |
| `population` | no | Parsed population |
| `area_km2` | no | Parsed area |
| `population_density` | no | Parsed/calculated density |
| `source_url` | yes | Wikipedia URL |
| `metadata_source` | yes | Always `wikipedia` |
| `processed_at_utc` | yes | Processing timestamp |
| `parse_status` | yes | `success`, `partial`, `failed` |
| `parse_notes` | no | Parser notes |

## Acceptance Criteria

- [ ] Raw HTML files are read from Bronze layer.
- [ ] Metadata parsing is implemented in the notebook.
- [ ] At least `city_id`, `city_name`, `country_code`, `metadata_source`, `parse_status` are populated.
- [ ] Population, area and density are extracted where possible.
- [ ] Parser handles missing values defensively.
- [ ] Parser status is documented per city.
- [ ] A preview table is displayed.
- [ ] No causal interpretation is made.

## Definition of Done

- [ ] Parsed metadata DataFrame exists in the notebook.
- [ ] Parse status distribution is shown.
- [ ] Parser limitations are documented.
- [ ] Output is ready for normalization and Silver write in Issue 4.4.

## Recommended labels

```text
phase-4
web-scraping
parser
notebook
priority-high
```

---

# Issue 4.4 — Normalize metadata and write Silver Parquet

## Title

`Phase 4.4 — Normalize Wikipedia metadata and write city_metadata.parquet`

## Objective

Normalize the parsed Wikipedia metadata, validate the output and write a Silver-layer Parquet file.

Main output:

```text
data/silver/city_metadata.parquet
```

## Context

The Silver layer contains cleaned and structured data. This dataset will later be joined with air quality data using `city_id`.

## Requirements

- [ ] Continue in `notebooks/04_wikipedia_web_scraping.ipynb`.
- [ ] Convert numeric fields to suitable types:
  - `population`
  - `area_km2`
  - `population_density`
- [ ] If density is missing and population + area are available, calculate:

```text
population_density = population / area_km2
```

- [ ] Ensure one row per `city_id`.
- [ ] Ensure `city_id` is not null.
- [ ] Ensure `metadata_source = wikipedia`.
- [ ] Validate joinability with `city_reference.parquet`.
- [ ] Write Parquet output:

```text
data/silver/city_metadata.parquet
```

- [ ] Read the Parquet file back and display sample rows.
- [ ] Optionally write a small CSV preview for inspection:

```text
data/silver/city_metadata_preview.csv
```

## Technical Scope

### Included

- normalization
- type conversion
- plausibility checks
- join validation
- Parquet write/read-back

### Excluded

- additional scraping
- Gold layer
- visualization
- Kafka/Spark

## Suggested validation checks

```python
assert city_metadata_df["city_id"].notna().all()
assert city_metadata_df["city_id"].is_unique
assert (city_metadata_df["metadata_source"] == "wikipedia").all()
```

```python
joined = city_reference_df.merge(
    city_metadata_df,
    on="city_id",
    how="left",
    indicator=True
)

joined["_merge"].value_counts()
```

```python
city_metadata_df.to_parquet(
    "data/silver/city_metadata.parquet",
    index=False
)

pd.read_parquet("data/silver/city_metadata.parquet").head()
```

## Acceptance Criteria

- [ ] Numeric fields are normalized where possible.
- [ ] Missing values are handled explicitly.
- [ ] `city_id` is unique.
- [ ] Output has one row per selected city.
- [ ] Join with `city_reference.parquet` works.
- [ ] `data/silver/city_metadata.parquet` is created.
- [ ] Parquet output can be read back.
- [ ] Output schema is displayed.
- [ ] Missing values and parse status are summarized.
- [ ] No unsupported causal claims are made.

## Definition of Done

- [ ] `city_metadata.parquet` exists locally.
- [ ] Notebook can be rerun after Issues 4.1–4.3.
- [ ] Silver metadata is ready for later pipeline phases.
- [ ] Validation results are visible in the notebook.

## Recommended labels

```text
phase-4
silver-layer
data-quality
notebook
priority-high
```

---

# Issue 4.5 — Document Wikipedia source limitations and update project documentation

## Title

`Phase 4.5 — Document Wikipedia source limitations and update project docs`

## Objective

Update the project documentation so that the Wikipedia source, scraping strategy, data quality limitations and usage boundaries are clearly documented.

## Context

Wikipedia data is useful for contextual metadata but has limitations:

- page structures can change,
- values may differ by language/version,
- metadata may be incomplete,
- population and area values may refer to different administrative definitions,
- density is contextual and not causal evidence for air quality.

These limitations must be explicit in the project.

## Requirements

- [ ] Update `docs/data_sources.md`.
- [ ] Update or create `docs/limitations.md`.
- [ ] Explain that Wikipedia is the web scraping source.
- [ ] Document extracted fields:
  - population,
  - area,
  - density,
  - source URL,
  - processing timestamp,
  - parse status.
- [ ] Explain Bronze/Silver separation:
  - Bronze = raw HTML,
  - Silver = structured metadata.
- [ ] Explain scraping limitations.
- [ ] Explain that city metadata is used only as context.
- [ ] Add a short Phase 4 summary to README if appropriate.
- [ ] Ensure documentation matches the actual notebook outputs.

## Technical Scope

### Included

- documentation updates
- limitation notes
- data source description
- method summary

### Excluded

- code changes unless documentation reveals a clear inconsistency
- new data sources
- new visualizations

## Suggested documentation content

```markdown
## Wikipedia City Metadata

Wikipedia city pages are used as the web scraping source.
The project stores raw HTML in the Bronze layer and extracts selected city metadata into the Silver layer.

Extracted fields:
- population
- area_km2
- population_density
- source_url
- parse_status
- parse_notes

Limitations:
- Wikipedia page structure may change.
- Population and area definitions may differ between cities.
- Some fields may be missing or partially parsed.
- Metadata is used as contextual information only and not as causal evidence.
```

## Acceptance Criteria

- [ ] `docs/data_sources.md` describes Wikipedia as the web scraping source.
- [ ] `docs/limitations.md` includes Wikipedia-specific limitations.
- [ ] Documentation mentions Bronze raw HTML and Silver metadata.
- [ ] Documentation does not overclaim data reliability.
- [ ] README is consistent with the notebook output.
- [ ] No causal claims are introduced.
- [ ] Documentation is concise but specific.

## Definition of Done

- [ ] Documentation reflects actual Phase 4 implementation.
- [ ] A reviewer can understand how the Wikipedia data was obtained and used.
- [ ] Limitations are explicit enough for presentation and final report.

## Recommended labels

```text
phase-4
documentation
limitations
data-source
priority-medium
```

---

# Issue 4.6 — Phase 4 QA and handoff to later phases

## Title

`Phase 4.6 — Run Phase 4 QA and prepare handoff to Gold and analysis phases`

## Objective

Perform a final QA check for Phase 4 and verify that the Wikipedia metadata output can be used in later notebooks.

## Context

Phase 4 is complete only if its output is usable by downstream pipeline stages:

```text
Phase 6 — Spark Structured Streaming Kafka to Parquet
Phase 7 — Gold Layer and Data Quality
Phase 8 — Analysis, Visualization and Storytelling
```

This issue verifies that Phase 4 has not just generated files, but has produced a reliable and documented Silver dataset.

## Requirements

- [ ] Restart kernel and rerun `notebooks/04_wikipedia_web_scraping.ipynb`.
- [ ] Verify that all sections execute in order.
- [ ] Verify that raw HTML files exist locally.
- [ ] Verify that `data/silver/city_metadata.parquet` exists.
- [ ] Verify that `city_metadata.parquet` can be read.
- [ ] Verify that it joins with `city_reference.parquet`.
- [ ] Verify that the notebook includes:
  - validation summary,
  - parse status summary,
  - limitations,
  - next step.
- [ ] Verify that generated files are ignored by `.gitignore`.
- [ ] Add a short QA note to:

```text
docs/qa/final_readiness_check.md
```

or create:

```text
docs/qa/phase4_web_scraping_check.md
```

## Technical Scope

### Included

- notebook rerun check
- output validation
- downstream readiness check
- QA documentation

### Excluded

- rewriting the scraper from scratch
- adding new sources
- adding visualizations
- starting Phase 5/6 work

## QA checklist

- [ ] Notebook runs from top to bottom.
- [ ] `city_reference.parquet` is loaded successfully.
- [ ] raw HTML files exist.
- [ ] metadata output exists.
- [ ] metadata output has one row per city.
- [ ] `city_id` is unique.
- [ ] `parse_status` exists.
- [ ] limitations are documented.
- [ ] generated data files are not accidentally staged for Git.
- [ ] no credentials or secrets are present.
- [ ] README and docs are consistent.

## Suggested final validation code

```python
from pathlib import Path
import pandas as pd

city_reference = pd.read_parquet("data/silver/city_reference.parquet")
city_metadata = pd.read_parquet("data/silver/city_metadata.parquet")

assert city_metadata["city_id"].notna().all()
assert city_metadata["city_id"].is_unique

joined = city_reference.merge(
    city_metadata,
    on="city_id",
    how="left",
    indicator=True
)

display(joined["_merge"].value_counts())
display(city_metadata.head())
```

## Acceptance Criteria

- [ ] Phase 4 notebook runs in order.
- [ ] Raw HTML is present locally.
- [ ] `city_metadata.parquet` is present and readable.
- [ ] Join with city reference works.
- [ ] Documentation is updated.
- [ ] Limitations are documented.
- [ ] Phase 4 is ready for downstream use.
- [ ] No scope creep was introduced.

## Definition of Done

- [ ] Phase 4 can be marked complete.
- [ ] Downstream notebooks can use `city_metadata.parquet`.
- [ ] QA result is documented.
- [ ] Git status does not contain unintended generated data files.

## Recommended labels

```text
phase-4
qa
handoff
data-quality
priority-high
```

---

# Phase 4 Final Definition of Done

Phase 4 is complete when all Phase 4 issues are done:

```text
4.1 Notebook structure and input contract
4.2 Raw HTML retrieval and Bronze archive
4.3 Metadata parsing
4.4 Silver Parquet output
4.5 Documentation and limitations
4.6 QA and handoff
```

## Final criteria

- [ ] `notebooks/04_wikipedia_web_scraping.ipynb` exists and is complete.
- [ ] Wikipedia is clearly documented as the web scraping source.
- [ ] Raw HTML is stored in `data/bronze/wikipedia_html/`.
- [ ] `data/silver/city_metadata.parquet` exists locally.
- [ ] Metadata can be joined with `city_reference.parquet`.
- [ ] Missing/partial parsing is documented via `parse_status` or `parse_notes`.
- [ ] Limitations are documented in notebook and docs.
- [ ] The output is ready for later phases.
- [ ] No unrelated scope was introduced.
- [ ] No large generated files are accidentally committed.

---

# Phase 4 Issue Dependency Map

```text
4.1 Notebook structure and input contract
        ↓
4.2 Fetch raw HTML into Bronze
        ↓
4.3 Parse metadata from raw HTML
        ↓
4.4 Normalize and write Silver Parquet
        ↓
4.5 Update documentation and limitations
        ↓
4.6 QA and downstream handoff
```

---

# GitHub Milestone Recommendation

Create a milestone:

```text
Phase 4 — Wikipedia Web Scraping
```

Add all issues 4.1 to 4.6 to this milestone.

Recommended labels:

```text
phase-4
web-scraping
notebook
bronze-layer
silver-layer
data-quality
documentation
qa
```
