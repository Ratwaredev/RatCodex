# RatCodex

> An open, license-aware registry of reusable assets, templates, tutorials, documents and AI-ready skills.

RatCodex turns scattered development knowledge into **portable, machine-readable packages** that both humans and AI agents can actually use.

It is not a link dump and it is not a blind mirror of the internet. Every entry carries provenance, license evidence, redistribution rules, compatibility metadata and an AI entry point.

## Why this exists

Useful knowledge is fragmented across GitHub repositories, documentation sites, demo projects, asset libraries, videos and articles. Humans can often piece those sources together; agents waste context rediscovering them and frequently cannot tell what is safe to copy, redistribute or execute.

RatCodex normalizes that material into one catalog:

- **Assets** — shaders, VFX, models, audio, UI, textures, scenes and reusable code.
- **Templates** — complete or partial starter projects and proven implementations.
- **Tutorials** — structured guides with source references and AI-readable steps.
- **Skills** — packages following the Agent Skills `SKILL.md` convention when possible.
- **Documents** — references normalized for retrieval without stripping attribution.
- **Transcripts** — only when redistribution is explicitly allowed; otherwise RatCodex stores timestamped summaries and source references.
- **Collections** — curated upstream indexes that RatCodex can discover and continuously verify.

## Core rule: provenance before convenience

A resource is never considered reusable just because it is publicly accessible.

Every package must declare one redistribution policy:

| Policy | Meaning |
|---|---|
| `mirror` | RatCodex may redistribute the verified material. |
| `selective` | Only specifically verified files/subsets may be redistributed. |
| `metadata-only` | RatCodex stores metadata, instructions and source links, not the protected content. |

Unknown, private, non-commercial or permission-restricted content is **not** silently exported into public/runtime-safe bundles.

See [`docs/LICENSING.md`](docs/LICENSING.md).

## AI-native package format

RatCodex is compatible with the Agent Skills idea instead of inventing a closed prompt format. A normalized package can look like this:

```text
packages/<id>/
├── manifest.json          # provenance, rights, compatibility, integrity
├── SKILL.md               # compact instructions for an agent
├── references/            # redistributable reference material
├── assets/                # verified reusable assets
├── templates/             # copy-ready project fragments
└── NOTICE.md              # attribution + upstream notices
```

`SKILL.md` is the progressive-disclosure entry point. Large references and binaries stay outside the initial context and are loaded only when needed.

## Catalog

The first verified upstream sources live in [`catalog/sources.json`](catalog/sources.json). They intentionally mix three classes:

1. redistributable sources that can seed actual packages;
2. mixed-license sources that require file-level selection;
3. discovery indexes where RatCodex only catalogs downstream resources until their individual rights are verified.

The canonical resource contract is [`schemas/resource.schema.json`](schemas/resource.schema.json).

## Forge Studio integration

RatCodex extends the existing Forge Bible model instead of replacing it.

Forge Studio can consume the public catalog and map resources into its current export profiles:

- `ai-portable`: AI instructions, manifests and redistributable references;
- `runtime-safe`: executable/copy-ready material whose rights permit that use;
- `private-full`: user-owned/local material that must never be republished automatically.

A user should be able to search RatCodex from Forge, inspect a real preview, read the source/license, then **Add to Bible** or install a verified template without losing provenance.

## RatLab integration

RatLab consumes the same catalog for its **BIBLE** and **SKILLS** surfaces. RatCodex remains the canonical public data source; RatLab can expose a cached/searchable API without forking the data model.

The integration contract is documented in [`docs/INTEGRATIONS.md`](docs/INTEGRATIONS.md).

## Contribution model

The path to scale is community contribution plus automated verification, not committing random files by hand.

A contribution should be one of:

- a new source manifest;
- a normalized package;
- a license/provenance correction;
- a compatibility test;
- an ingestion adapter;
- a better AI guide for an existing resource.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## North star

The repo should earn that by becoming the place where an agent can answer: _“Do we already have a legal, tested implementation of this?”_ and immediately retrieve one.

The growth loop is:

```text
Discover → Verify rights → Normalize → Test → Index → Install in Forge/RatLab → Improve → Contribute back
```

## Roadmap

- [x] Public registry contract
- [x] License-aware redistribution model
- [x] Initial verified source catalog
- [x] Forge Studio / RatLab integration contract
- [x] Agent-compatible package convention
- [ ] Ingestion CLI (`ratcodex add <url>`)
- [ ] GitHub source crawler + license evidence cache
- [ ] Package validator + SHA-256 integrity checks
- [ ] Generated static catalog/index
- [ ] RatLab searchable API
- [ ] Forge Studio one-click install/import
- [ ] Preview generation for supported assets/templates
- [ ] Contribution bot that rejects unknown rights
- [ ] Public catalog site

## Non-goals

RatCodex will not:

- scrape and republish copyrighted tutorials because they are easy to download;
- publish full YouTube transcripts unless the license or creator permission allows redistribution;
- treat a repository-level license as proof that every bundled art/audio asset has the same license;
- execute untrusted templates automatically;
- remove upstream attribution;
- become a multi-gigabyte graveyard of duplicated archives.

## License

RatCodex's own code, schemas and documentation are MIT licensed. Every external resource keeps its own upstream license and attribution requirements. A RatCodex package may therefore contain stricter terms than this repository itself.
