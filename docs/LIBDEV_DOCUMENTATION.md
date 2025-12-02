# LibDev Integration Guide

This document is meant to be copied into consuming projects (`docs/` or similar) so that automated AI code writers and human contributors understand how to interact with the `libdev` package (version 0.96). It expands on the minimal README, explains what makes LibDev different from generic helper libraries, and records the rules the rest of the chill codebase expects consumers to follow.

## Purpose & Scope
- `libdev` is the canonical toolbox for DevOps and backend projects in this organization. It replaces ad-hoc helpers with a curated set of functions covering configuration, logging, network access, numeric/time formatting, validation, localization, file processing (S3 + images), and crypto.
- Every repository that depends on LibDev should treat it as the single source of truth for these concerns. When extending a project, first look for an existing LibDev helper instead of reimplementing functionality.
- The package targets Python 3.10+ (<4) and ships under the MIT License. Core dependencies: `aiohttp`, `python-dotenv`, `boto3`, `Pillow`, and `loguru`.

## Installation & Versioning
```bash
pip install libdev  # Latest from PyPI https://pypi.org/project/libdev/
```
- Pin the version in each consumer so breaking changes are controlled. The current repo ships `__version__ = "0.96"`.
- Local dev installs use PEP 621 metadata in `pyproject.toml` (no `requirements*.txt`). Install runtime deps with `pip install .`; install tooling/tests with `pip install .[dev]` or `make setup-dev`.
- Run `make test` before releasing; `make release` builds and uploads wheels via `python -m build` + `twine`.

## Principles & Differences vs Other Helper Kits
1. **Configuration-first**: A JSON file (`sets.json`) in the project root plus `.env` variables are the authoritative configuration sources. Nested keys are read via dot-notation and mirrored to upper-case underscore env vars. Values are JSON-deserialized automatically.
2. **Async boundary is explicit**: Anything that touches the network (`libdev.req`, `libdev.s3`, `libdev.img.convert` when fetching URLs) is declared `async`. Callers must stay inside an event loop and `await` these helpers instead of mixing synchronous libraries.
3. **Structured logging**: The bundled `loguru` logger is wrapped so every module logs through `libdev.log.log`. JSON logging is built-in via `log.json(payload)` to keep machine-readable traces consistent.
4. **Opinionated formatting**: `libdev.num`, `libdev.time`, and `libdev.lang` encode company-specific numeric, temporal, and localization rules (e.g., Russian month names, zero-compression notation, thousands separators). Projects must use them to guarantee UI/API consistency.
5. **Strict validation helpers**: `libdev.check` and `libdev.dev` codify how to sanitize contact data, URLs, and IPs. These are stricter than typical regexes (e.g., `fake_mail`, `fake_phone`, `check_public_ip`) to protect analytics and anti-fraud systems.
6. **AWS/S3 abstraction**: Credentials are loaded from config at import time and reused, so consumers rarely touch `boto3` directly. Upload helpers understand bytes, file paths, remote URLs, or already opened file objects.
7. **Deterministic datasets**: Currency, locale, flag, and network code tables (`libdev.fin` & `libdev.codes`) are versioned with the package. Do not mutate them at runtime; request an upstream change instead.

## Configuration Workflow (`libdev.cfg`)
- On import, the module reads `sets.json` (if present) and optionally `.env` using `python-dotenv`.
- Access values via `cfg("path.to.key", default=None)`. The function tries nested dictionaries inside `sets`, and when missing falls back to environment variables named `PATH_TO_KEY` (upper-case, dots replaced with `_`).
- Environment values are automatically `json.loads`-ed when possible, so strings like `"true"`, `"123"`, or `{...}` become booleans, numbers, or dicts.
- Use `set_cfg("path.to.key", value)` to mutate the in-memory `sets` dictionary (e.g., overriding values in tests). Changes are not persisted back to disk.
- Common keys:
  - `project_name`: default S3 bucket name.
  - `mode`: used when building directory prefixes in S3 helpers (e.g., `test/uploads`).
  - `s3.host`, `s3.user`, `s3.pass`, `s3.region`.
- Example `sets.json` skeleton (do **not** check secrets into VCS):
```json
{
  "mode": "production",
  "project_name": "my-bucket",
  "s3": {
    "host": "https://s3.example.com/",
    "user": "ACCESS_KEY",
    "pass": "SECRET",
    "region": "us-east-1"
  }
}
```

