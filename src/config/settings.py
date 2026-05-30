"""Environment-driven project settings.

The module is side-effect free: it reads environment variables only and does
not start services, open network connections, or create files.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectSettings:
    """Runtime settings used by later pipeline phases."""

    execution_env: str = "local_project"
    open_meteo_base_url: str = ""
    spark_master_url: str = "local[*]"
    cluster_spark_master_url: str = "spark://172.29.16.102:7077"
    kafka_bootstrap_servers: str = "172.29.16.101:9092"
    kafka_topic_air_quality_live: str = "bdeng_g1_air_quality_live"
    project_timezone: str = "UTC"
    data_dir: str = "data"
    checkpoint_dir: str = "data/checkpoints"
    log_level: str = "INFO"


def get_settings() -> ProjectSettings:
    """Return project settings from environment variables with safe defaults."""
    return ProjectSettings(
        execution_env=os.getenv("EXECUTION_ENV", "local_project"),
        open_meteo_base_url=os.getenv("OPEN_METEO_BASE_URL", ""),
        spark_master_url=os.getenv("SPARK_MASTER_URL", "local[*]"),
        cluster_spark_master_url=os.getenv(
            "CLUSTER_SPARK_MASTER_URL",
            "spark://172.29.16.102:7077",
        ),
        kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "172.29.16.101:9092"),
        kafka_topic_air_quality_live=os.getenv(
            "KAFKA_TOPIC_AIR_QUALITY_LIVE",
            "bdeng_g1_air_quality_live",
        ),
        project_timezone=os.getenv("PROJECT_TIMEZONE", "UTC"),
        data_dir=os.getenv("DATA_DIR", "data"),
        checkpoint_dir=os.getenv("CHECKPOINT_DIR", "data/checkpoints"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
