# Visual previews

RatCodex resources may expose an optional `preview` object. It is deliberately additive: the resource ID, install behavior, rights and Forge export profiles do not change when a preview is absent or fails to render.

## One resource, one identity

A preview is not a second asset library. It belongs to the same canonical resource manifest consumed by RatCodex, RatLab and Forge Studio.

```text
RatCodex resource
├── manifest + rights + compatibility
├── SKILL.md
├── installable/reference payload
└── preview (optional)
    ├── static image/gallery
    ├── video
    ├── HTML/live web entrypoint
    ├── Godot scene
    ├── 3D model
    └── audio
```

Consumers that do not understand `preview` can ignore it and keep working exactly as before.

## Preview modes

### `image` / `gallery`

Best for UI templates, screenshots, textures, static assets and fallback posters. `hero` references a package-relative file; `heroUrl` references a verified upstream visual without mirroring it.

### `video`

Best for animation, VFX, interaction and motion-heavy templates. Public packages may only redistribute video when rights allow it. Otherwise use an upstream URL or a locally generated Forge preview that is not published.

### `html`

For web templates that can be rendered safely. Forge may launch the template in its existing isolated preview flow; RatLab can use a deployed/static preview or generated screenshot rather than executing untrusted third-party code in the catalog page.

### `godot-scene`

For spells, VFX, scenes and reusable Godot mechanics. `entrypoint` identifies the source scene and `runtimeEntrypoint` may identify the runtime-safe scene that Forge already knows how to launch.

Forge Studio is the authoritative interactive renderer for this mode. RatLab should normally show a poster/video/storyboard and offer **Open in Forge** for the live version.

### `model` / `audio`

Use Forge's existing GLB/GLTF and media preview capabilities when compatible. RatLab can render supported browser-safe formats and fall back to static metadata otherwise.

## Providers

- `package` — preview material is physically inside the RatCodex package and follows its redistribution rules.
- `upstream` — preview remains at the upstream source. RatCodex stores only the reference.
- `forge-local` — preview or derived media exists only in the user's local Forge data. Never publish automatically.
- `generated` — derived preview produced from redistributable source material. It must preserve source/rights provenance.

## Spell/VFX rule

Existing Forge VFX/spell scenes remain the source of truth. RatCodex must not create a duplicate scene solely to make a preview.

For a spell package:

```json
{
  "preview": {
    "mode": "godot-scene",
    "provider": "forge-local",
    "entrypoint": "spells/08_tornado/scene.tscn",
    "runtimeEntrypoint": "godot/.../spell_08_tornado.tscn",
    "interactive": true,
    "aspectRatio": "16:9",
    "fallback": "placeholder"
  }
}
```

A validated spell can be previewed and installed. An unvalidated spell may still be visually inspected, but its validation status must remain visible and it must never be promoted to approved merely because the preview renders.

## Template rule

A template preview answers “what does this become?” before installation. Prefer, in order:

1. live isolated preview when already supported and safe;
2. generated screenshot/video from a deterministic build;
3. verified upstream screenshot/demo;
4. placeholder + source link.

Preview failure never changes the template's install contract. Download/import routes continue using the same resource/version/hash.

## RatLab behavior

RatLab reads the canonical preview descriptor and can display:

- hero visual directly in search results;
- gallery/video in the resource detail;
- validation/license badges over the visual rather than hiding them;
- **Open in Forge** when an interactive local renderer is required.

RatLab must not invent a second preview ID. Cache keys should include the RatCodex resource ID and version/hash.

## Forge Studio behavior

Forge maps preview modes onto capabilities it already has:

- image/video/audio/text → existing media preview;
- GLB/GLTF → existing 3D viewer;
- web template → existing project preview;
- Godot spell/VFX → existing executable scene/runtime scene;
- unsupported native formats → local application fallback.

The current Bible/import/export paths remain unchanged. Preview is an inspection layer before the existing **Add to Bible / Use in project** action.

## Rights and private media

A preview never widens the rights of a package. `metadata-only` stays metadata-only; non-commercial material does not become `runtime-safe` because it has a screenshot.

Local captures generated from user-held/private material remain `forge-local` unless their redistribution rights are independently verified.
