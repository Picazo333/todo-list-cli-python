"""Extra checks beyond the official test.py contract.

The official suite shares one in-memory list and must be run on its own:

    python3 test.py

Run this file in a separate process:

    python3 -m unittest tests.test_robustness
"""

import csv
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

import app


class CsvRoundTripTest(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self._previous = os.getcwd()
        os.chdir(self._tmpdir.name)
        self.addCleanup(os.chdir, self._previous)
        app.todos.clear()

    def tearDown(self):
        app.todos.clear()

    def _read_like_official_test(self):
        file = open("todos.csv", "r")
        rows = []
        for row in csv.reader(file):
            rows.append(row[0])
        file.close()
        return rows

    def test_comma_and_unicode_roundtrip(self):
        titles = [
            "Buy milk, bread",
            'Say "hi"',
            "Revisar muelle — ñandú",
            "café, azúcar",
        ]
        for title in titles:
            app.add_one_task(title)
        self.assertTrue(app.save_todos())
        self.assertEqual(self._read_like_official_test(), titles)
        app.todos.clear()
        self.assertTrue(app.load_todos())
        self.assertEqual(app.get_todos(), titles)

    def test_plain_lines_from_official_load_fixture(self):
        file = open("todos.csv", "w+")
        file.write("\n".join(["jump", "run", "roll"]))
        file.close()
        app.add_one_task("this should be replaced")
        self.assertTrue(app.load_todos())
        self.assertEqual(app.get_todos(), ["jump", "run", "roll"])

    def test_empty_file_loads_empty_list(self):
        app.add_one_task("temporary")
        file = open("todos.csv", "w")
        file.close()
        self.assertTrue(app.load_todos())
        self.assertEqual(app.get_todos(), [])

    def test_missing_file_keeps_memory(self):
        app.add_one_task("Keep me")
        buffer = StringIO()
        with redirect_stdout(buffer):
            loaded = app.load_todos()
        self.assertFalse(loaded)
        self.assertEqual(app.get_todos(), ["Keep me"])
        self.assertIn("does not exist", buffer.getvalue())
        self.assertIn("not changed", buffer.getvalue())

    def test_corrupt_csv_keeps_memory(self):
        app.add_one_task("Keep me")
        file = open("todos.csv", "w", encoding="utf-8")
        file.write("not,a,single,field\n")
        file.close()
        buffer = StringIO()
        with redirect_stdout(buffer):
            loaded = app.load_todos()
        self.assertFalse(loaded)
        self.assertEqual(app.get_todos(), ["Keep me"])
        self.assertIn("more than one column", buffer.getvalue())
        self.assertIn("not changed", buffer.getvalue())

    def test_nul_bytes_keep_memory(self):
        app.add_one_task("Keep me")
        file = open("todos.csv", "w", encoding="utf-8")
        file.write("ok\x00hidden")
        file.close()
        buffer = StringIO()
        with redirect_stdout(buffer):
            loaded = app.load_todos()
        self.assertFalse(loaded)
        self.assertEqual(app.get_todos(), ["Keep me"])
        self.assertIn("not a text file", buffer.getvalue())

    def test_invalid_utf8_keeps_memory(self):
        app.add_one_task("Keep me")
        file = open("todos.csv", "wb")
        file.write(b"\xff\xfe not utf-8")
        file.close()
        buffer = StringIO()
        with redirect_stdout(buffer):
            loaded = app.load_todos()
        self.assertFalse(loaded)
        self.assertEqual(app.get_todos(), ["Keep me"])
        self.assertIn("not valid UTF-8", buffer.getvalue())

    def test_delete_accepts_int_and_numeric_string(self):
        app.add_one_task("Make the bed")
        app.add_one_task("Make lunch")
        app.add_one_task("Clean kitchen")
        self.assertTrue(app.delete_task("2"))
        self.assertEqual(app.get_todos(), ["Make the bed", "Clean kitchen"])
        with redirect_stdout(StringIO()):
            self.assertTrue(app.delete_task(1))
        self.assertEqual(app.get_todos(), ["Clean kitchen"])

    def test_delete_on_empty_list_explains_the_next_step(self):
        buffer = StringIO()
        with redirect_stdout(buffer):
            removed = app.delete_task(1)
        self.assertFalse(removed)
        self.assertEqual(app.get_todos(), [])
        self.assertIn("list is empty", buffer.getvalue())
        self.assertIn("option 1", buffer.getvalue())

    def test_invalid_positions_do_not_change_the_list(self):
        app.add_one_task("Only task")
        cases = ["0", "-1", "2", "abc", "", "1.5", None]
        for case in cases:
            buffer = StringIO()
            with redirect_stdout(buffer):
                result = app.delete_task(case)
            self.assertFalse(result, case)
            self.assertEqual(app.get_todos(), ["Only task"])
            self.assertIn("Invalid position", buffer.getvalue())

    def test_print_list_uses_one_based_positions(self):
        app.add_one_task("Make the bed")
        app.add_one_task("Clean kitchen")
        buffer = StringIO()
        with redirect_stdout(buffer):
            app.print_list()
        self.assertEqual(buffer.getvalue(), "1. Make the bed\n2. Clean kitchen\n")

    def test_print_list_empty_state_names_the_next_action(self):
        buffer = StringIO()
        with redirect_stdout(buffer):
            app.print_list()
        text = buffer.getvalue()
        self.assertIn("No tasks yet", text)
        self.assertIn("option 1", text)
        self.assertIn("Make the bed", text)

    def test_several_adds_keep_order(self):
        for title in ("one", "two", "three", "four"):
            app.add_one_task(title)
        self.assertEqual(app.get_todos(), ["one", "two", "three", "four"])


if __name__ == "__main__":
    unittest.main()
