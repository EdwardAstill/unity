---
name: use_uv_not_pip
description: Always use uv for package management and running tests, never pip directly
type: feedback
---

Use `uv` for all package management and running the project, never `pip` directly.

**Why:** User uses uv as their Python package manager and expects all commands to go through it.

**How to apply:** Use `uv add` for dependencies, `uv add --dev` for dev deps, `uv run` to execute scripts/tests, and `uv pip install -e .` for editable installs.
