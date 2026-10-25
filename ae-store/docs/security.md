# Foundation security boundary

## Protected assets and actors

Human decision authority, future provider credentials, private context, billed resources and auditable policy versions must stay separate from published metadata. Treat publishers, imported templates, modules, model output and registry descriptions as untrusted until verified. Repository write access is not a grant to provision a computer.

## Implemented defenses

- The offline CLI is read-only, bounded to local files and requires no network or third-party packages. It does not execute manifest content or follow remote schema references.
- Object fields are closed and required. Unknown schema keywords fail closed. Duplicate JSON keys, malformed/non-finite JSON, control-character metadata, files over 64 KiB and symlink references are rejected.
- Default proposals remain inactive: no image, adapter, modules, agents, grants, publisher identity, released artifact, allocated resources or execution evidence is permitted. Human-root authority and noninheritance are explicit invariant checks.
- Exact-byte SHA-256 bindings connect the manifest to the charter and governance template. Stale files and mismatched versions fail validation. The CLI never rewrites these bindings.
- The inactive DAO template cannot claim members, an adopted decision rule, legal formation, delegated scopes or working runtime enforcement.
- CI uses the pull_request event, read-only contents permission, a pinned checkout action, no persisted checkout credentials, a timeout and no provisioner/provider secrets. Existing production deployment workflow is unchanged.

## Tested attacks

The standard-library test suite checks privilege escalation, retained operator authority, invented runtime/verification/release state, nonzero resource allocation, live-DAO claims, paths outside the declared policy set, remote references, malformed/duplicate/oversized JSON, symlinks, version mismatches and policy tampering. It also verifies that failure output does not echo a supplied private-data sentinel and that validation does not repair a tampered manifest.

## Limits

A content hash is not a publisher signature, human approval, trusted timestamp or independent attestation. Someone who can modify both a policy and its binding can create an internally consistent proposal. Human review, protected branches and a separate future signature/trust contract are required. This validator does not establish authenticated identity, defend a compromised CI runner, prevent concurrent filesystem replacement by a privileged local actor, or make arbitrary repository code safe to run.

This is a bounded implementation of the included schema vocabulary, not a general JSON Schema validator. Do not extend schemas with unsupported keywords and assume they are enforced. The CLI must reject the extension until reviewed implementation and negative tests exist.

No VM/sandbox, durable revocation, grant verification service, image admission, resource metering, monetary budget, provider adapter, signed receipt, legal entity or DAO enforcement is implemented. Do not widen proposal states or add executable artifacts as a shortcut to provisioning. A future runnable release requires its own reviewed format, authenticated grant path and execution evidence.

Provider host-level administration may persist even after application/bootstrap grants are revoked. Any future sovereignty claim must disclose actual provider control and recovery/exit limitations.

Do not submit credentials, live grants, personal identity documents or private context to this public repository. A green check does not authorize deployment or execution.

## References

- [JSON Schema structural validation vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
