# Phase 2 — Identity and Multi-Tenancy

Phase 2 adds authentication, rotating refresh sessions, organizations, RBAC, workspaces, projects, and tenant-aware authorization.

## Security decisions
- Passwords use Argon2.
- Access tokens are short-lived JWTs.
- Refresh tokens are opaque random values; only SHA-256 hashes are persisted.
- Refresh tokens rotate on use.
- Cross-tenant access returns 404 where practical to avoid resource enumeration.
- RBAC is permission-based rather than route-specific role checks.
- Refresh credentials are HttpOnly cookies; the demo uses `secure=false` for localhost and must use secure cookies behind HTTPS in production.

## Role hierarchy
Owner > Admin > Developer > Viewer.

## Phase 3 dependency
Agent executions will attach to `Project`, making this tenancy model the security boundary for all future workflows.
