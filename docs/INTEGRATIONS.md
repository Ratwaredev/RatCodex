# Forge Studio and RatLab integration contract

RatCodex is the canonical **public upstream registry**. Forge Studio and RatLab are consumers with different responsibilities.

## Stable contract

Consumers should depend on generated JSON, not scrape the README or repository tree.

Initial files:

- `catalog/sources.json` — upstream discovery sources;
- `catalog/index.json` — generated package index (next milestone);
- `schemas/resource.schema.json` — resource contract.

Future HTTP surfaces may proxy these files, but they must preserve resource IDs and schema semantics.

## Forge Studio

Forge already has a local Bible and export profiles. RatCodex should plug into that rather than create another parallel library.

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

Avoid generic AI cards or a separate chatbot UI. The agent can use the same package data invisibly.

### Import flow

```text
Search RatCodex
  → fetch manifest
  → validate schema
  → verify allowed Forge profile
  → show preview/source/license
  → download verified files
  → verify SHA-256
  → import as versioned Bible resource
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
- preserve source structure where runtime dependencies require it.

`private-full`
- may combine RatCodex metadata with user-held/local media;
- local derived transcripts/previews remain private unless their rights are independently verified;
- never contribute private material back automatically.

### Contribution back

A future **Contribute to RatCodex** action should create a branch/PR containing manifests and explicitly selected files. Never silently upload a user's Bible.

## RatLab

RatLab owns discovery/search/community UX, not the canonical resource payload.

Recommended mapping:

- **BIBLE** → assets, templates, tutorials, documents and collections;
- **SKILLS** → AI-native packages with `SKILL.md`;
- **STUDIO** → opens/install selected resource in Forge Studio;
- **API** → cached/search-optimized projection of RatCodex catalog.

### API shape

RatLab can expose a projection such as:

```http
GET /api/catalog.json
GET /api/catalog/search?q=fire+shader&engine=godot
GET /api/catalog/:id
```

Responses should include the canonical RatCodex resource ID and source commit/version so consumers can detect stale caches.

### Search ranking

Do not rank only by upstream stars. Suggested signals:

1. exact task/engine match;
2. rights verified;
3. compatibility tested;
4. curated quality;
5. recency/maintained status;
6. upstream/community popularity.

### Write path

Community additions should become pull requests to RatCodex. RatLab can provide the form/review UI, but the Git history in this public repository remains the audit trail.

## Versioning

RatCodex resources should use immutable content versions. Forge Studio records the exact imported version/hash. RatLab may show newer versions without mutating existing installs.

Breaking schema changes require a new `schemaVersion`; consumers must reject unknown breaking versions rather than guessing.
