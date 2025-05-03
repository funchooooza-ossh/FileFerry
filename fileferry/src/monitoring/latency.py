import functools
import time
from collections.abc import Awaitable, Callable
from typing import ParamSpec, TypeVar

from prometheus_client import Histogram

P = ParamSpec("P")
T = TypeVar("T")


def record_latency(
    histogram: Histogram,
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            start = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                histogram.observe(time.perf_counter() - start)

        return wrapper

    return decorator
