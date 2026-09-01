"""Helpers for chaining function calls."""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable


def run_list(next_function: Callable[..., Any]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Run ``next_function`` after the decorated function completes.

    The original function's return value is preserved.  The queued function is
    called with the same positional and keyword arguments as the original call.
    Both synchronous and asynchronous functions are supported.
    """
    if not callable(next_function):
        raise TypeError("next_function must be callable")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                result = await func(*args, **kwargs)
                queued_result = next_function(*args, **kwargs)
                if inspect.isawaitable(queued_result):
                    await queued_result
                return result

            return async_wrapper

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            queued_result = next_function(*args, **kwargs)
            if inspect.isawaitable(queued_result):
                raise TypeError("an async next_function requires an async decorated function")
            return result

        return wrapper

    return decorator


# Backwards-compatible public name matching this module's original name.
runList = run_list
