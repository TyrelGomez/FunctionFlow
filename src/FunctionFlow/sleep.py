"""Sleep helper with pause/unpause control.

Provides a `sleep(seconds)` function that counts only while not paused.
Call `pause()` to pause the countdown and `unpause()` to resume it.
"""
from __future__ import annotations

import threading
import time

# Event is set when execution is allowed to progress, cleared when paused.
_running_event = threading.Event()
_running_event.set()


def pause_sleep() -> None:
    """Pause the countdown used by `sleep`.

    Calling `pause()` will suspend all ongoing `sleep()` countdowns until
    `unpause()` is called.
    """
    _running_event.clear()


def unpause() -> None:
    """Resume previously paused `sleep()` countdowns."""
    _running_event.set()


def is_paused() -> bool:
    """Return True if paused, False otherwise."""
    return not _running_event.is_set()


def sleep(seconds: float) -> None:
    """Sleep for `seconds` of active (unpaused) time.

    If `pause()` is called while this function is waiting, the countdown
    is suspended until `unpause()` is called. The function returns only
    after the requested amount of unpaused time has elapsed.
    """
    if seconds <= 0:
        return

    end = time.monotonic() + float(seconds)
    # Use small sleep chunks so we can react quickly to pause/unpause.
    chunk = 0.05
    while True:
        # Wait until we are allowed to run. This will block while paused.
        _running_event.wait()

        remaining = end - time.monotonic()
        if remaining <= 0:
            break

        time.sleep(min(chunk, remaining))
