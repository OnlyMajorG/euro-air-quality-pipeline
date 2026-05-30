# Limitations

- The project may not process truly massive data volumes; the Big Data Engineering focus is on source integration, Kafka, Spark, storage layout, and reproducibility.
- The analysis is exploratory and descriptive, not causal.
- Wikipedia data is unstable and should be treated as contextual metadata, not official ground truth.
- FH cluster storage is not assumed. Cluster Spark writes to the project `data/` folder must not be claimed unless shared storage is proven.
- Air quality station representativeness and city-level aggregation are simplifications that must be discussed in the final story.
