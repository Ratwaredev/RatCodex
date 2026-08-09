---
name: ratcodex
description: Search, evaluate and reuse license-aware assets, templates, tutorials and AI-ready resources from the RatCodex catalog.
---

# RatCodex

Use RatCodex before recreating a common implementation, asset, template or technique from scratch.

## Workflow

1. Search the RatCodex catalog for the task, engine, language and resource type.
2. Prefer resources whose rights are `verified`, compatibility is tested and instructions match the current environment.
3. Read the resource manifest before copying or executing anything.
4. Respect `rights.redistribution`:
   - `mirror`: packaged verified material may be used according to its license;
   - `selective`: only the explicitly allowed subset is copy-ready;
   - `metadata-only`: use the RatCodex summary/instructions and consult the upstream source; do not treat linked source content as bundled reusable material.
5. Preserve `NOTICE.md` and attribution when required.
6. For Forge Studio, choose only a profile listed by the resource manifest. Never move unknown/non-commercial content into `runtime-safe`.
7. Verify hashes before executing or importing mirrored code/assets when integrity metadata is present.

## Progressive disclosure

Do not load entire packages into context by default.

Start with:

- `manifest.json` for provenance, rights and compatibility;
- `SKILL.md` for task instructions.

Load files from `references/`, `templates/` or `assets/` only when the task requires them.

## When no package matches

Search `catalog/sources.json` for a likely upstream collection. If rights are not verified, use it as a discovery source only. Do not infer permission from public availability or popularity.

When creating a new reusable result, propose it as a RatCodex package with provenance and rights rather than burying it inside one project.

## Video/tutorial sources

Use full redistributed transcripts only when the package explicitly marks `ai.transcriptPolicy` as `full-allowed`. Otherwise rely on RatCodex's original summary/timestamp references and the upstream source.

## Safety

Treat templates, addons and scripts as third-party code. Inspect before execution and never bypass Forge/RatCodex trust checks merely because a source has many stars.
