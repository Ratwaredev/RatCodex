from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def write_json_atomic(path: str | os.PathLike[str], value: Any, *, indent: int | None = 2) -> None:
    """Serialize JSON and atomically replace the destination on the same filesystem."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(value, ensure_ascii=False, indent=indent, sort_keys=True) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, target)
    except BaseException:
        try:
            temp_path.unlink(missing_ok=True)
        finally:
            raise
