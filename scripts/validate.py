from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
PACKAGES = ROOT / "packages"

PREVIEW_MODES = {"image", "gallery", "video", "html", "godot-scene", "model", "audio", "none"}
PREVIEW_PROVIDERS = {"package", "upstream", "forge-local", "generated"}


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"{path.relative_to(ROOT)}: invalid JSON: {exc}") from exc


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_relative(value: str) -> bool:
    candidate = Path(value)
    return bool(value) and not candidate.is_absolute() and ".." not in candidate.parts


def is_runtime_blocked(manifest: dict) -> bool:
    rights = manifest.get("rights", {})
    if rights.get("status") != "verified":
        return True
    license_text = str(rights.get("license") or "").lower()
    blocked = (
        "unknown",
        "private",
        "noncommercial",
        "non-commercial",
        "cc-by-nc",
        "cc by-nc",
        "permission-required",
    )
    return any(token in license_text for token in blocked)


def validate_preview(package_dir: Path, preview: dict, rel: Path, errors: list[str]) -> None:
    mode = preview.get("mode")
    provider = preview.get("provider")
    if mode not in PREVIEW_MODES:
        errors.append(f"{rel}: invalid preview.mode={mode!r}")
    if provider not in PREVIEW_PROVIDERS:
        errors.append(f"{rel}: invalid preview.provider={provider!r}")

    if mode == "godot-scene" and not (preview.get("entrypoint") or preview.get("runtimeEntrypoint")):
        errors.append(f"{rel}: godot-scene preview needs entrypoint or runtimeEntrypoint")

    if provider == "upstream" and mode not in {"none", "godot-scene"}:
        if not preview.get("heroUrl") and not preview.get("gallery"):
            errors.append(f"{rel}: upstream visual preview needs heroUrl or gallery")

    if provider not in {"package", "generated"}:
        return

    local_refs: list[str] = []
    for key in ("hero", "entrypoint", "runtimeEntrypoint"):
        value = preview.get(key)
        if value:
            local_refs.append(value)
    for value in preview.get("gallery", []):
        if isinstance(value, str) and "://" not in value:
            local_refs.append(value)

    for value in local_refs:
        if not safe_relative(value):
            errors.append(f"{rel}: unsafe preview path: {value}")
            continue
        if not (package_dir / value).is_file():
            errors.append(f"{rel}: preview file missing: {value}")


