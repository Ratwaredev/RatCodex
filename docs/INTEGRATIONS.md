# RatCodex integration contract

RatCodex is the canonical public registry for reusable development resources. Consumers should depend on RatCodex directly rather than routing its catalog through another Ratware product.

## Stable contract

Consumers should depend on generated JSON and package manifests, not scrape the README or repository tree.

Current files:

- `catalog/sources.json` — upstream discovery sources;
- `catalog/index.json` — normalized package index;
- `schemas/resource.schema.json` — resource contract;
- `packages/<id>/manifest.json` — exact package provenance, rights, validation and integrity.

Future HTTP surfaces may project these files, but they must preserve resource IDs, immutable versions/hashes and schema semantics.

## Forge Studio

Forge already has a local resource/Bible model and export profiles. RatCodex should plug into that rather than create another parallel library.

### UX

Add an **Online / RatCodex** source inside the existing Library/Bible surface.

For every result show only decision-relevant information:

- real preview when supported;
- resource type;
- engine/version compatibility;
- source/upstream;
- license + redistribution state;
- trust/test state;
- install/import action.

Avoid a separate chatbot UI. Coding agents can consume the same package metadata invisibly.

### Import flow

```text
Search RatCodex
  → fetch manifest
  → validate schema
  → verify allowed Forge profile
  → show preview/source/license/test state
  → download verified files
  → verify SHA-256
  → import as versioned resource
  → retain NOTICE + upstream identity
```

### Existing export profiles

`ai-portable`
- manifests;
- `SKILL.md`;
- permitted text references;
- metadata-only pointers;
- no restricted binary payloads.

`runtime-safe`
- only files allowed by the verified rights policy;
- block unknown, permission-required and non-commercial material by default;
- require the package's declared runtime/integrity guarantees;
- preserve source structure where runtime dependencies require it.

`private-full`
- may combine RatCodex metadata with user-held/local media;
- local derived transcripts/previews remain private unless their rights are independently verified;
- never contribute private material back automatically.

### Contribution back

A future **Contribute to RatCodex** action should create a branch/PR containing manifests and explicitly selected files. Never silently upload a user's local resource library.

## RatLab boundary

RatLab is intentionally not a RatCodex consumer or distribution layer.

RatLab owns image/video production, characters, generated media and its own source-backed creative prompt/preset library. RatCodex owns reusable development packages and the evidence required to copy/install them safely.

This means:

- RatLab does not expose RatCodex as `BIBLE` or `SKILLS`;
- RatLab's RatAPI does not proxy the RatCodex catalog;
- RatCodex availability does not depend on RatLab;
- shared Ratware branding does not imply a shared data model or backend.

A Ratware product may link to RatCodex as an external product, but integration code should consume RatCodex directly from its canonical catalog/API.

## Future HTTP API

A RatCodex-native read-only API may expose projections such as:

```http
GET /api/catalog
GET /api/catalog/search?q=fire+shader&engine=godot
GET /api/catalog/:id
```

Responses must include the canonical resource ID, source version/ref, rights state, validation state and integrity evidence so clients can reject stale or unsafe data.

### Search ranking

Do not rank only by upstream stars. Suggested signals:

1. exact task/engine match;
2. rights verified;
3. runtime/compatibility tested;
4. curated quality;
5. recency/maintained status;
6. upstream/community popularity.

## Versioning

RatCodex resources should use immutable content versions. Forge Studio records the exact imported version/hash and may show newer versions without mutating existing installs.

Breaking schema changes require a new `schemaVersion`; consumers must reject unknown breaking versions rather than guessing.
