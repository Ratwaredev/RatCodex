# Python atomic JSON write

Use this package when a JSON file must never be left partially written after a process interruption or write failure.

## Install

Copy `templates/atomic_json.py`. It uses only the Python standard library and targets Python 3.10+.

## Behavior

`write_json_atomic(path, value)` serializes before touching the destination, writes to a temporary file in the same directory, flushes and `fsync`s it, then replaces the target with `os.replace`.

This protects existing content from JSON serialization failures and avoids readers observing a half-written file. It does not provide multi-process locking or durability guarantees for the containing directory on every filesystem.

## Validation

`tests/test_atomic_json.py` verifies valid UTF-8 JSON output, preservation of an existing file after serialization failure, and temporary-file cleanup. RatCodex CI reruns it before this package may remain `copyReady`.
