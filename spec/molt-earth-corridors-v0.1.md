# molt.earth — Corridors v0.1

Status: Proposal · Pilot: COTA → CDMX · Mode: Simulation-first  
Owner: æ Studio / Agentic Environments

## Goal

Convert a geographic corridor into an auditable operational workflow incorporating a map, timeline, checkpoints, border/safety alerts, agent handoffs, and mandatory human approval for high-risk actions.

## Scope

- Map: GeoJSON corridor segments and checkpoints with provenance and verification state.
- Timeline: planned/actual timestamps in UTC, rendered with IANA time zones.
- Checkpoints: origin, intermediate stop, border, destination.
- Alerts: severity, source URL, fetched/observed/expiry times, evidence hash.
- Agent handoffs: persisted workflow state, correlation IDs, bounded retries.
- Human approval: version- and payload-bound decision gate.

Out of scope: automated border crossing, autonomous real-world travel instructions, payments, reservations, vehicle control, personal tracking.

## Reference stack (adapt to existing repo)

- Next.js + TypeScript + MapLibre GL JS
- FastAPI + Pydantic
- PostgreSQL + PostGIS
- Transactional outbox + background worker, SSE, OIDC/JWT, OpenTelemetry

## Data model

- corridors(id UUID PK, slug UNIQUE, name, status, version INT, owner_id, created_at, updated_at)
- checkpoints(id UUID PK, corridor_id FK, name, kind, location GEOGRAPHY(Point,4326), planned_arrival, actual_arrival, status)
- segments(id UUID PK, corridor_id FK, sequence INT, origin_checkpoint_id FK, destination_checkpoint_id FK, geometry GEOGRAPHY(LineString,4326) NULL, status, verification_status, estimate_seconds NULL)
- alerts(id UUID PK, corridor_id FK, segment_id FK NULL, source_url, source_name, source_observed_at, fetched_at, expires_at, severity, verification_status, summary, evidence_hash, state)
- agent_runs(id UUID PK, corridor_id FK, agent_type, task_type, input_ref, output_ref, status, correlation_id, created_at, finished_at)
- handoffs(id UUID PK, run_id FK, source_agent, target_agent, task_ref, status, created_at, acknowledged_at)
- approvals(id UUID PK, corridor_id FK, action_type, payload_hash, corridor_version, status, requested_by, decided_by NULL, reason NULL, created_at, decided_at, expires_at)
- events(id UUID PK, corridor_id FK, event_type, schema_version, aggregate_version, correlation_id, causation_id NULL, producer, payload JSONB, occurred_at)

Add foreign keys, GiST indexes, unique (corridor_id, sequence), and append-only audit/event storage.

## REST API /api/v1

| Method | Path | Purpose |
|---|---|---|
| POST | `/corridors` | Create draft |
| GET | `/corridors/{id}` | Corridor state |
| PATCH | `/corridors/{id}` | Edit draft |
| GET | `/corridors/{id}/geojson` | Map data |
| GET | `/corridors/{id}/timeline` | Timeline |
| POST | `/corridors/{id}/checkpoints` | Create checkpoint |
| GET | `/corridors/{id}/alerts` | Alerts with provenance |
| POST | `/corridors/{id}/agent-runs` | Launch bounded agent task |
| GET | `/agent-runs/{id}` | Task status |
| POST | `/corridors/{id}/approvals` | Request decision |
| POST | `/approvals/{id}/decisions` | Human approve/reject |
| POST | `/corridors/{id}/transitions` | State transition |
| GET | `/corridors/{id}/events` | Audit events |
| GET | `/corridors/{id}/stream` | SSE stream |

API rules: idempotency keys for POST mutations, If-Match for state changes, structured problem+json errors, permission checks per corridor, UTC API timestamps, RFC 7946 GeoJSON.

## State machine

DRAFT → PROPOSED → UNDER_REVIEW → APPROVED → ACTIVE → COMPLETED.

ACTIVE ↔ PAUSED only with required guards; CANCELLED available from nonterminal states with authorization. High-risk changes require a fresh human approval bound to both corridor version and action payload hash.

## Agents and permissions

- Geo: verifies geometry/provenance; cannot certify travel safety.
- Risk: evaluates sourced alerts and expiry; can request preventative pause.
- Timeline: computes dependency/ETA estimates with uncertainty.
- Approval: prepares approval request; cannot self-approve.
- Event: publishes outbox records; consumers idempotent.
- Audit: verifies lineage and state transitions.

All agents use least-privilege identities, limited tool permissions, and traceable runs.

## Event contract

Envelope: event_id, type, schema_version, corridor_id, aggregate_version, correlation_id, causation_id, producer, occurred_at, payload.

Events: corridor.created, corridor.proposed, route.verified, checkpoint.arrived, alert.raised, alert.stale, corridor.paused, agent.handoff_requested, agent.handoff_completed, approval.requested, approval.granted, approval.rejected, corridor.activated, corridor.completed.

Transactional outbox; at-least-once delivery, deduplication by event_id.

## Approval policy

Require explicit human authorization to activate an international corridor, modify an approved route, confirm a border-crossing plan, resume after a critical alert, or override a policy where permitted. An approval is invalid if payload hash/version changed, it expired, or supporting evidence became stale. Critical verified alerts and non-overridable technical restrictions block activation regardless of approval. Record identity, timestamp, reasoning, and evidence.

## Pilot fixture: COTA-CDMX

Origin: Circuit of the Americas (Austin, America/Chicago).  
Destination: Autódromo Hermanos Rodríguez (Ciudad de México, America/Mexico_City).

Candidate simulation-only checkpoints: COTA, Laredo, Nuevo Laredo, Monterrey, San Luis Potosí, Autódromo Hermanos Rodríguez. Not a recommended safe driving route. Never treat unverified route geometry or outdated border advisories as operational instructions.

## Acceptance criteria

- AC01: Authenticated creation produces exactly one DRAFT and corridor.created.
- AC02: GeoJSON correctly renders verified checkpoints and labels unverified geometry.
- AC03: Timeline displays planned vs actual times with correct time zones.
- AC04: Verified critical alert blocks activation and yields auditable event.
- AC05: Expired evidence becomes STALE and cannot authorize real-world action.
- AC06: Geo → Risk handoff preserves correlation, input/output references, status.
- AC07: Activation without valid approval returns HTTP 409 without state mutation.
- AC08: Stale version/payload makes previous approval unusable.
- AC09: Duplicate idempotent request yields no duplicate logical action or events.
- AC10: Events and approval history can be retrieved in audit order.
- AC11: Unauthorized corridor access returns HTTP 403.
- AC12: E2E simulation demonstrates create → verify → alert → pause → approval → resume → complete with no external physical action.

## Definition of done

Reproducible migrations, OpenAPI validation, unit/integration/E2E tests covering AC01–AC12, access-control tests, outbox recovery tests, logging/tracing, CI receipts, and security/privacy review.

## Suggested implementation order

1. Repo scaffolding + CI, database migrations.
2. API contracts, auth/RBAC, optimistic concurrency.
3. Map + timeline + checkpoint UI.
4. Provenance-aware alerts and outbox/handoffs.
5. Human approval gates.
6. Simulation fixture and AC01–AC12 test suite.

> This file is a specification, not a claim that the implementation, repository commit, or CI verification has happened.
