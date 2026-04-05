import contextlib
import sys
import os
import unittest
import io
import tempfile
from project1 import *

class TestProject1(unittest.TestCase):
    def setUp(self):

        self._temp_file = tempfile.NamedTemporaryFile(mode = "w+", delete=False)
        self._temp_file.write("LENGTH 9999\n" +
                "DEVICE 1\n" +
                "DEVICE 2\n" +
                "DEVICE 3\n" +
                "DEVICE 4\n" +
                "PROPAGATE 1 2 750\n" +
                "PROPAGATE 2 3 1250\n" +
                "PROPAGATE 3 4 500\n" +
                "PROPAGATE 4 1 1000\n" +
                "ALERT 1 Trouble 0\n" +
                "CANCEL 1 Trouble 2200\n")
        self._temp_file.close()
        self._path = Path(self._temp_file.name)
        self._temp_file_name = self._temp_file.name

    def tearDown(self):
        if Path.exists(self._path):
            os.remove(self._temp_file.name)

    def test_read_an_existent_file(self):
        content = read_from_file(self._path)
        expected = ["LENGTH 9999", "DEVICE 1", "DEVICE 2",
                    "DEVICE 3", "DEVICE 4", "PROPAGATE 1 2 750",
                    "PROPAGATE 2 3 1250", "PROPAGATE 3 4 500",
                    "PROPAGATE 4 1 1000", "ALERT 1 Trouble 0",
                    "CANCEL 1 Trouble 2200"]
        self.assertEqual(content, expected)

    def test_read_a_nonexistent_file(self):

        with (contextlib.redirect_stdout(io.StringIO())) as log:
            path = Path("DOES NOT EXIST")
            read_from_file(path)

        self.assertEqual(log.getvalue(), "FILE NOT FOUND\n")

    def test_read_a_big_file(self):
        content = read_from_file(self._path)

        expected = ['LENGTH 9999', 'DEVICE 1', 'DEVICE 2', 'DEVICE 3', 'DEVICE 4', 'PROPAGATE 1 2 750', 'PROPAGATE 2 3 1250', 'PROPAGATE 3 4 500', 'PROPAGATE 4 1 1000', 'ALERT 1 Trouble 0', 'CANCEL 1 Trouble 2200']

        self.assertEqual(content, expected)

    def test_getting_correct_commands(self):

        lines = read_from_file(self._path)
        test = get_commands(lines)

        expected = Commands("9999", [1,2,3,4], [["1", "2", "750"], ["2", "3", "1250"], ["3", "4", "500"], ["4", "1", "1000"]],
                            [["1", "Trouble", "0"]], [["1", "Trouble", "2200"]])

        self.assertEqual(test, expected)

    def test_log_result_from_run_simulation(self):
        lines = read_from_file(self._path)
        commands = get_commands(lines)
        log = run_simulation(commands)

        expected = ["@0: #1 SENT ALERT TO #2: Trouble",
                    "@750: #2 RECEIVED ALERT FROM #1: Trouble",
                    "@750: #2 SENT ALERT TO #3: Trouble",
                    "@2000: #3 RECEIVED ALERT FROM #2: Trouble",
                    "@2000: #3 SENT ALERT TO #4: Trouble",
                    "@2200: #1 SENT CANCELLATION TO #2: Trouble",
                    "@2500: #4 RECEIVED ALERT FROM #3: Trouble",
                    "@2500: #4 SENT ALERT TO #1: Trouble",
                    "@2950: #2 RECEIVED CANCELLATION FROM #1: Trouble",
                    "@2950: #2 SENT CANCELLATION TO #3: Trouble",
                    "@3500: #1 RECEIVED ALERT FROM #4: Trouble",
                    "@4200: #3 RECEIVED CANCELLATION FROM #2: Trouble",
                    "@4200: #3 SENT CANCELLATION TO #4: Trouble",
                    "@4700: #4 RECEIVED CANCELLATION FROM #3: Trouble",
                    "@4700: #4 SENT CANCELLATION TO #1: Trouble",
                    "@5700: #1 RECEIVED CANCELLATION FROM #4: Trouble"]

        self.assertEqual(log, expected)

    def test_print_log(self):
        lines = read_from_file(self._path)
        commands = get_commands(lines)
        log = run_simulation(commands)

        with contextlib.redirect_stdout(io.StringIO()) as log_printed:
            print_log(log)

        expected = ("@0: #1 SENT ALERT TO #2: Trouble\n" +
                    "@750: #2 RECEIVED ALERT FROM #1: Trouble\n" +
                    "@750: #2 SENT ALERT TO #3: Trouble\n" +
                    "@2000: #3 RECEIVED ALERT FROM #2: Trouble\n" +
                    "@2000: #3 SENT ALERT TO #4: Trouble\n" +
                    "@2200: #1 SENT CANCELLATION TO #2: Trouble\n" +
                    "@2500: #4 RECEIVED ALERT FROM #3: Trouble\n" +
                    "@2500: #4 SENT ALERT TO #1: Trouble\n" +
                    "@2950: #2 RECEIVED CANCELLATION FROM #1: Trouble\n" +
                    "@2950: #2 SENT CANCELLATION TO #3: Trouble\n" +
                    "@3500: #1 RECEIVED ALERT FROM #4: Trouble\n" +
                    "@4200: #3 RECEIVED CANCELLATION FROM #2: Trouble\n" +
                    "@4200: #3 SENT CANCELLATION TO #4: Trouble\n" +
                    "@4700: #4 RECEIVED CANCELLATION FROM #3: Trouble\n" +
                    "@4700: #4 SENT CANCELLATION TO #1: Trouble\n" +
                    "@5700: #1 RECEIVED CANCELLATION FROM #4: Trouble\n" +
                    "@9999: END\n")

        self.assertEqual(log_printed.getvalue(), expected)

    def test_user_input_file_path(self):
        temp_file = tempfile.NamedTemporaryFile(mode = "w+", delete = False)
        temp_file.write("Hello World!")
        temp_file.close()
        user_input = io.StringIO(temp_file.name)
        sys.stdin = user_input
        content = read_from_file(None)
        self.assertEqual(content, ["Hello World!"])

    def test_main(self):
        user_input = io.StringIO(self._temp_file_name)
        sys.stdin = user_input
        with contextlib.redirect_stdout(io.StringIO()) as log_printed:
            main()

        log = log_printed.getvalue()

        expected = ("@0: #1 SENT ALERT TO #2: Trouble\n" +
                    "@750: #2 RECEIVED ALERT FROM #1: Trouble\n" +
                    "@750: #2 SENT ALERT TO #3: Trouble\n" +
                    "@2000: #3 RECEIVED ALERT FROM #2: Trouble\n" +
                    "@2000: #3 SENT ALERT TO #4: Trouble\n" +
                    "@2200: #1 SENT CANCELLATION TO #2: Trouble\n" +
                    "@2500: #4 RECEIVED ALERT FROM #3: Trouble\n" +
                    "@2500: #4 SENT ALERT TO #1: Trouble\n" +
                    "@2950: #2 RECEIVED CANCELLATION FROM #1: Trouble\n" +
                    "@2950: #2 SENT CANCELLATION TO #3: Trouble\n" +
                    "@3500: #1 RECEIVED ALERT FROM #4: Trouble\n" +
                    "@4200: #3 RECEIVED CANCELLATION FROM #2: Trouble\n" +
                    "@4200: #3 SENT CANCELLATION TO #4: Trouble\n" +
                    "@4700: #4 RECEIVED CANCELLATION FROM #3: Trouble\n" +
                    "@4700: #4 SENT CANCELLATION TO #1: Trouble\n" +
                    "@5700: #1 RECEIVED CANCELLATION FROM #4: Trouble\n" +
                    "@9999: END\n")

        self.assertEqual(log, expected)

    def test_when_there_are_no_alerts_or_cancels(self):

        commands = Commands("9999", [1,2,3,4], [["1", "2", "750"], ["2", "3", "1250"], ["3", "4", "500"], ["4", "1", "1000"]],[],[])
        registry_log = run_simulation(commands)
        with contextlib.redirect_stdout(io.StringIO()) as log_printed:
            print_log(registry_log)

        expected = "@9999: END\n"
        self.assertEqual(log_printed.getvalue(), expected)

if __name__ == '__main__':
    unittest.main()

