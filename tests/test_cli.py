import io
import unittest
from contextlib import redirect_stdout

from ulid_cli.cli import main


class TestCli(unittest.TestCase):
    def test_default_prints_one_ulid(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main([])
        self.assertEqual(code, 0)
        lines = out.getvalue().strip().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(len(lines[0]), 26)

    def test_count_generates_multiple(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["--count", "5"])
        self.assertEqual(code, 0)
        lines = out.getvalue().strip().splitlines()
        self.assertEqual(len(lines), 5)

    def test_count_zero_is_an_error(self) -> None:
        code = main(["--count", "0"])
        self.assertEqual(code, 2)

    def test_fixed_timestamp_is_reproducible_in_time_prefix(self) -> None:
        out1 = io.StringIO()
        with redirect_stdout(out1):
            main(["--timestamp", "1469918176385"])
        out2 = io.StringIO()
        with redirect_stdout(out2):
            main(["--timestamp", "1469918176385"])
        # time component (first 10 chars) must match; randomness may differ.
        self.assertEqual(out1.getvalue().strip()[:10], out2.getvalue().strip()[:10])

    def test_timestamp_out_of_range_exits_two(self) -> None:
        code = main(["--timestamp", str(2 ** 48)])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
