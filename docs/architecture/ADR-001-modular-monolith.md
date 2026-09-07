# ADR-001: Start as a modular monolith

## Status
Accepted.

## Context
ForgeOS will eventually contain independent workloads, but Phase 1 does not yet justify distributed-service operational overhead.

## Decision
Use one FastAPI deployable with strict module boundaries and extract services only when scaling, ownership, or reliability requirements justify it.

## Consequences
Development remains fast while preserving a clear migration path to services later.
