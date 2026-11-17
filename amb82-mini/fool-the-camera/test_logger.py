# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Vince Bono
import csv
import tempfile
import unittest
from pathlib import Path

from logger import main, parse, summarize


class LoggerTest(unittest.TestCase):
    def test_parse_takes_only_our_lines(self):
        self.assertEqual(parse("FTC,1234,87\r\n"), 87)
        self.assertEqual(parse("FTC,1234,0"), 0)
        self.assertIsNone(parse("Connecting to wifi"))
        self.assertIsNone(parse("FTC,1234,abc"))
        self.assertIsNone(parse("FTC,1,2,3"))

    def test_summarize_counts_frames_with_a_person(self):
        self.assertEqual(
            summarize([80, 0, 60, 0]),
            {"frames": 4, "detected": 2, "detection_rate": 0.5, "mean_score": 70.0},
        )
        self.assertEqual(summarize([])["detection_rate"], 0.0)
        self.assertEqual(summarize([40, 90], threshold=50)["detected"], 1)

    def test_main_appends_a_row_per_attempt_and_fails_on_no_data(self):
        with tempfile.TemporaryDirectory() as d:
            log, out = Path(d, "serial.txt"), Path(d, "results.csv")
            log.write_text("boot noise\nFTC,1,90\nFTC,2,0\n", encoding="utf-8")
            self.assertEqual(main(["baseline", "--file", str(log), "--out", str(out)]), 0)
            self.assertEqual(main(["patch", "--file", str(log), "--out", str(out)]), 0)
            rows = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual([r["attack"] for r in rows], ["baseline", "patch"])
            self.assertEqual(rows[0]["detection_rate"], "0.5")
            log.write_text("nothing useful\n", encoding="utf-8")
            self.assertEqual(main(["empty", "--file", str(log), "--out", str(out)]), 1)


if __name__ == "__main__":
    unittest.main()