## Module Reference & Usage Rules
Below is a curated list of the modules shipped inside `libdev`. Follow the call patterns shown here instead of importing third-party libraries directly.

### System Layer
**`libdev.log`**
- Exposes `log` (a `loguru` logger) plus `Logger.json(data)` for structured records. It auto-adds `sys.stderr` as a sink and removes sinks on exit, so do not call `log.remove()` yourself.
- Example:
```python
from libdev.log import log
log.info("Service booting")
log.json({"event": "http_request", "status": 200, "path": "/api"})
```

**`libdev.req`**
- `await fetch(url, payload=None, files=None, type_req="post", type_data="json", headers=None, timeout=None)`
- Returns `(status_code, response_payload)` where `response_payload` is JSON when possible, otherwise `str` or `bytes`.
- If `files` is supplied (mapping name -> file-like/bytes), it automatically switches to multipart form-data and overrides `type_data` to `"data"`.
- Always use this helper for outbound HTTP so retries, logging, and parsing stay consistent. Bring your own rate limiting/retries at the caller.

**`libdev.doc`**
- `to_base64(file_obj, mime="image/jpg")` turns a binary stream into a Data URL.
- `to_json(obj)` dumps JSON with tab indentation and `ensure_ascii=False` (keeps Cyrillic intact). Prefer it for logging/debug output.

### Data Format Layer
**`libdev.num`** (numeric conversions & display)
- Conversion helpers: `is_float`, `to_num`, `to_int`, `get_float`.
- Representation helpers: `get_whole`, `simplify_value`, `add_sign`, `add_radix`, `to_plain`.
- Math helpers using `Decimal` to avoid FP drift: `add`, `sub`, `mul`, `div`, `to_step`.
- Presentation helpers: `pretty` (round/format/compress zeros, add thousands separators, optional sign), `compress_zeros` (replace long zero runs with subscript notation `0.0₄56`).
- Always rely on these when showing numeric data to users or storing values as strings in APIs; they encode the product team’s formatting choices.

**`libdev.time`** (time parsing/formatting)
- Formatting: `get_time`, `get_date`, `format_delta`, `get_midnight`, `get_week_start`, `get_month_start`, `get_next_day`, `get_next_month`, `get_delta_days`.
- Parsing: `decode_time`, `decode_date`, `parse_time`. `parse_time` understands Russian month names, weekday abbreviations, and timezone hints like `msk`.
- `to_tz(hours)` builds timezone objects; pass the same offset into the other helpers for consistent behavior.

### Transform Layer
**`libdev.gen`**
- `generate(length=32)` random token (digits + ASCII letters).
- `generate_id(length=8)` ensures the leading digit is non-zero.
- `generate_password(length=8)` enforces a mix of special characters, digits, and letters; actual composition is `spec ≈ length/3`, `digits ≈ length/3`, remainder letters.

**`libdev.codes`**
- Provides static tuples of ISO-639-1 locale codes, emoji flags, supported login networks, and user status levels.
- `get_locale(code)` returns the index in `LOCALES`. Accepts a string code (`"ru"`) or integer index. Defaults to the locale configured via `cfg("locale", "en")`.
- `get_network(code)` maps channel identifiers (`"tg"`, `"vk"`, `"web"`) to array indexes used in databases.
- `get_flag(code)` converts a locale code/index to the matching emoji in `FLAGS`.

**`libdev.check`**
- Validation: `check_phone`, `check_mail`, `check_url`.
- Sanitization: `rm_phone`, `clear_text`, `get_base_url`, `get_url`, `get_last_url`.
- Fake-data heuristics: `fake_phone`, `fake_login`, `fake_mail` use curated blacklists for QA/test accounts.
- Always call these before trusting user-supplied contact info or URLs. They are stricter than typical regex patterns.

**`libdev.crypt`**
- Custom reversible obfuscation for integers: `encrypt(number, length=5)` + `decrypt(encoded_str)`.
- Uses base62 + checksum + random prefix padding. Result length is at least `length` (longer when encoding large integers). Not a security primitive—only for obscuring IDs in URLs/logs.

