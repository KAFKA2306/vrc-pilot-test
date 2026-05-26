# Repository Guidelines

## Project Structure & Module Organization

- Keep experiment code out of `src/`. Put runnable scripts under `exp/{NNN}_{purpose}/`, with one entry file per experiment, for example `exp/001_vrchat_explorer/explorer.py`.
- `Taskfile.yml` is the only supported entry point for local runs.
- `docs/ADR/` holds decision records and `scripts/` holds helper shell scripts.
- `pyproject.toml` and `uv.lock` define Python dependencies and lock state.

## Build, Test, and Development Commands

- `task explorer` runs the VRChat explorer experiment.
- `task mass-photographer` runs the multi-world photo experiment.
- `uv run python <path>` is the underlying execution pattern used by Taskfile targets.
- If you add new runnable experiments, add a matching Taskfile target instead of invoking the script directly.

## Coding Style & Naming Conventions

- Use Python 3.12+.
- Keep code direct and minimal. Do not add comments unless a line is genuinely hard to read.
- Use snake_case for Python names and lower-case task names with hyphens, such as `mass-photographer`.
- Name experiment directories with a zero-padded numeric prefix and a concrete purpose: `exp/002_vrchat_mass_photographer/`.

## Testing Guidelines

- There is no test suite in the repository yet.
- When you add behavior, prefer a small runnable experiment in `exp/` and verify it through the matching `task` target.
- Keep generated artifacts out of version control unless they are deliberate examples.

## Commit & Pull Request Guidelines

- The repository has no commit history yet, so there is no established message convention.
- Use short imperative commit subjects, for example: `Add VRChat explorer task`.
- PRs should explain what changed, how to run it, and any manual verification performed.
- Include screenshots or output files only when they help review the change.

## Configuration Notes

- Keep environment-specific paths and cache settings in `Taskfile.yml`, not scattered through scripts.
- Avoid moving experiment logic back into `src/`; that directory should stay empty unless the project later gains shared library code.
