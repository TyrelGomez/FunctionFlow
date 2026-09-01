from __future__ import annotations

import asyncio
import functools
import inspect
import math
import time
from numbers import Real
from typing import Any, Callable, Optional, Sequence


def _accepts_result(condition: Callable[..., bool]) -> bool:
    """Return whether a predicate can be called with one positional argument."""
    try:
        signature = inspect.signature(condition)
    except (TypeError, ValueError):
        return True

    try:
        signature.bind(object())
    except TypeError:
        return False
    return True


def repeat_until(
    condition: Optional[Callable[..., bool]] = None,
    *,
    max_attempts: Optional[int] = None,
    delay: float = 0.0,
    catch_exceptions: Optional[Sequence[type[Exception]]] = None,
    raise_on_failure: bool = False,
):
    """Repeat a function until its predicate succeeds.

    ``condition`` may accept the function result, or be a zero-argument
    predicate for state-based checks. If omitted, the result's truthiness is
    used. Caught exceptions consume an attempt but never satisfy the condition.
    """
    if condition is None:
        condition = bool
    elif not callable(condition):
        raise TypeError("condition must be callable")

    if max_attempts is not None and (
        isinstance(max_attempts, bool) or not isinstance(max_attempts, int) or max_attempts < 1
    ):
        raise ValueError("max_attempts must be a positive integer or None")

    if isinstance(delay, bool) or not isinstance(delay, Real) or not math.isfinite(delay) or delay < 0:
        raise ValueError("delay must be a finite, non-negative number")

    try:
        retry_exceptions = tuple(catch_exceptions or ())
    except TypeError as error:
        raise TypeError("catch_exceptions must be a sequence of exception types") from error
    if not all(isinstance(error_type, type) and issubclass(error_type, Exception)
               for error_type in retry_exceptions):
        raise TypeError("catch_exceptions must contain Exception subclasses")

    condition_accepts_result = _accepts_result(condition)

    def condition_is_met(result: Any) -> bool:
        return bool(condition(result) if condition_accepts_result else condition())

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        is_coro = inspect.iscoroutinefunction(func)

        if is_coro:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                attempts = 0
                last_result = None
                while True:
                    attempts += 1
                    try:
                        last_result = await func(*args, **kwargs)
                    except retry_exceptions:
                        last_result = None
                    else:
                        if condition_is_met(last_result):
                            return last_result

                    if max_attempts is not None and attempts >= max_attempts:
                        if raise_on_failure:
                            raise RuntimeError("repeat_until: max_attempts exhausted")
                        return last_result

                    if delay:
                        await asyncio.sleep(delay)

            return async_wrapper

        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                attempts = 0
                last_result = None
                while True:
                    attempts += 1
                    try:
                        last_result = func(*args, **kwargs)
                    except retry_exceptions:
                        last_result = None
                    else:
                        if condition_is_met(last_result):
                            return last_result

                    if max_attempts is not None and attempts >= max_attempts:
                        if raise_on_failure:
                            raise RuntimeError("repeat_until: max_attempts exhausted")
                        return last_result

                    if delay:
                        time.sleep(delay)

            return sync_wrapper

    return decorator
