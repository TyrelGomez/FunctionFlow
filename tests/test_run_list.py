import asyncio
import unittest

from FunctionFlow import run_list


class RunListTests(unittest.TestCase):
    def test_queued_function_runs_after_and_result_is_preserved(self):
        calls = []

        def after(value):
            calls.append(("after", value))

        @run_list(after)
        def first(value):
            calls.append(("first", value))
            return value * 2

        self.assertEqual(first(3), 6)
        self.assertEqual(calls, [("first", 3), ("after", 3)])

    def test_async_functions_are_supported(self):
        calls = []

        async def after(value):
            calls.append(("after", value))

        @run_list(after)
        async def first(value):
            calls.append(("first", value))
            return value

        self.assertEqual(asyncio.run(first("ok")), "ok")
        self.assertEqual(calls, [("first", "ok"), ("after", "ok")])
