# ADR-003: City Reference Model

## Status
Accepted

## Context
Multiple sources use different city naming conventions and metadata completeness.

## Decision
Adopt a unified city reference model for source harmonization in downstream layers.

## Phase 2 Review - 2026-05-30
Reviewed during Issue 2.2. The decision remains unchanged.

The Phase 2 schema uses `city_id` as the stable join key and records city
coordinates, EEA station mapping notes, and Wikipedia metadata linkage fields.
The schema deliberately separates source alignment notes from later ingestion
logic. EEA ingestion, Wikipedia parser implementation, Open-Meteo client
implementation, Kafka, and Spark remain out of scope for this ADR review.

## Consequences
Additional mapping effort is required, but joins and analytics become more consistent.
