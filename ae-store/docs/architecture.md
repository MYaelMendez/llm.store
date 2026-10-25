# Architecture · target, not deployed infrastructure

The product is a human-governed virtual computer. Studio is the interface to it. This directory supplies a proposed descriptor and charter; it does not yet supply the runtime.

## Target lifecycle

1. **Declare:** human chooses purpose, resources, providers and governance. Record a versioned manifest; reject missing source, license, image digest or governance.
2. **Review:** resolve dependencies, inspect provenance, determine compatibility, resource costs and residual provider control. Record which claims are verified.
3. **Authorize:** obtain a distinct provisioning grant bound to principal, manifest digest/version, target provider, resources, spend ceiling and expiry. A repository file is not that grant.
4. **Provision:** an authenticated adapter applies an idempotency key, creates the isolated runtime and initializes policy. A descriptor must never select arbitrary shell commands from untrusted metadata.
5. **Verify and hand over:** test isolation, least privilege, network/resource boundaries, cleanup and recovery. Return provider IDs and an export path. Revoke bootstrap credentials and disclose residual provider administration.
6. **Operate:** each agent/tool action checks its own grant and policy. Model output is untrusted. No inherited authority between processes or nested computers.
7. **Reflect and renew:** the human reviews results and proposes changes. A new manifest or policy version does not automatically authorize migration.
8. **Exit:** export permitted state and evidence, revoke grants, stop billed resources under an explicit teardown grant, and verify provider cleanup.

## Registry boundary

A future registry must validate schemas and artifact digests, track publisher provenance and immutable versions, identify revocations, and separate draft/reviewed/released states. The manifest and governance schemas describe the deliberately unbound proposal format only. The offline validator enforces that bounded vocabulary and policy hash consistency. It is not a runtime policy engine, package installer or complete release validator.

## Computer image boundary

A future release must identify its actual image format, source/build revision, immutable digest, supported architecture, provider compatibility and license. An interface hosted in a browser does not establish a VM, hardware virtualization, sandbox isolation, persistent disk, safe networking or resource metering. Those require implementation and execution evidence.

## Relationship to existing work

llm.store keeps its current site and [codæ plan/receipt specifications](../../packages/codae-core/README.md). Those contracts remain specification-first. The existing OpenAI-hosted Studio, GitHub Pages and chat are peer interfaces; this proposal does not synchronize their state or credentials. Existing application identity and API integration need their own verified authorization and hosting contracts.

## Acceptance before claiming the first provisioned computer

- Exact manifest, image digest, governance policy and separate grant are validated server-side.
- Anonymous, unauthorized, stale, revoked and over-budget provisioning is refused without creating resources.
- Duplicate requests create at most one logical computer; failures and recovery reconcile with the provider.
- Isolation, network/resource restrictions, credential teardown and export are exercised with real execution records.
- No operator runtime grant remains after handover; provider administration and recovery limits are disclosed.
- Runtime and DAO capabilities are described only to the extent their enforcement was tested. A DAO template is not a legal entity.

