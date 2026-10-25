# æ.store

**The governing registry and provisioner for human-governed virtual computers in the Internet of Agents.**

Transform purpose into enterprise. Many agents. One human principal.

## The product

The primary artifact is a **virtual computer**: a versioned environment definition with a declared runtime image, capabilities, governance policy, resource limits and export path. æ Studio is its conversational workspace and control surface. Agents are processes inside the environment, not its owners.

This directory incubates the æ.store foundation within the existing **llm.store** repository. It does not rename that repository, change a domain, create a marketplace service, or replace its existing contracts.

## Current implementation boundary

| Item | Status in this directory |
| --- | --- |
| Charter, architecture and human-root contract | Written specification |
| Default computer manifest | Proposed configuration; no image attached |
| Registry manifest schema | JSON Schema document; no registry validator/service installed |
| DAO governance template | Proposed policy document; no deployed DAO or legal entity |
| Provisioning, VM isolation, credentials and runtime enforcement | Not implemented here |
| Signed registry entries, revocation service and execution receipts | Not implemented here |

The manifest is **not a bootable image**. There is no provisioner executable, hypervisor, OS kernel or resource isolation implementation in this foundation. Existing Studio interface behavior does not prove those capabilities. Browser presentation, model inference and an isolated virtual computer are distinct layers.

## Roles

| Layer | Responsibility |
| --- | --- |
| Chat / æ Studio | Express intent, compose, inspect, approve and receive results |
| Agents / models | Perform bounded work under explicit grants |
| æ.store | Register, resolve, distribute and request provisioning under published policy |
| Virtual computer | User's runtime and state boundary; must be verified by a provider adapter |
| DAO | Optional collective governance under an explicitly adopted policy |
| human://root | Human authority root; delegation is scoped, explicit and revocable |

## Foundation layout

- [CHARTER.md](CHARTER.md): authority, stewardship and publication rules.
- [computers/default/manifest.json](computers/default/manifest.json): deliberately unbound computer template.
- [computers/default/governance/dao.template.json](computers/default/governance/dao.template.json): collective-governance proposal.
- [computers/default/agents/README.md](computers/default/agents/README.md): optional process boundaries.
- [registry/schema/computer-manifest.schema.json](registry/schema/computer-manifest.schema.json): proposed manifest format.
- [modules/README.md](modules/README.md): widget, skill and harness contracts.
- [docs/architecture.md](docs/architecture.md): target provisioning lifecycle and verification gates.
- [docs/human-root.md](docs/human-root.md): human authority and DAO delegation.

## First implementation milestone

Implement one provider adapter that accepts a reviewed manifest plus a separately verified provisioning grant, creates one isolated sandbox, proves its resource and access boundaries, returns an exportable receipt, and disposes of its bootstrap credentials. Include refusal, stale-version, revocation, duplicate-request and cleanup tests before claiming provisioning works.

No infrastructure is provisioned by cloning, registering or reading this repository. No secret, private conversation or authorization grant belongs in a public manifest.

The repository's [LICENSE](../LICENSE) applies to this foundation; third-party images and modules retain their own licenses. A proposed artifact without a resolvable source, license and digest must not be released as a runnable computer.

**Context may propagate; authority does not.**
