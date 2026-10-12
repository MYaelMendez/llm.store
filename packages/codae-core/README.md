# codæ Core · Universal Code Mode

Portable execution contracts for **llm.store**.

**Invariant:** Context may propagate; authority does not.

## Flow

HUMAN://intent → DISCOVER → AHTML://proposal → COMPOSE → HUMAN://authorize → EXECUTE → WITNESS://receipt → HUMAN://return

## What v0.1 contains

- `schemas/plan.schema.json`: versioned, provider-independent plan format
- `schemas/receipt.schema.json`: execution receipt envelope
- `examples/meeting.plan.json`: safe, local-only sample

A plan is **never an authorization**. The executor must verify a separately issued, principal-bound, scoped, time-limited grant before consequential execution. Receipts describe observations, not automatically cryptographic proof.

## Integration contract

An LLM adapter emits a plan conforming to the schema. A capability registry resolves declared capabilities. A policy engine evaluates requested scopes. An executor validates a real authorization grant and runs only allowlisted capabilities in isolation. A witness service records the result.

This package is specification-first. It does **not** yet include a Cloudflare Worker, live LLM provider adapters, credential management, a policy service, or signed receipts.

Public browser demonstration: https://myaelmendez.github.io/codae/
