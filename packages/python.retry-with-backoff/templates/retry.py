from __future__ import annotations

import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    fn: Callable[P, R],
    *args: P.args,
    attempts: int = 3,
    initial_delay: float = 0.1,
    multiplier: float = 2.0,
    max_delay: float = 5.0,
    retry_on: tuple[type[BaseException], ...] = (Exception,),
    sleeper: Callable[[float], None] = time.sleep,
    **kwargs: P.kwargs,
) -> R:
    """Call fn until it succeeds or the allowed attempts are exhausted."""
    if attempts < 1:
        raise ValueError("attempts must be >= 1")
    if initial_delay < 0 or max_delay < 0:
        raise ValueError("delays must be >= 0")
    if multiplier < 1:
        raise ValueError("multiplier must be >= 1")

    delay = min(initial_delay, max_delay)
    for attempt in range(1, attempts + 1):
        try:
            return fn(*args, **kwargs)
        except retry_on:
            if attempt == attempts:
                raise
            sleeper(delay)
            delay = min(delay * multiplier, max_delay)

    raise AssertionError("unreachable")
