# Emoji plugin release factory

GitHub is the source of truth for these public-upload candidates. The first four entry points are 🔍 search, 📋 capture, 🏎️ motorsports and 📺 television/briefings.

## Build

Requires Python 3.10+; no package installation, API keys or network calls.

```bash
python3 scripts/test_plugin_factory.py
python3 scripts/build_plugins.py
```

The manual **Build emoji plugin drafts** workflow and matching pull requests produce four complete ZIPs and individual readiness receipts as Actions artifacts. Each ZIP opens directly at `plugin.json`, contains its real PNG icon, skill and support files, and includes a SHA-256 source inventory. ZIP timestamps, permissions and file order are fixed; identical source and revision produce identical bytes. ZIP hashes and per-file hashes are recorded outside the ZIP in `plugin-dist/`.

A clean Git checkout records its actual HEAD revision in the receipt. A dirty or non-Git build records a null revision; source hashes remain available. Hashes provide integrity checks, not cryptographic signatures or publisher verification.

## Source and listing

- `plugins/catalog.json`: exact imported private release identities and versions.
- `plugins/<role>/`: complete imported sources, preserved verbatim, including compatibility manifests and icons.
- `publication/<role>.json`: separate public listing drafts, with useful descriptions and release notes. Builds overlay metadata in memory; private plugin sources are not rewritten.
- `publication/settings.json`: unresolved publisher, country and commerce decisions. Null means unknown. An explicit empty country array means all available countries; do not use it without the publisher's choice.

Public copy retains emoji names and original starter prompts. The sources were imported from the user's four owned workspace plugins; no account credentials, private knowledge uploads, App binding or MCP server is included. Editing this repository does not update installed private plugins automatically. Public updates must preserve their own portal-generated identity and binding.

## Public review preparation

All four packages currently have **draft_not_submitted** status. They are skills-only; MCP review cases, a demo recording and reviewer credentials do not apply to this release type. They use tools available in the host; the skills themselves add no search API, account connection, live feed, background clipboard monitor or cross-plugin router. Runtime evaluations have not been recorded.

Before submission, complete these concrete items:

1. Select the intended verified individual or business publisher; confirm redistribution rights and country targeting.
2. Confirm whether these plugins themselves involve purchases/payments.
3. Provide and verify each plugin's public website, support page, privacy policy and terms URLs. Set the four URL fields under the listing overlay's `interface`. Inspect actual page content and unauthenticated access before adding a URL to `verified_urls`; an HTTP status alone is insufficient. Do not invent support contacts, data retention practices or legal promises.
4. Confirm the supported dashboard category and icon legibility on light and dark surfaces. Existing square 512px PNG assets pass local dimensions/size checks.
5. Rebuild, inspect the exact ZIP, and complete target portal validation, publisher/domain verification and required attestations. Submission and publication are separate steps and require their actual confirmations.

The builder implements focused structural checks, not the complete portable schema or a guarantee of review approval. `--require-ready` exits 2 while external review/attestation gaps remain; ordinary draft builds succeed while reporting gaps. Never bypass those gaps by marking unverified information confirmed.

## Adding a plugin

Add its reviewed complete source directory and catalog entry with an observed release ID. Add a separate public listing overlay, extend the tests and inspect redistribution rights. Do not package a private App binding as a public upload. App-backed æ Studio must retain canonical Sites App ownership and use a compatible submission path; do not create a duplicate private Studio plugin.

## White labeling

Fork the repository, adapt names, branding and workflows, then establish your own publisher identity and policy pages. A fork carries code and context; it does not carry the original publisher's account access, tool grants or authority. Preserve applicable licenses and notices.

Many agents. One principal. Context may propagate; authority does not.

References: [OpenAI submission](https://developers.openai.com/plugins/deploy/submission), [GitHub workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands).
