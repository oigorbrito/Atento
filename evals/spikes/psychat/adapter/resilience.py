from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry_with_timeout_boundary(
    operation: Callable[[], T],
    *,
    attempts: int = 2,
    retryable: tuple[type[Exception], ...] = (TimeoutError,),
) -> T:
    """Retry policy boundary.

    The provider/donor call itself owns the concrete timeout parameter. This
    wrapper owns retry semantics so they are not hidden inside donor code.
    """
    if attempts < 1:
        raise ValueError("attempts must be >= 1")
    last: Exception | None = None
    for _ in range(attempts):
        try:
            return operation()
        except retryable as exc:
            last = exc
    assert last is not None
    raise last
