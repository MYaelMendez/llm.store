# Optional starter agents

No agent runtime is installed by this directory.

Future modules can propose bounded roles: builder, inspector and witness. Each declaration must identify its source/version, input/output contract, tools, limits and verification state. Installation is distinct from execution; each invocation needs a valid grant. Review agents cannot approve on behalf of a human unless the adopted policy explicitly delegates that exact decision within a bounded scope.

Do not place credentials, live grant tokens, private context or arbitrary executable bootstrap scripts in a published computer manifest.
