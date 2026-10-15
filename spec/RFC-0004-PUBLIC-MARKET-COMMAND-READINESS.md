# RFC-0004 — $æ Public Command & Control / Market Readiness
Status: **public-preview candidate; not an approved financial product or securities offering**
Date: 2026-10-14

## Product
The `$æ` console is a mobile-first 9:16 agentic command-and-control interface. Prototype: https://github.com/MYaelMendez/MYaelMendez.github.io/blob/gh-pages/ae/control/index.html

### Shipped in this iteration
- Four independent teleprompter panels: principal intent, compiler, agent orchestration, Witness/markets.
- Three independently animated tickers: operations, agents, market-data connection status.
- Twelve selectable life-tower floors; each displays `🧠ᵐ · ▦ᑫ · 🛸ᵃ · 🧾ʷ`.
- Command parser for local demo commands `status`, `inspect`, `publish`, and arbitrary intents.
- Local event log, pause/resume animation, model preference mock selector, unsigned JSON demo receipt export.
- Visible link from existing `/ae/` entrypoint; coffee and handshake preserved.
- Explicit zero active agents, no market prices, no API keys, no order execution, no invented live telemetry.

### Architecture requirements
Event stream envelope: `event_id`, `occurred_at`, `ingested_at`, `source_id`, `source_url`, `source_timestamp`, `principal_id`, `task_id`, `parent_task_id`, `state`, `severity`, `authorization_ref`, `witness_ref`, `cost`, `is_simulated`.
Teleprompter priority: human approvals > errors > task progress > informational feeds. Implement backpressure, source freshness, filtering, and deduplication before live integrations. Animations are not evidence of execution.
Ticker contracts: **source, symbol/metric, timestamp, units, market session, delayed/live indicator, licensing, error/fallback**. Never display market figures without data rights and provenance.
Command gating: readonly status first; writes require principal identity, least-privilege consent, idempotency, revocation, audit trail, and fail-closed execution.

## Public launch checklist
- [x] Open-sourceware proof-of-concept UI and source committed.
- [x] Explicit simulated/no-feed indicators.
- [x] Human control and pause of ticker animations.
- [x] Local demo event export.
- [ ] Verify production hosting, routing, accessibility, and mobile browser QA.
- [ ] Security review: CSP, XSS, dependency supply chain, secrets, privacy notice, rate limits.
- [ ] License and third-party trademark/brand review.
- [ ] Actual agent runtime and model selection with provider authentication.
- [ ] Signed receipts and tamper-evident Witness verification.
- [ ] Authorized QR descriptor/scan flows.
- [ ] Authorized, licensed market-data provider, timestamps and delayed/live disclosures.
- [ ] Market-data redistribution and exchange agreements as applicable.
- [ ] Privacy policy, terms, consumer-support channel, incident response.
- [ ] Public docs, screenshots, versioned API schemas, smoke tests, CI and release tag.

## Separate financial-markets track
If “submittal for public markets” means securities issuance/listing, brokerage, investment advisory services, or market-data commercialization, **do not infer readiness from software deployment**. Obtain appropriate professional legal, regulatory, and accounting advice; establish legal issuer/entity and capitalization, audited financial statements where applicable, disclosures, exchange/SEC or jurisdiction-specific eligibility, data licensing, and approvals. This RFC makes no claims of registration, investment performance, offering availability, or listing eligibility.

## Next implementation slice
1. Read-only real event adapter with source timestamps and signed provenance.
2. Schema validation, permissions, receipt storage, deterministic replay.
3. Teleprompter filters by source, priority, and floor.
4. Instrumentation: verified outcomes / (tokens + compute cost), plus human approval burden.
5. GitHub Actions CI and staging smoke test before marking production-ready.

**Many agents. One principal. Coffee and handshake included.**
