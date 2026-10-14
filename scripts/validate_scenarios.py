#!/usr/bin/env python3
"""Fast, offline schema checks for DWELL scenario source files."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TECHNIQUE = re.compile(r"^T\d{4}(\.\d{3})?$")
REQUIRED = ("id", "name", "difficulty", "requires", "backstory", "chain", "expected_detections", "iocs", "answer_summary")


def fail(errors, path, message):
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def main():
    errors, ids = [], set()
    for path in sorted((ROOT / "scenarios").glob("scenario_*.yml")):
        if path.name == "scenario_template.yml":
            continue
        try:
            with path.open(encoding="utf-8") as handle:
                data = yaml.safe_load(handle)
        except yaml.YAMLError as exc:
            fail(errors, path, f"invalid YAML: {exc}")
            continue
        if not isinstance(data, dict):
            fail(errors, path, "must contain a mapping")
            continue
        for key in REQUIRED:
            if not data.get(key):
                fail(errors, path, f"missing or empty '{key}'")
        sid = data.get("id", "")
        if sid in ids:
            fail(errors, path, f"duplicate id '{sid}'")
        ids.add(sid)
        if sid and path.stem != sid:
            fail(errors, path, f"id '{sid}' must match filename '{path.stem}'")
        if data.get("difficulty") not in {"easy", "medium", "hard"}:
            fail(errors, path, "difficulty must be easy, medium, or hard")
        if data.get("requires") not in {"linux", "windows"}:
            fail(errors, path, "requires must be linux or windows")
        for step in data.get("chain", []):
            if not isinstance(step, dict) or not TECHNIQUE.match(str(step.get("technique", ""))):
                fail(errors, path, "each chain step needs a valid ATT&CK technique")
        for detection in data.get("expected_detections", []):
            if not isinstance(detection, dict) or not detection.get("index") or not detection.get("query"):
                fail(errors, path, "each expected detection needs index and query")
        hints = data.get("hints", [])
        if hints and (not isinstance(hints, list) or len(hints) != 3 or not all(isinstance(h, str) and h.strip() for h in hints)):
            fail(errors, path, "hints must be exactly three non-empty strings")
    if errors:
        print("Scenario validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Scenario validation passed ({len(ids)} scenarios).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
