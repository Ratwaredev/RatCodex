from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "packages"


def safe_relative(value: str) -> bool:
    candidate = Path(value)
    return bool(value) and not candidate.is_absolute() and ".." not in candidate.parts


def run_test(package_dir: Path, runner: str, test_path: str) -> subprocess.CompletedProcess[str]:
    path = package_dir / test_path
    if runner == "python":
        cmd = [sys.executable, str(path)]
    elif runner == "node":
        node = shutil.which("node")
        if not node:
            raise RuntimeError("node runner requested but node is unavailable")
        cmd = [node, "--test", str(path)]
    else:
        raise RuntimeError(f"runner {runner!r} is not executable by this CI harness")
    return subprocess.run(cmd, cwd=package_dir, text=True, capture_output=True, timeout=60)


def main() -> int:
    failures: list[dict] = []
    executed = 0
    passed_packages = 0

    for manifest_path in sorted(PACKAGES.glob("*/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validation = manifest.get("validation", {})
        if validation.get("status") != "passed":
            continue

        runner = validation.get("runner")
        if runner not in {"python", "node"}:
            failures.append({"package": manifest.get("id"), "error": f"unsupported executable runner: {runner}"})
            continue

        package_ok = True
        for test_path in validation.get("tests", []):
            if not safe_relative(test_path) or not (manifest_path.parent / test_path).is_file():
                failures.append({"package": manifest.get("id"), "test": test_path, "error": "missing or unsafe test path"})
                package_ok = False
                continue
            executed += 1
            try:
                result = run_test(manifest_path.parent, runner, test_path)
            except Exception as exc:
                failures.append({"package": manifest.get("id"), "test": test_path, "error": str(exc)})
                package_ok = False
                continue
            if result.returncode != 0:
                failures.append({
                    "package": manifest.get("id"),
                    "test": test_path,
                    "returncode": result.returncode,
                    "stdout": result.stdout[-4000:],
                    "stderr": result.stderr[-4000:],
                })
                package_ok = False
        if package_ok:
            passed_packages += 1

    payload = {
        "ok": not failures,
        "runtimeTestedPackages": passed_packages,
        "testFilesExecuted": executed,
        "failures": failures,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
