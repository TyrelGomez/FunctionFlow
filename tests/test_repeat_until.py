import asyncio
import unittest

from FunctionFlow import repeat_until


class RepeatUntilTests(unittest.TestCase):
    def test_accepts_a_zero_argument_condition(self):
        calls = []

        @repeat_until(lambda: len(calls) == 3)
        def work():
            calls.append("called")
            return False

        self.assertFalse(work())
        self.assertEqual(calls, ["called", "called", "called"])

    def test_caught_exception_cannot_satisfy_condition(self):
        attempts = 0

        @repeat_until(lambda result: result is None, max_attempts=2, catch_exceptions=(ValueError,))
        def work():
            nonlocal attempts
            attempts += 1
            raise ValueError("retry")

        self.assertIsNone(work())
        self.assertEqual(attempts, 2)

    def test_async_function_retries_until_its_result_matches(self):
        attempts = 0

        @repeat_until(lambda result: result == 2, max_attempts=2)
        async def work():
            nonlocal attempts
            attempts += 1
            return attempts

        self.assertEqual(asyncio.run(work()), 2)

    def test_rejects_invalid_attempt_limit(self):
        with self.assertRaises(ValueError):
            repeat_until(max_attempts=0)
