#!/usr/bin/env python3
"""Validate recorded cross-host forward-test results."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_HOSTS = {"claude-code", "codex", "kimi-code", "cursor"}
ALLOWED_RESULTS = {"pass", "fail", "blocked"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")


def validate(payload: object, require_all: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["Root value must be an object"]
    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if set(payload.get("required_hosts", [])) != REQUIRED_HOSTS:
        errors.append("required_hosts must list claude-code, codex, kimi-code, and cursor")

    runs = payload.get("runs")
    if not isinstance(runs, list):
        return errors + ["runs must be an array"]

    latest_results: dict[str, str] = {}
    seen_ids: set[str] = set()
    for index, run in enumerate(runs):
        label = f"runs[{index}]"
        if not isinstance(run, dict):
            errors.append(f"{label} must be an object")
            continue
        required = {
            "id",
            "host",
            "host_version",
            "date",
            "skill_commit",
            "cases",
            "result",
            "artifact",
            "notes",
        }
        missing = sorted(required - run.keys())
        unknown = sorted(run.keys() - required)
        if missing:
            errors.append(f"{label} missing: {', '.join(missing)}")
        if unknown:
            errors.append(f"{label} unknown keys: {', '.join(unknown)}")
        if missing:
            continue

        run_id = run["id"]
        if not isinstance(run_id, str) or not run_id:
            errors.append(f"{label}.id must be a non-empty string")
        elif run_id in seen_ids:
            errors.append(f"{label}.id is duplicated")
        else:
            seen_ids.add(run_id)

        host = run["host"]
        if host not in REQUIRED_HOSTS:
            errors.append(f"{label}.host is unsupported")
        if not isinstance(run["host_version"], str) or not run["host_version"].strip():
            errors.append(f"{label}.host_version must be recorded")
        if not isinstance(run["date"], str) or not DATE_RE.fullmatch(run["date"]):
            errors.append(f"{label}.date must use YYYY-MM-DD")
        if not isinstance(run["skill_commit"], str) or not COMMIT_RE.fullmatch(run["skill_commit"]):
            errors.append(f"{label}.skill_commit must be a 7–40 character Git hash")
        if not isinstance(run["cases"], list) or not run["cases"] or not all(
            isinstance(case, str) and case for case in run["cases"]
        ):
            errors.append(f"{label}.cases must list executed blind-eval case ids")
        if run["result"] not in ALLOWED_RESULTS:
            errors.append(f"{label}.result must be pass, fail, or blocked")
        artifact = run["artifact"]
        if not isinstance(artifact, str) or not artifact.startswith("tests/host-artifacts/"):
            errors.append(f"{label}.artifact must point inside tests/host-artifacts/")
        if not isinstance(run["notes"], str):
            errors.append(f"{label}.notes must be a string")
        if host in REQUIRED_HOSTS:
            latest_results[host] = run["result"]

    if require_all:
        missing_passes = sorted(host for host in REQUIRED_HOSTS if latest_results.get(host) != "pass")
        if missing_passes:
            errors.append("Missing passing host runs: " + ", ".join(missing_passes))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("--require-all", action="store_true")
    args = parser.parse_args()

    try:
        payload = json.loads(args.results.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        parser.error(str(error))
    errors = validate(payload, require_all=args.require_all)
    if isinstance(payload, dict) and isinstance(payload.get("runs"), list):
        repository = Path(__file__).resolve().parent.parent
        for index, run in enumerate(payload["runs"]):
            if not isinstance(run, dict) or not isinstance(run.get("artifact"), str):
                continue
            artifact = repository / run["artifact"]
            if not artifact.is_file():
                errors.append(f"runs[{index}].artifact does not exist: {run['artifact']}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.results}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
