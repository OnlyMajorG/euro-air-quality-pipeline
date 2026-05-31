# Final Readiness Check

## Checklist

- [ ] All notebooks execute in order from `00` to `08`.
- [ ] No secrets or credentials are committed.
- [ ] Generated data remains ignored by Git.
- [ ] Kafka topic is group-specific.
- [ ] Spark Structured Streaming reads from Kafka and writes Parquet.
- [ ] Gold tables and figures are generated.
- [ ] Limitations and non-causal interpretation are documented.
- [ ] Presentation storyline is complete.

## Current Phase Gate Notes

| Phase | Current status | Gate note |
| --- | --- | --- |
| 0 | complete | Notebook-only repository structure is in place. |
| 1 | complete | Source and cluster checks are implemented; local QA executed the guarded Open-Meteo and Wikipedia source spikes successfully. |
| 2 | complete | City reference notebook writes CSV and Parquet locally. |
| 3 | complete with data note | EEA batch notebook works with local EEA files or controlled sample fallback. Real EEA data is needed for final analysis. |
| 4 | complete | Wikipedia scraping notebook implements Bronze HTML, parser and Silver metadata output; local validation produced readable `city_metadata.parquet`. |
| 5 | implemented; local mock pass; FH evidence pending | Open-Meteo Bronze JSON, manifest, latest-hour JSONL events, Kafka producer, bounded consumer and mock broker are implemented. Strict FH Kafka delivery remains required. |
| 6-8 | pending | Spark streaming, Gold layer and storytelling remain to be completed. |

## Git Hygiene

- `project-resources/` is ignored by Git and removed from tracking with `git rm --cached`.
- Generated local files under `data/` remain ignored.
- The project repository deliverable is the notebook-only structure, docs, diagrams, configuration examples and presentation placeholders.
