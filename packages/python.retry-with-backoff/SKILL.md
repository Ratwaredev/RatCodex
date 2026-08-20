# Python retry with bounded exponential backoff

Use this package when a synchronous Python operation may fail transiently and retrying is safe.

## Install

Copy `templates/retry.py` into the project. It has no third-party dependencies and targets Python 3.10+.

## Use

Call `retry(fn, ...)` and explicitly narrow `retry_on` when possible. Do not retry validation errors, authentication failures, or non-idempotent operations unless the caller can prove retry safety.

The helper validates its retry configuration, caps exponential delay, re-raises the final exception unchanged, and accepts an injectable sleeper for deterministic tests.

## Validation

`tests/test_retry.py` exercises immediate success, capped backoff, exception filtering, and invalid configuration. RatCodex CI reruns it before this package may remain `copyReady`.
