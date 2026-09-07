# Phase 1 Architecture

ForgeOS begins as a modular monolith rather than premature microservices.

```text
Browser
   |
   v
Next.js / TypeScript
   |
   | REST
   v
FastAPI / Python
   |          \
   v           v
PostgreSQL    Redis
```

## Boundaries

- `api`: HTTP transport and routing.
- `services`: business use-cases.
- `repositories`: persistence abstraction.
- `models`: SQLAlchemy persistence entities.
- `schemas`: API contracts.
- `core`: configuration, logging, exceptions.
- `middleware`: cross-cutting request behavior.

## Reliability

The API exposes separate liveness and readiness probes. Liveness verifies the process can respond. Readiness verifies PostgreSQL and Redis are usable before traffic should be routed to the service.
