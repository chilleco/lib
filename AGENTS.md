# Repository Guidelines

## Project Structure & Module Organization
- Core library lives in `libdev/` (async HTTP helpers, config, logging, S3, image tools, formatting utilities).
- Tests sit in `tests/` (`test_*.py`), sharing fixtures/config in the same folder.
- Docs are in `docs/` (`LIBDEV_DOCUMENTATION.md`), build assets under `build/` and `dist/` after packaging.
- Packaging metadata: `pyproject.toml`; legacy `setup.py` is a shim for `setuptools`.
- Local config/example values live in `sets.json`; never commit real secrets here.

## Build, Test, and Development Commands
- Create venv + runtime deps: `make setup` or `pip install .`
- Full dev tooling (lint/test/release): `make setup-dev` or `pip install .[dev]`
- Lint + tests: `make test` (runs pylint + pytest)
- Build artifacts: `python -m build` (also runs in `make release` before `twine upload`)
- Clean artifacts: `make clean`; remove venvs/cache: `make clear`

## Coding Style & Naming Conventions
- Python 3.10+; use 4-space indentation and explicit imports.
- Follow pylint rules from `tests/.pylintrc`; keep functions small and async-safe where network I/O occurs.
- Tests mirror module names: `test_<module>.py`; fixtures inline or colocated.
- Avoid committing generated files (`build/`, `dist/`, `*.egg-info/`, `__pycache__/`).

## Testing Guidelines
- Frameworks: `pytest`, `pytest-asyncio`; run via `make test` or `python -m pytest -s tests/`.
- Name tests descriptively (`test_req_fetch_handles_json`) and keep async tests using `@pytest.mark.asyncio`.
- For config-dependent code, override with `set_cfg()` in test setup and reset after.

## Commit & Pull Request Guidelines
- Commits: concise, imperative summaries (e.g., `Add pyproject metadata`, `Fix req fetch errors`); group related changes.
- PRs: describe intent, key changes, and testing performed; link issues if applicable. Include notes on config/secrets expectations and any breaking API shifts.

## Security & Configuration Tips
- Do not commit real credentials in `sets.json` or `.env`; use placeholders in examples.
- S3 helpers initialize at import—tests should mock or supply dummy endpoints/keys to avoid real uploads.
