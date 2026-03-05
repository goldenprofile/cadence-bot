# Decision Log (ADR)

## 2026-03-05 — SQLite over Postgres/JSON/Pickle

**Context:** Personal bot, no concurrent load.
**Decision:** SQLite via `aiosqlite`.
**Rationale:** ACID guarantees, no server, human-readable with DB Browser, easy migration path to Postgres if needed. JSON risks corruption on crash; Pickle is opaque and brittle.
