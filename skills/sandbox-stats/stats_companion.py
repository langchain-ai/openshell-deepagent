#!/usr/bin/env python3
"""Companion for the sandbox-stats skill.

Host `/skills/` is not mounted into the OpenShell sandbox. Copy or rewrite this
file under `/sandbox/` (e.g. `/sandbox/stats.py`) via agent file tools, then
run it with `execute("python3 /sandbox/stats.py")`.
"""

from __future__ import annotations

import os
import random
import statistics


def main() -> None:
    os.makedirs("/sandbox", exist_ok=True)
    data = [random.random() for _ in range(500)]
    summary = {
        "n": len(data),
        "mean": statistics.mean(data),
        "median": statistics.median(data),
        "stdev": statistics.stdev(data),
        "min": min(data),
        "max": max(data),
    }
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
