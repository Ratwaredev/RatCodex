# RatCodex

> An open, license-aware registry of reusable development resources with explicit trust evidence for humans and AI agents.

RatCodex is not a link dump and it is not a mirror of whatever is public on the internet. A resource only becomes reusable here when its provenance, rights and exact packaged content are known. `copyReady` is stricter: it also requires a reproducible runtime test.

## Trust model

RatCodex keeps four separate claims instead of collapsing them into one badge:

| Claim | What it means |
|---|---|
| **Rights verified** | The license and redistribution policy have evidence. |
| **Integrity verified** | Packaged files match recorded byte sizes and SHA-256 hashes. |
| **Runtime tested** | A checked-in test was executed by an allowed RatCodex runner. |
| **Copy ready** | Rights allow reuse, integrity is anchored, and runtime validation passed. |

A public GitHub repository is not automatically reusable. A valid hash is not a runtime test. A runtime test does not override a restrictive license.

The validator rejects `copyReady: true` unless all required evidence exists.

## Current catalog

The catalog currently contains four normalized packages:

- `python.retry-with-backoff` — runtime tested, copy ready.
- `python.atomic-json-write` — runtime tested, copy ready.
- `node.safe-json-fetch` — runtime tested, copy ready.
- `godot.hierarchical-finite-state-machine` — rights and integrity verified, but **not runtime tested by RatCodex yet**, so it is not marked copy ready.

The first three packages are intentionally small. They establish the quality gate before the catalog grows.

See [`catalog/index.json`](catalog/index.json) for the machine-readable index.

## Package format

```text
packages/<id>/
├── manifest.json          # provenance, rights, compatibility, validation, integrity
├── SKILL.md               # compact AI/human usage instructions
├── templates/             # reusable implementation
├── tests/                 # reproducible package tests when applicable
├── assets/                # verified reusable assets when applicable
├── references/            # redistributable reference material
└── NOTICE.md              # attribution and upstream notices
```

The canonical contract is [`schemas/resource.schema.json`](schemas/resource.schema.json).

## Validation

`python scripts/validate.py` checks catalog consistency, rights policy, safe paths, required notices, previews, exact file sizes and SHA-256 hashes. It also prevents untested or rights-blocked packages from being labeled copy ready.

`python scripts/test_packages.py` executes only allowlisted test runners. Package manifests cannot inject arbitrary shell commands into CI. The current executable runners are Python and Node; additional runtimes must be added explicitly to the harness before they can produce a runtime-passed package.

GitHub Actions runs both checks on pull requests to `main`.

## Rights and redistribution

Every resource declares one redistribution policy:

| Policy | Meaning |
|---|---|
| `mirror` | RatCodex may redistribute the verified material. |
| `selective` | Only specifically verified files/subsets may be redistributed. |
| `metadata-only` | RatCodex stores metadata and source references, not protected content. |

Unknown, private, non-commercial or permission-restricted material is never silently promoted into a runtime-safe or copy-ready package.

See [`docs/LICENSING.md`](docs/LICENSING.md).

## Source catalog

[`catalog/sources.json`](catalog/sources.json) contains upstream collections and discovery sources. A source entry is not the same thing as a copy-ready package: each downstream resource still needs its own rights and validation evidence.

## Consumers

RatCodex is its own public registry. Consumers should read its generated catalog and manifests directly instead of routing through another Ratware product.

Forge Studio is the primary product integration: it can search/import RatCodex resources while preserving exact versions, hashes, rights and notices. RatLab is intentionally separate; its creative prompt/preset library is not a RatCodex frontend.

See [`docs/INTEGRATIONS.md`](docs/INTEGRATIONS.md).

## Contribution rule

Prefer one small package with proof over twenty untested snippets.

A contribution should add or improve at least one of: provenance, license evidence, normalized implementation, integrity hashes, a reproducible compatibility/runtime test, preview evidence, or AI usage instructions.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Roadmap

- [x] Public registry contract
- [x] License-aware redistribution model
- [x] Agent-compatible package convention
- [x] SHA-256/package integrity validation
- [x] Runtime copy-ready gate
- [x] Safe Python/Node package test harness
- [ ] Godot headless validation runner
- [ ] Ingestion CLI (`ratcodex add <url>`)
- [ ] GitHub source crawler + license evidence cache
- [ ] Generated catalog/index from manifests
- [ ] Read-only HTTP catalog/search API
- [ ] Preview generation for supported resources
- [ ] Forge Studio one-click install/import
- [ ] Contribution bot for rights/test policy
- [ ] Public catalog site

## Non-goals

RatCodex will not republish material merely because it is easy to download, infer file-level rights from a repository badge, execute contributor-supplied shell commands, strip attribution, or label an implementation copy ready without a reproducible test.

It also will not depend on RatLab for search, distribution or API availability.

## License

RatCodex's own code, schemas, documentation and original templates are MIT licensed. External resources keep their upstream licenses and attribution requirements.
