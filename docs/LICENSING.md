# Licensing and provenance policy

RatCodex is useful only if an AI can distinguish **available** from **reusable**.

Public access is not redistribution permission. Every source and package must keep enough evidence to explain why RatCodex is allowed to index, copy, transform or redistribute it.

## Redistribution classes

### `mirror`

Use only when the verified license or explicit permission allows RatCodex to redistribute the material in the intended form.

Examples: MIT code, Apache-2.0 code, CC0 assets, CC-BY material with required attribution preserved.

### `selective`

Use when an upstream source contains materials under different terms, or only a known subset is safe to redistribute.

The manifest must identify the allowed subset. A repository-level SPDX value is not sufficient when bundled art, audio, fonts, models, datasets or third-party files have separate terms.

### `metadata-only`

RatCodex may store facts about the resource, a source URL, tags, compatibility data, original analysis and non-infringing summaries. It must not republish the protected source material.

Use this when rights are unknown, permission is required, the source is merely an index of third-party material, or the license blocks the intended redistribution.

## Forge export mapping

RatCodex deliberately preserves Forge Studio's three-profile model.

| RatCodex state | `ai-portable` | `runtime-safe` | `private-full` |
|---|---:|---:|---:|
| verified permissive / commercial-safe | yes | yes | yes |
| verified non-commercial | metadata/instructions only | no | local/user-held only |
| unknown rights | metadata only | no | local/user-held only |
| permission-required | metadata only | no | only after the user supplies lawful local material |

`private-full` is not a loophole for RatCodex to publish protected content. It describes local Forge behavior for material the user already has the right to use.

## YouTube and video tutorials

A public RatCodex package may contain a full transcript only when redistribution is supported by one of the following:

- the video is explicitly released under a compatible Creative Commons license;
- the material is public domain;
- the creator has granted explicit permission that covers the intended redistribution;
- another clearly documented legal basis applies and has been reviewed.

For ordinary videos without such permission, RatCodex stores:

- source URL and creator;
- title and public metadata;
- original RatCodex summary;
- timestamped concepts/chapters where appropriate;
- AI instructions that tell the agent when to consult the original source.

It does **not** publish a scraped verbatim transcript.

Forge Studio may support local transcription of user-provided/lawfully held media inside `private-full`; those transcripts must not be pushed into RatCodex automatically.

## Attribution

Each normalized package should generate a `NOTICE.md` containing, when applicable:

- upstream project/resource name;
- author/organization;
- original source;
- exact license identifier/text reference;
- required attribution wording;
- modifications made by RatCodex contributors;
- retrieval and verification timestamps.

Attribution must survive export into Forge Studio and RatLab.

## Evidence

`rights.evidenceUrl` or `rights.evidencePath` must point to the material used to make the rights decision. `rights.verifiedAt` records when it was checked.

If evidence becomes unavailable or contradictory, the package falls back to `metadata-only` until reviewed.

## Mixed repositories

Mixed licensing is normal. Treat files independently when needed.

For example, an upstream Godot demo may put scripts/scenes/shaders under MIT while textures/models are under a non-commercial Creative Commons license. RatCodex can redistribute the MIT subset while blocking the art from `runtime-safe`.

## Contribution rule

When in doubt, do not mirror. A useful metadata-only entry is better than an illegally convenient archive.
