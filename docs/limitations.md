# Limitations

- The project may not process truly massive data volumes; the Big Data Engineering focus is on source integration, Kafka, Spark, storage layout, and reproducibility.
- The analysis is exploratory and descriptive, not causal.
- Wikipedia data is unstable and should be treated as contextual metadata, not official ground truth.
- FH cluster storage is not assumed. Cluster Spark writes to the project `data/` folder must not be claimed unless shared storage is proven.
- Air quality station representativeness and city-level aggregation are simplifications that must be discussed in the final story.

## Phase-Specific Limitations Through Phase 4

- Phase 1 source spikes are guarded by execution flags. If they are not run in the current environment, the notebook records the intended check and must be executed before final submission.
- Phase 2 city coordinates are city-center approximations and are used for API requests and joins, not as station coordinates.
- Phase 3 can use a controlled sample when no local EEA extract is available. That sample proves transformation mechanics but is not analytical evidence.
- Phase 3 EEA station mapping is simplified and must be reviewed against real station metadata before drawing conclusions.
- Phase 4 Wikipedia parsing is heuristic. Missing or ambiguous population, area, or density fields remain nullable and are documented with `parse_status` and `parse_notes`.
