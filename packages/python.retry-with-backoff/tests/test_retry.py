from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).parents[1] / "templates" / "retry.py"
spec = importlib.util.spec_from_file_location("retry_template", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
retry = module.retry


class RetryTests(unittest.TestCase):
    def test_returns_first_success(self):
        self.assertEqual(retry(lambda: 7), 7)

    def test_retries_with_capped_backoff(self):
        calls = 0
        sleeps: list[float] = []

        def flaky():
            nonlocal calls
            calls += 1
            if calls < 4:
                raise RuntimeError("temporary")
            return "ok"

        result = retry(flaky, attempts=4, initial_delay=0.25, multiplier=3, max_delay=1, sleeper=sleeps.append)
        self.assertEqual(result, "ok")
        self.assertEqual(calls, 4)
        self.assertEqual(sleeps, [0.25, 0.75, 1])

    def test_does_not_retry_unlisted_exception(self):
        calls = 0

        def fail():
            nonlocal calls
            calls += 1
            raise ValueError("bad input")

        with self.assertRaises(ValueError):
            retry(fail, attempts=3, retry_on=(RuntimeError,), sleeper=lambda _: None)
        self.assertEqual(calls, 1)

    def test_rejects_invalid_attempts(self):
        with self.assertRaises(ValueError):
            retry(lambda: None, attempts=0)


if __name__ == "__main__":
    unittest.main()
