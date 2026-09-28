---
name: sandbox-stats
description: >-
  Write and run a Python stats script inside the OpenShell sandbox. Use when
  the user asks for descriptive statistics, random-number summaries, mean,
  median, stddev, min/max, or a quick numeric analysis that should execute
  under /sandbox.
---

# Sandbox stats

## Overview

Produce a short summary of a numeric series by writing a script under
`/sandbox/`, executing it with the `execute` tool, and reporting stdout.

Skills and memory on the host (`/skills/`, `/memory/`) are **not** visible to
sandbox Python. Keep all runnable code under `/sandbox/`.

## Companion script

A checked-in companion lives next to this skill:

`/skills/sandbox-stats/stats_companion.py`

Prefer this pattern:

1. `read_file("/skills/sandbox-stats/stats_companion.py")` (or this `SKILL.md`).
2. `write_file` the companion body to `/sandbox/stats.py` (adapt the sample
   size or dataset if the user asked for something specific).
3. `execute("python3 /sandbox/stats.py")`.

Do **not** try to `python3 /skills/...` — that path is host-only via agent
file tools.

## Instructions

1. Create the working directory if needed:
   `os.makedirs("/sandbox", exist_ok=True)` inside the script, or
   `mkdir -p /sandbox` via `execute`.
2. Prefer the companion above; otherwise use `write_file` to create
   `/sandbox/stats.py` from the example pattern below.
3. Prefer the stdlib only (`statistics`, `random`) unless the user asks for
   third-party packages and policy allows installing them.
4. Print a concise summary to stdout (under ~10KB). If the full dataset is
   large, write it to `/sandbox/results.txt` and use `read_file` to show a
   sample.
5. Run with `execute("python3 /sandbox/stats.py")`.
6. On failure, fix the script and retry at most twice; then report the error.

## Example pattern

```python
import os
import random
import statistics

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
```

## Success criteria

- Skill or companion was consulted under `/skills/sandbox-stats/`
- Script lives under `/sandbox/` (not executed from `/skills/`)
- `execute` exits 0
- User sees n, mean, median, stdev (or equivalent), min, and max
