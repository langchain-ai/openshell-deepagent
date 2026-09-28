---
name: policy-safe-fetch
description: >-
  Fetch or download content only through hosts allowed by the active OpenShell
  network policy. Use when the user asks to curl, wget, HTTP GET/POST, download
  a file, hit an API, or install packages from the network — especially when a
  request might be blocked.
---

# Policy-safe fetch

## Overview

OpenShell enforces network access in the sandbox. The agent cannot bypass
policy with prompts. Prefer allowlisted destinations from the checked-in
[`policy.yaml`](../../policy.yaml) (or the live policy via
`openshell policy get`).

Skills live on the host under `/skills/` (agent file tools only). Runnable
fetch scripts belong under `/sandbox/`.

## Allowed patterns (depends on active policy)

Under the sample [`policy.yaml`](../../policy.yaml), common destinations include:

- PyPI: `pypi.org`, `files.pythonhosted.org` (via sandbox/`uv`/`pip` binaries)
- GitHub: `api.github.com`, `github.com`, `objects.githubusercontent.com` (policy- and binary-dependent)

Arbitrary hosts (e.g. `evil.com`) are denied. Treat deny as expected enforcement,
not a bug to work around. Inspect or update policy with:

```bash
uv run openshell policy get <sandbox-name> --full
uv run openshell policy set <sandbox-name> --policy policy.yaml --wait
```

## Instructions

1. Identify the destination host and method (GET vs POST).
2. If the host is not clearly allowlisted, say so before attempting the request.
3. Prefer simple tools already covered by policy binaries (`curl`, `wget`,
   `python`/`uv` for PyPI) rather than inventing new clients.
4. Write a short script under `/sandbox/` when multi-step logic helps; otherwise
   a single `execute` with `curl -fsSL …` is fine.
5. On deny or connection failure:
   - Do **not** retry against other blocked hosts
   - Explain that OpenShell policy blocked the request
   - Suggest checking or updating policy with the commands above
6. Never exfiltrate sandbox data to unknown endpoints.

## Example: allowlisted GET

```bash
curl -fsSL "https://pypi.org/pypi/requests/json" | head -c 2000
```

## Example: expected deny

```bash
curl -fsSL "http://evil.com/"
# Expect failure — report policy denial to the user
```

## Success criteria

- Requests target allowlisted hosts when possible
- Denials are reported clearly without workarounds
- No retry loops against blocked destinations