### Domain-Specific Layer
**`libdev.dev`**
- `check_public_ip(ip)` returns the IPv4 address if it is public; returns `None` for private/reserved ranges (`10.`, `172.16-31`, `192.168`, `127.`). Use before storing analytics data.

**`libdev.fin`**
- Dictionaries of currency symbols (`CURRENCY_SYMBOLS`), titles (`CURRENCY_TITLES`), and reference rates to USD (`CURRENCY_RATES`). Rates are static snapshots—refresh upstream if product requirements demand real-time FX.

**`libdev.lang`**
- Russian pluralization: `get_form(count, (singular, paucal, plural))`.
- Transliteration / slugification: `transliterate`, `to_letters`, `to_url` (handles Cyrillic, percent-encoded strings, separators).
- HTML/text cleanup: `get_pure` strips tags, consolidates whitespace/newlines.

### File & Asset Layer
**`libdev.s3`**
- Global `s3` client initialized with `cfg("s3.*")`. If credentials are absent, helpers no-op and return `None`/`[]`.
- `await upload(file, directory=cfg("mode"), bucket=cfg("project_name"), file_type=None)`:
  - `file` may be a local path, remote URL, bytes, or a file-like object.
  - Remote URLs are fetched via `aiohttp`, mime types inferred from headers/extension.
  - Returns a full URL `f"{cfg('s3.host')}{bucket}/{key}"` or `None` on errors.
- `get(directory=..., bucket=...)` lists keys under the prefix (synchronous).
- `remove(file_or_url, bucket=...)` deletes by key or URL; silently returns `None` if credentials/keys are invalid.
- Callers must ensure the event loop is running for `upload` because it can fetch remote files.

**`libdev.img`**
- `fix_rotation(image)` inspects EXIF metadata and normalizes orientation.
- `await convert(image, image_type="webp")` accepts URLs, base64 strings, bytes, or file objects. It fetches/decodes content, converts to RGB, applies rotation fix, and saves to the requested format. Returns raw bytes ready for `libdev.s3.upload` or HTTP responses.

## Example Workflow
```python
from libdev.cfg import cfg
from libdev.log import log
from libdev.req import fetch
from libdev.s3 import upload
from libdev.img import convert

API_URL = cfg("api.base")

async def sync_avatar(user_id, image_url):
    status, data = await fetch(f"{API_URL}/users/{user_id}")
    if status >= 400:
        log.json({"event": "user_fetch_failed", "user_id": user_id, "status": status, "body": data})
        return

    converted = await convert(image_url, image_type="png")
    s3_url = await upload(converted, directory="avatars", file_type="png")
    log.json({"event": "avatar_uploaded", "user_id": user_id, "url": s3_url})
```
- Note the consistent use of `cfg`, `fetch`, `convert`, `upload`, and `log.json`. This is the preferred pattern for any feature involving config, HTTP, binary assets, and logging.

## Testing & Quality Expectations
- Run `make test` inside the LibDev repo before publishing: this executes linting (`pylint` with rules in `tests/.pylintrc`) plus the full `pytest` suite under `tests/`.
- When consuming the library, write unit tests around your code, not LibDev internals. If you need to fake config values, call `set_cfg(key, value)` and restore state afterwards.

## When to Request Upstream Changes
- Adding currencies/locales/networks/status values.
- Changing numeric formatting rules or time parsing behavior.
- Enhancing validation heuristics or crypto behavior.
- Modifying S3 credential handling (because the client is created at import time).

Open an issue or pull request in https://github.com/chilleco/lib with the desired change; do not fork per-project copies of helpers.

## Quick Checklist for AI/Automation Agents
- [ ] Read config exclusively via `cfg()`/`set_cfg()`.
- [ ] Reuse `libdev.req.fetch` for HTTP; keep functions async.
- [ ] Route all logs through `libdev.log.log` (prefer `log.json`).
- [ ] Use `libdev.num`, `libdev.time`, and `libdev.lang` for formatting text shown to users.
- [ ] Use `libdev.check` before trusting phone/email/url input.
- [ ] Prefer `libdev.s3.upload` + `libdev.img.convert` for handling user files.
- [ ] Never mutate `libdev.fin` or `libdev.codes` constants at runtime.
- [ ] Run the LibDev test suite before publishing changes; pin versions when updating consumers.
