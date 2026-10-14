#!/usr/bin/env python3
"""Print one spoiler-safe hint from a scenario.

Usage: hints.py /scenarios/scenario_02_linux.yml 2
"""
import sys
import yaml


def main():
    if len(sys.argv) != 3:
        print("usage: hints.py <scenario.yml> <level 1-3>", file=sys.stderr)
        return 2
    try:
        level = int(sys.argv[2])
    except ValueError:
        print("hint level must be 1, 2, or 3", file=sys.stderr)
        return 2
    if level not in (1, 2, 3):
        print("hint level must be 1, 2, or 3", file=sys.stderr)
        return 2
    with open(sys.argv[1], encoding="utf-8") as handle:
        scenario = yaml.safe_load(handle) or {}
    hints = scenario.get("hints", [])
    # Existing v1 scenarios remain playable while authors progressively add
    # tailored hints. These are intentionally generic and disclose no IOC,
    # query, or technique from the answer key.
    if not hints:
        hints = [
            "Start with the asset and time range named in the ticket; establish the first anomalous event.",
            "Pivot from that event on a stable field such as host, account, source, destination, or process.",
            "Compare activity immediately before and after the pivot to reconstruct the sequence, then record only evidence you can cite.",
        ]
    if len(hints) < level:
        print(f"Only {len(hints)} hint level(s) are available for {scenario.get('id')}.")
        return 1
    print(f"Hint {level}/3 — {scenario.get('name', scenario.get('id'))}")
    print(hints[level - 1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
