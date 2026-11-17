#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Vince Bono
"""Score one attack attempt: how often did the camera still see a person?

Reads the board's `FTC,<millis>,<score>` lines for a few seconds and appends one row to a CSV.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from collections.abc import Iterable, Iterator
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["time_utc", "attack", "frames", "detected", "detection_rate", "mean_score"]


def parse(line: str) -> int | None:
    """Person score from one serial line, or None for anything that isn't ours."""
    parts = line.strip().split(",")
    if len(parts) != 3 or parts[0] != "FTC":
        return None
    try:
        return int(parts[2])
    except ValueError:
        return None


def summarize(scores: list[int], threshold: int = 0) -> dict[str, float | int]:
    hits = [s for s in scores if s > threshold]
    return {
        "frames": len(scores),
        "detected": len(hits),
        "detection_rate": round(len(hits) / len(scores), 3) if scores else 0.0,
        "mean_score": round(sum(hits) / len(hits), 1) if hits else 0.0,
    }


def serial_lines(port: str, baud: int, seconds: float) -> Iterator[str]:
    import serial  # pyserial; only needed when reading from a board

    end = time.monotonic() + seconds
    with serial.Serial(port, baud, timeout=1) as ser:
        while time.monotonic() < end:
            yield ser.readline().decode("ascii", "replace")


def record(lines: Iterable[str], attack: str, out: Path, threshold: int = 0) -> dict[str, object]:
    scores = [s for s in map(parse, lines) if s is not None]
    row: dict[str, object] = {
        "time_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "attack": attack,
        **summarize(scores, threshold),
    }
    new = not out.exists()
    with out.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    return row


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("attack", help='label for this attempt, e.g. "baseline" or "paper patch on chest"')
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--port", help="serial port of the board, e.g. COM5 or /dev/ttyUSB0")
    src.add_argument("--file", type=Path, help="read saved serial output instead of a board")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--seconds", type=float, default=20, help="how long to watch (default 20)")
    ap.add_argument("--threshold", type=int, default=0, help="count a frame as detected above this score")
    ap.add_argument("--out", type=Path, default=Path("results.csv"))
    args = ap.parse_args(argv)

    if args.file:
        lines: Iterable[str] = args.file.read_text(encoding="utf-8", errors="replace").splitlines()
    else:
        lines = serial_lines(args.port, args.baud, args.seconds)
    row = record(lines, args.attack, args.out, args.threshold)
    if not row["frames"]:
        print("No FTC lines seen. Is the sketch running and the port right?", file=sys.stderr)
        return 1
    print(f"{row['attack']}: person seen in {row['detected']}/{row['frames']} frames "
          f"({row['detection_rate']:.0%}), mean score {row['mean_score']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
