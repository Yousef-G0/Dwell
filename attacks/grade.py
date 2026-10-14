#!/usr/bin/env python3
"""Grade learner findings without revealing the scenario answer key.

Accepted answer-file form:
  scenario: scenario_02_linux
  iocs:
    - {type: ip, value: 172.30.0.99}
  findings:
    - {id: initial_access, value: SSH brute force}
"""
import json
import sys

import yaml


def norm(value):
    return " ".join(str(value).casefold().split())


def load(path):
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main():
    if len(sys.argv) != 3:
        print("usage: grade.py <scenario.yml> <answers.yml>", file=sys.stderr)
        return 2
    scenario, answers = load(sys.argv[1]), load(sys.argv[2])
    if answers.get("scenario") and answers["scenario"] != scenario.get("id"):
        print(json.dumps({"error": "answers file names a different scenario"}))
        return 2

    expected_iocs = {(norm(i.get("type")), norm(i.get("value")))
                     for i in scenario.get("iocs", []) if i.get("value")}
    submitted_iocs = {(norm(i.get("type")), norm(i.get("value")))
                      for i in answers.get("iocs", []) if isinstance(i, dict) and i.get("value")}
    found_iocs = expected_iocs & submitted_iocs

    rubric = scenario.get("grading", {}).get("required_findings", [])
    submitted_findings = {str(f.get("id")): norm(f.get("value", ""))
                          for f in answers.get("findings", []) if isinstance(f, dict) and f.get("id")}
    found_findings = []
    for item in rubric:
        value = submitted_findings.get(str(item.get("id")), "")
        if value and any(value == norm(choice) for choice in item.get("accepted", [])):
            found_findings.append(item["id"])

    total = len(expected_iocs) + len(rubric)
    earned = len(found_iocs) + len(found_findings)
    score = round((earned / total) * 100) if total else 100
    result = {
        "scenario": scenario.get("id"), "score": score,
        "earned": earned, "possible": total,
        "ioc_credit": {"earned": len(found_iocs), "possible": len(expected_iocs)},
        "finding_credit": {"earned": len(found_findings), "possible": len(rubric)},
        "feedback": "Compare your timeline to the ticket and investigate the missing evidence." if earned < total else "Case reconstruction complete."
    }
    print(json.dumps(result, indent=2))
    return 0 if earned == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
