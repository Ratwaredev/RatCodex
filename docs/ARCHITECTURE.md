# Architecture

RatCodex separates **discovery**, **rights verification**, **normalization** and **distribution** so the project can scale without turning into an unsafe mirror.

## Layers

```text
Upstream sources
   │
   ▼
Discovery adapters ── GitHub / web / video / docs
   │
   ▼
Rights verifier ───── license evidence + redistribution policy
   │
   ▼
Normalizer ────────── manifest.json + SKILL.md + NOTICE.md
   │
   ├──► metadata-only catalog
   ├──► ai-portable package
   └──► runtime-safe package
   │
   ▼
Static catalog/index
   │
   ├──► Forge Studio
   ├──► RatLab BIBLE / SKILLS
   └──► third-party agents/tools
```

## Source registry

`catalog/sources.json` is the discovery layer. It describes upstream collections and their current rights assessment. A source is not automatically a package.

## Resource manifests

Every installable/AI-consumable item validates against `schemas/resource.schema.json`.

A resource ID is stable even if an upstream URL changes. Upstream identity, ref/path and integrity hashes are stored separately.

## Packages

Normalized packages live under `packages/<id>/` and should prefer the Agent Skills progressive-disclosure structure:

```text
manifest.json
SKILL.md
references/
assets/
templates/
NOTICE.md
```

`SKILL.md` must be short enough to load as instructions. Large source material belongs in `references/` and should be referenced by task, not dumped into every agent context.

## Ingestion pipeline

Planned CLI:

```bash
ratcodex add <url>
ratcodex inspect <source-id>
ratcodex verify <package-id>
ratcodex build
ratcodex audit
```

`add` must not immediately mirror content. It creates a candidate and runs adapters in this order:

1. identify source type;
2. capture immutable upstream identity/ref when possible;
3. detect license files and per-file exceptions;
4. classify `mirror`, `selective` or `metadata-only`;
5. extract only allowed material;
6. generate AI guidance and NOTICE;
7. hash mirrored files;
8. run compatibility/security checks;
9. validate schema;
10. publish generated index only if all mandatory checks pass.

## Trust states

Suggested future trust levels:

- `discovered` — useful upstream candidate, not reviewed;
- `rights-verified` — evidence checked;
- `normalized` — package format complete;
- `tested` — compatibility test passed;
- `curated` — human-reviewed high-quality entry.

Trust is orthogonal to popularity. Stars do not make an asset safe or good.

## Security

Templates and scripts are supply-chain inputs. RatCodex should eventually add:

- immutable commit/tag pinning for mirrored GitHub material;
- SHA-256 hashes for every redistributed file;
- archive traversal/symlink guards;
- executable/script detection;
- dependency manifest extraction;
- secret scanning;
- generated SBOM where meaningful;
- sandboxed preview/build checks;
- no auto-execution on catalog import.

Forge Studio may preview or install a package only after showing source, rights and trust state. A package update must be a new version, not a silent mutation.

## Generated catalog

The repository should eventually produce immutable versioned releases plus a small current index:

```text
catalog/index.json
catalog/sources.json
catalog/packages.json
releases/<version>/catalog.json
```

RatLab may cache/index the catalog for search, but RatCodex remains canonical for public provenance and contribution history.

## Storage strategy

Do not store every upstream archive in Git. Prefer:

- small redistributable text/assets directly in packages;
- generated release artifacts for larger verified bundles;
- metadata-only references for material that cannot or should not be mirrored;
- optional external object storage later if legitimate mirrored binaries outgrow GitHub Releases.

This keeps clone size small and makes the catalog star/fork friendly.
