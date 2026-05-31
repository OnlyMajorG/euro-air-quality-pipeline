# Phase 7 Gold Layer and Data Quality Check

## Scope

Notebook `07_gold_layer_and_data_quality.ipynb` validates the Phase-2 to Phase-6 handoff, creates analysis-ready Gold datasets and prepares the Phase-8 visualization boundary.

## Design Decisions

- Historical EEA aggregates and Open-Meteo live context remain separate.
- Gold Parquet files are written driver-locally for reproducibility.
- Kafka broker and Spark master connectivity are checked visibly.
- `RUN_PHASE7_SPARK_STORAGE_PROBE=true` enables an optional Spark-worker write/readback probe on FH JupyterHub.
- Missing Phase-6 Silver live Parquet may use a clearly labeled Phase-5 JSONL reconstruction fallback for local mechanics.
- Controlled EEA sample data remains visible through `data_status=controlled_sample_fallback` and blocks final analytical claims.

## Expected Gold Outputs

```text
data/gold/city_air_quality_daily_summary.parquet
data/gold/pollutant_ranking_by_city.parquet
data/gold/city_context_air_quality.parquet
data/gold/live_air_quality_latest.parquet
data/gold/data_quality_summary.parquet
```

## Local Run

Run notebooks `02`, `03`, `04`, `05`, then `07`. Notebook `06` remains required for the FH Spark-from-Kafka evidence run, but Phase 7 can use its explicit JSONL reconstruction fallback locally.

Expected local markers:

```text
eea_sample_fallback_used: True
live_input_mode: phase5_jsonl_mock_reconstruction
final_analytical_claims_allowed: False
```

## FH JupyterHub Run

Run notebooks `02` through `07` in order. For infrastructure evidence, configure:

```env
KAFKA_MODE=kafka
ALLOW_KAFKA_MOCK_FALLBACK=false
SPARK_KAFKA_MODE=kafka
ALLOW_SPARK_KAFKA_MOCK_FALLBACK=false
RUN_PHASE7_SPARK_STORAGE_PROBE=true
```

Expected final live marker:

```text
live_input_mode: phase6_spark_stream_silver
```

Final analytical claims additionally require a real EEA input file, not the controlled sample.

## Local Verification Result

The local Run-All verification completed successfully on May 31, 2026.

| Check | Result |
| --- | --- |
| Phase-3 Silver EEA provenance | `controlled_sample_fallback` |
| Historical daily Gold rows | `720` |
| Pollutant ranking Gold rows | `24` |
| City context Gold rows | `24` |
| Latest live snapshot rows | `8` |
| Quality summary rows | `4` |
| Duplicate Gold keys | `0` |
| Historical/live separation | Passed |
| Live input mode | `phase5_jsonl_mock_reconstruction` |
| Final analytical claims allowed | `False` until real EEA input is used |

The local fallback validates Phase-7 mechanics and Phase-8 readiness. It does not replace the FH JupyterHub Kafka-to-Spark evidence run from notebooks `05` and `06`.
