# æ · Network Consolidation RFC 0002
Status: DESIGN BASELINE · 2026-10-14

## Purpose
Preserve the consolidated usability and sustainability architecture across the æ network. This is a design baseline, not a claim that integrations, revenue, or real-time synchronization have been implemented.

## Human invariant
**Many agents. One principal. Context may propagate; authority does not.**
No plugin, agent, QR code, household member, or fork inherits authorization merely by receiving context. Human consent, least privilege, provenance, and revocation govern actions.

## One architecture, three surfaces
1. **Viewport** — responsive 9:16 mobile-first, transparent glass widgets, animated colored signal rails, emoji launchers, high contrast and reduced-motion alternatives.
2. **Chat** — natural-language and voice-first commands; symbols are shortcuts, never mandatory.
3. **Compute** — discovered and authorized capabilities, MCP/WebMCP/AndroidMCP adapters where supported, asynchronous workers, durable events, receipts.

These surfaces are not inherently synchronized. Live state requires implemented identity, transport, storage, permissions and reconciliation.

## Unified entry
- `$æ` conceptual agentic engineering entry; `$ae` ASCII fallback where registered.
- `$🏡` Agentic Home conceptual launcher.
- `🤝` connect/share/consent entry; never silently authorizes external access.
- QR codes resolve to versioned HTTPS entrypoints with clear ownership and campaign metadata.
- `#startabusiness` and `/cli` are user-facing pathways, not claims of deployed routing.
- Each domain can point into a shared specification without duplicating authority or claiming automatic network propagation.

## Usability system
- Transparent modular widgets, differentiated semantic colors, flowing arrows and motion for actual event state; never show decorative motion as live telemetry.
- Three lanes: 🟨 Discover, 🟦 Engineer, 🟩 Govern.
- Secondary domains: 🟪 Economics, 🍊 Growth, pink Household.
- Compact emoji affordances plus accessible text labels; touch targets, screen-reader descriptions, localization, low bandwidth, offline fallbacks.
- Household flows: 🍼 bottle, 📺 remote, 🛒 shopping, ☕ coffee; sensor/tracker findings only if verified by connected devices.
- Life-stage examples: 🤰 pregnancy, 🏥 birth, 🍼 newborn, 🧸 toddler. Educational support only; clinician-reviewed medical content and urgent human escalation required.

## Circular QR economy — first implementation target
```
▦ SCAN → 🏡 USE → 🤝 VERIFIED VALUE → 💵 REVENUE
       → 🧾 ATTRIBUTION & COST → ⚡ COMPUTE → ♻️ REINVEST ↺
```
Economic transactions must deliver independent user value. Never reward recruitment alone or represent referrals as guaranteed earnings.

### Minimum test
1. One physical or digital QR campaign and canonical landing URL.
2. One useful service with disclosed partner economics and opt-in.
3. Event sequence: scan (privacy-safe), landing, consent, qualified action, verified transaction, refund/chargeback, attributable commission/payment, operating cost.
4. Idempotent transaction receipts; no payment credentials in QR payloads.
5. Metrics: unique scans, qualified usage, conversion, attributed settled revenue, fees, direct compute/hosting/support costs, net contribution, repeat usage, refund rate.
6. Acceptance: end-to-end transaction verified and reconciled, correct attribution, no silent permission elevation, accessible 9:16 UI, explicit simulation labels, documented net contribution.

`Net contribution = settled revenue - refunds - payment fees - partner costs - direct compute/hosting/support costs.`

## Repositories and responsibilities
- `MYaelMendez/llm.store`: AHTML contracts, capability discovery, runtime, witness and canonical economic spec.
- `MYaelMendez/MYaelMendez.github.io`: public viewport and usability reference, including links to canonical spec.
- Other named domains and projects may reference this baseline through versioned links. Publishing this document does NOT deploy it across all domains.

## Implementation backlog
P0: QR attribution schema, consent UX, real transaction and cost receipts, dashboard with verified/simulated distinction.
P1: modular transparent widgets and accessible 9:16 viewport, offline cache, event-backed motion.
P2: authorized adapters and async orchestration; cross-device sync; forks with explicit permissions.

## Verification status
Design consolidated in conversation. No claims of completed live payments, MCP connectivity, cross-device state, or deployed QR campaign. Test each independently before marking shipped.
