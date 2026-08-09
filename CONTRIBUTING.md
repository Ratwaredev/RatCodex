# Contributing to RatCodex

RatCodex accepts useful resources only when provenance and rights are explicit.

## Best contributions

1. **Source** — add an upstream collection to `catalog/sources.json`.
2. **Package** — normalize one concrete resource under `packages/<id>/`.
3. **Adapter** — teach the future ingestion CLI how to understand a source type.
4. **Verification** — improve license evidence, compatibility or integrity metadata.
5. **Guide** — improve a package's `SKILL.md` so an agent can use it without loading unnecessary context.

## Package checklist

A package PR should include:

```text
packages/<id>/manifest.json
packages/<id>/SKILL.md
packages/<id>/NOTICE.md
```

and only the `references/`, `assets/` or `templates/` material whose redistribution is justified by the manifest.

Before requesting review:

- use a stable lowercase resource ID;
- record the original source and author/organization;
- pin a Git commit/tag when possible;
- record license evidence;
- choose `mirror`, `selective` or `metadata-only` conservatively;
- preserve required attribution;
- do not upload secrets/build outputs/cache directories;
- do not upload a full YouTube transcript unless redistribution is explicitly allowed;
- do not assume linked content inherits the license of an awesome-list/index;
- do not assume all files in a repository inherit its root license;
- hash mirrored files once the validator is available;
- explain how an AI should use the resource in `SKILL.md`.

## `SKILL.md`

Keep the entry point practical and compact. It should tell an agent:

- what problem the package solves;
- when to use it;
- compatibility constraints;
- which files are copy-ready versus reference-only;
- how to install/adapt the resource;
- what not to do;
- where to load deeper references only when needed.

Do not paste an entire upstream tutorial into `SKILL.md`.

## Rights review

If the license is unclear, submit the package as `metadata-only` and open a follow-up issue. That is accepted behavior, not a failed contribution.

If an upstream source has mixed rights, list the safe subset instead of downgrading the whole source or mirroring it all.

## Security review

Executable templates, addons and scripts are code dependencies. Contributors should never ask reviewers to run unknown binaries. Future CI will inspect archives, paths, secrets, dependencies and executable content before a package can become `tested` or `curated`.

## Quality

RatCodex is curated, not exhaustive-by-default. A resource should solve a real task, demonstrate a reusable technique, provide a high-quality template/asset, or improve AI access to difficult knowledge.

Duplicate low-quality resources should be consolidated rather than multiplied.
