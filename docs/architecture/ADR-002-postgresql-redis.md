# ADR-002: PostgreSQL for durable state and Redis for ephemeral state

## Status
Accepted.

## Decision
Use PostgreSQL for relational transactional data and Redis for low-latency ephemeral state, caching, rate limiting, and future queue coordination.
