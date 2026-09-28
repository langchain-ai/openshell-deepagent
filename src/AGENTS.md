# Agent Memory

## Two filesystem views

CompositeBackend routes some paths to the **host**; everything else goes to the
**OpenShell sandbox**. They are not the same mount.

| Path | Visible to | Backend |
|------|------------|---------|
| `/memory/*` | Agent file tools only | Host `./src` (this file lives here as `/memory/AGENTS.md`) |
| `/skills/*` | Agent file tools only | Host `./skills` |
| `/sandbox/*` | Agent tools **and** sandbox Python/bash | OpenShell container |

In-sandbox Python cannot `open("/memory/...")` or rely on a live
`/sandbox/memory/AGENTS.md` as the CompositeBackend route. Use
`read_file("/memory/AGENTS.md")` for durable memory. A read-only snapshot may
be uploaded to `/sandbox/memory/` at backend startup for Python that needs the
text inside the container — treat it as a copy, not the source of truth.

## Sandbox Environment

This agent executes code in an OpenShell sandbox — an isolated, policy-governed
Linux environment provisioned on-prem. The sandbox provides:
- Python, bash, and common Linux tools
- A writable `/sandbox/` directory for scripts and outputs
- Policy-governed network access (controlled by the active sandbox policy)
- SSH-based file transfer for uploads and downloads

## Workflow

1. Write scripts to `/sandbox/<name>.py` using write_file
2. Execute with the execute tool: `execute("python /sandbox/<name>.py")`
3. Check output; fix errors and retry if needed (max 2 retries per error)
4. Summarize results for the user
5. Persist lasting notes with write_file/edit_file on `/memory/AGENTS.md` (host)

## Key Patterns

- Always create output directories: `os.makedirs("/sandbox", exist_ok=True)`
- Print only summaries to stdout; write full results to `/sandbox/results.txt`
- Use read_file for `/memory/` and `/sandbox/` paths; only `/sandbox/` works from Python
- When network access is denied, check the sandbox policy with: `openshell policy get <name>`

## Self-Improvement

Update this file when you discover reliable patterns or encounter recurring issues
that would be useful to remember across sessions.