def validate_manifest(path: Path, errors: list[str]) -> dict | None:
    try:
        manifest = load_json(path)
    except RuntimeError as exc:
        errors.append(str(exc))
        return None

    rel = path.relative_to(ROOT)
    required = ("schemaVersion", "id", "title", "kind", "source", "rights", "ai")
    for key in required:
        if key not in manifest:
            errors.append(f"{rel}: missing required field {key}")

    if manifest.get("schemaVersion") != "1.0":
        errors.append(f"{rel}: unsupported schemaVersion={manifest.get('schemaVersion')!r}")

    resource_id = manifest.get("id")
    if resource_id and path.parent.name != resource_id:
        errors.append(f"{rel}: directory name must equal resource id {resource_id}")

    rights = manifest.get("rights", {})
    if rights.get("redistribution") not in {"mirror", "selective", "metadata-only"}:
        errors.append(f"{rel}: invalid rights.redistribution")
    if rights.get("status") not in {"verified", "mixed", "unknown", "permission-required"}:
        errors.append(f"{rel}: invalid rights.status")

    source = manifest.get("source", {})
    if not source.get("url") or not source.get("type"):
        errors.append(f"{rel}: source.type and source.url are required")

    ai = manifest.get("ai", {})
    entrypoint = ai.get("entrypoint", "SKILL.md")
    if not (path.parent / entrypoint).is_file():
        errors.append(f"{rel}: missing AI entrypoint {entrypoint}")

    if rights.get("redistribution") == "metadata-only" and ai.get("copyReady"):
        errors.append(f"{rel}: metadata-only resource cannot be copyReady")

    preview = manifest.get("preview")
    if preview is not None:
        if not isinstance(preview, dict):
            errors.append(f"{rel}: preview must be an object")
        else:
            validate_preview(path.parent, preview, rel, errors)

    forge_profiles = manifest.get("forge", {}).get("profiles", [])
    if "runtime-safe" in forge_profiles and is_runtime_blocked(manifest):
        errors.append(f"{rel}: runtime-safe is forbidden by current rights state/license")

    for item in manifest.get("upstream", {}).get("files", []):
        local_rel = item.get("ratcodexPath")
        if not local_rel:
            errors.append(f"{rel}: upstream file missing ratcodexPath")
            continue
        if not safe_relative(local_rel):
            errors.append(f"{rel}: unsafe mirrored file path: {local_rel}")
            continue
        local = path.parent / local_rel
        if not local.is_file():
            errors.append(f"{rel}: mirrored file missing: {local_rel}")
            continue
        expected_bytes = item.get("bytes")
        if expected_bytes is not None and local.stat().st_size != expected_bytes:
            errors.append(
                f"{rel}: {local_rel} bytes={local.stat().st_size}, expected={expected_bytes}"
            )
        expected_hash = item.get("sha256")
        if expected_hash and sha256(local) != expected_hash:
            errors.append(f"{rel}: {local_rel} sha256 mismatch")

    if rights.get("redistribution") in {"mirror", "selective"} and not (path.parent / "NOTICE.md").is_file():
        errors.append(f"{rel}: redistributed package requires NOTICE.md")

    return manifest


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        sources = load_json(CATALOG / "sources.json")
        index = load_json(CATALOG / "index.json")
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    source_rows = sources.get("sources", [])
    source_ids = [item.get("id") for item in source_rows]
    if None in source_ids:
        errors.append("catalog/sources.json: every source needs an id")
    if len(source_ids) != len(set(source_ids)):
        errors.append("catalog/sources.json: duplicate source ids")

    for source in source_rows:
        rights = source.get("rights", {})
        if rights.get("redistribution") not in {"mirror", "selective", "metadata-only"}:
            errors.append(f"source {source.get('id')}: invalid redistribution policy")
        if rights.get("status") in {"unknown", "permission-required"} and rights.get("redistribution") != "metadata-only":
            errors.append(f"source {source.get('id')}: unknown/permission-required source must be metadata-only")
        if not rights.get("evidenceUrl"):
            warnings.append(f"source {source.get('id')}: missing rights evidence URL")

    manifests: dict[str, dict] = {}
    if PACKAGES.exists():
        for manifest_path in sorted(PACKAGES.glob("*/manifest.json")):
            manifest = validate_manifest(manifest_path, errors)
            if manifest and manifest.get("id"):
                rid = manifest["id"]
                if rid in manifests:
                    errors.append(f"duplicate package id: {rid}")
                manifests[rid] = manifest

    indexed = index.get("packages", [])
    indexed_ids = [item.get("id") for item in indexed]
    if len(indexed_ids) != len(set(indexed_ids)):
        errors.append("catalog/index.json: duplicate package ids")

    missing_from_index = sorted(set(manifests) - set(indexed_ids))
    stale_index = sorted(set(indexed_ids) - set(manifests))
    if missing_from_index:
        errors.append(f"catalog/index.json missing packages: {missing_from_index}")
    if stale_index:
        errors.append(f"catalog/index.json references missing packages: {stale_index}")

    stats = index.get("stats", {})
    if stats.get("sources") != len(source_rows):
        errors.append(f"catalog/index.json stats.sources={stats.get('sources')}, expected={len(source_rows)}")
    if stats.get("packages") != len(manifests):
        errors.append(f"catalog/index.json stats.packages={stats.get('packages')}, expected={len(manifests)}")

    visual_count = sum(1 for manifest in manifests.values() if manifest.get("preview", {}).get("mode") not in {None, "none"})
    if stats.get("visualPackages") is not None and stats.get("visualPackages") != visual_count:
        errors.append(f"catalog/index.json stats.visualPackages={stats.get('visualPackages')}, expected={visual_count}")

    for row in indexed:
        rid = row.get("id")
        manifest = manifests.get(rid)
        if not manifest:
            continue
        if row.get("preview") != manifest.get("preview") and row.get("preview") is not None:
            # The compact index may omit notes/capture fields but must preserve the core visual identity.
            indexed_preview = row.get("preview", {})
            canonical_preview = manifest.get("preview", {})
            for key in ("mode", "provider", "hero", "heroUrl", "entrypoint", "runtimeEntrypoint", "interactive", "aspectRatio", "fallback"):
                if key in indexed_preview and indexed_preview.get(key) != canonical_preview.get(key):
                    errors.append(f"catalog/index.json package {rid}: preview.{key} differs from manifest")

    payload = {
        "ok": not errors,
        "sources": len(source_rows),
        "packages": len(manifests),
        "visualPackages": visual_count,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
