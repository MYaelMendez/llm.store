# RFC-0003 — Chat-to-Environment Recursive Compiler
Status: proposed specification; consolidated from the æ Agentic Electronic Engineering conversation (2026-10-14)

## Principal and syntax
`>_æææ://|||` invokes a human-governed compiler ontology. `|||` composes independent parallel tasks; `^` composes bounded hierarchical agent delegation; `↺` reintegrates results and updated human state. These are proposed syntax, not verified executable compiler operators.

**Invariant: many agents, one principal; context may propagate, authority does not.** Every branch has separate authorization, scope, deadline, cancellation, budget, and Witness receipt. No recursive escalation.

## Compile the conversation into eight workstreams
1. **🏢⁹:¹⁶ LIFE TOWER** — one mobile-first viewport with transparent floors for Home, Health, Learn, Faith, Build, Business, Economy, Impact, Move, Construct, Witness, Govern.
2. **🧠ᵐ MODEL MESH** — every widget has an OpenAI model picker, using actual account availability and task compatibility; `auto` fallback. No implied API entitlement.
3. **🛸ᵃ AGENT MESH** — capability discovery, bounded delegation, parallel queues, asynchronous waits, cancellation, retries, human approvals.
4. **▦ᑫ QR NETWORK** — per-widget versioned shareable HTTPS descriptor; QR conveys identity and entry, never credentials or authority.
5. **💵 CIRCULAR ECONOMY** — scan → useful service → consent → settled transaction → refund/fee/cost reconciliation → net contribution → reinvestment. No speculative earnings or recruitment-based rewards.
6. **🧾 WITNESS** — signed/attributable receipts for execution, permissions, source provenance, costs, and errors; receipt does not itself confer authority.
7. **📦 PUBLISH** — GitHub-native forkable specification and website, OpenAI conversational surface, named domains linking to versioned contracts; no automatic cross-platform deployment.
8. **🎙️ TELEPROMPTER** — real event-driven rails for intent, plan, authorize, queued, running, waiting, deferred, human review, verified, failed, returned. Decorative motion must be marked as illustrative.

## Widget contract (proposal)
```json
{
  "schema":"ae.widget.v1",
  "widget_id":"home",
  "widget_version":"1.0.0",
  "model_profile":"auto",
  "qr_entry_url":"https://example.org/ae/widgets/home",
  "agent_capabilities":[],
  "authority":{"principal_required":true,"delegation":"explicit","inherited":false},
  "execution":{"async":true,"max_depth":3,"max_parallel":4,"timeout_ms":60000},
  "witness":{"required_for_consequential_actions":true}
}
```
Numbers and URL are example defaults, not deployed service limits.

## Compilation algorithm
1. Extract user intent, explicit decisions, constraints, and unverified claims.
2. Normalize to a typed capability DAG with provenance per node.
3. Split independent tasks using `|||`; build nested bounded task trees using `^`.
4. Resolve providers/models/devices against actual availability, consent and cost.
5. Gate side effects with human principal authorization.
6. Execute asynchronously; track durable state and idempotency keys.
7. Reconcile receipts, errors, and actual cost; return actionable summary to principal.
8. Publish only reviewed, non-sensitive outputs to versioned repositories and domains.

## Human peace-of-mind acceptance
One viewport clearly distinguishes queued, running, waiting, approval-needed, failed, completed, and simulated. One tap can pause or revoke authorized work. No silent authority transfer; no fake live earnings or device state.

## Implementation status
**Specification captured only.** GitHub documentation commits are not proof of live model routing, MCP connectivity, QR generation, cross-device sync, background workers, or verified payments.

## Network motto
**PEOPLE BUILD TOMORROW.** One viewport. A life's tower of agents. Many devices, many models, many agents, one principal.
