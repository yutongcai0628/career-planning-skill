#!/usr/bin/env python3
"""Validate a generated career report without modifying it."""

from __future__ import annotations

import argparse
from pathlib import Path

from render_report import validate_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated career-planning HTML report.")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    try:
        document = args.report.read_text(encoding="utf-8")
    except OSError as error:
        parser.error(str(error))

    errors = validate_report(document)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
