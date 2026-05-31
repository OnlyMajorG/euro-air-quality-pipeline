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
- Phase 5 REST API values are current or near-current context. They are not historical EEA measurements and must remain labeled separately.
- Phase 5 controlled Open-Meteo fallback rows are mechanics-only test data. Final API claims require a successful run with `status=fetched_api`.
- Phase 5 Kafka publishing requires a reachable external broker and a real group-specific topic. A local JSONL event batch proves event generation, but it does not prove Kafka delivery.
- Phase 5 local mock-broker delivery proves producer/consumer mechanics only. The FH Kafka claim requires `KAFKA_MODE=kafka`, disabled mock fallback and a successful bounded consumer smoke test.
- Phase 6 local Spark file-stream fallback proves Spark Structured Streaming transformations, schema parsing, validation, joins, checkpointing and Parquet read-back only. The MUST-HAVE Kafka-to-Spark claim requires `SPARK_KAFKA_MODE=kafka`, disabled Spark mock fallback and `selected_source_mode=kafka` in the FH run.
- Spark Kafka connector packages must match the Spark and Scala versions installed on JupyterHub. Configure `SPARK_KAFKA_CONNECTOR_PACKAGE` only when the environment does not already provide the connector.
- Native Windows Spark file reads and Parquet writes require compatible Hadoop Windows binaries (`winutils.exe` and `hadoop.dll`) through `HADOOP_HOME`, or a Linux-based runtime. Use Java 17 or 21; Java 25 is not suitable for the current Hadoop filesystem dependency.
- Kafka delivery is at least once. Phase 6 must deduplicate by deterministic `event_id`.
- Phase 7 writes Gold Parquet driver-locally until FH shared storage is proven by `RUN_PHASE7_SPARK_STORAGE_PROBE=true`.
- If Phase-6 Silver streaming output is unavailable, Phase 7 may reconstruct a live snapshot from Phase-5 JSONL events. The output records `live_input_mode=phase5_jsonl_mock_reconstruction`; this is not Kafka-to-Spark evidence.
- Historical Gold tables preserve `data_status`. Controlled EEA sample data blocks final analytical claims and may demonstrate pipeline mechanics only.
- MongoDB and a Vienna-only weather collection are intentionally not introduced: they are not available artifacts and would conflict with the frozen EEA/Wikipedia/Open-Meteo/Kafka/Spark scope.
