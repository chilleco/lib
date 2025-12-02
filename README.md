# LibDev
Development library — Set of standard functions for development

[GitHub](https://github.com/chilleco/lib)
 | [PyPI](https://pypi.org/project/libdev/)

## Requirements
- Python 3.10+ (dependencies are 3.14-ready)

## Installation
- Runtime: `pip install .`
- Dev / tests: `pip install .[dev]` or `make setup-dev`

## Submodules
Stream | Submodule | Description
---|---|---
System | ` libdev.cfg ` | Configuration getting
&nbsp; | ` libdev.req ` | AsyncIO requests (AIOHTTP wrapper)
&nbsp; | ` libdev.log ` | Logger (Loguru wrapper)
Data Format | ` libdev.num ` | Numeric conversions & handlers
&nbsp; | ` libdev.time ` | Time processing
Transforms | ` libdev.gen ` | Code & token generators
&nbsp; | ` libdev.codes ` | Ciphers: langs & flags / networks / user statuses
&nbsp; | ` libdev.check ` | Validation functions
&nbsp; | ` libdev.crypt ` | Encryption and decryption functions
Fields | ` libdev.dev ` | Development tools
&nbsp; | ` libdev.fin ` | Financial codes and tools
&nbsp; | ` libdev.lang ` | Natural language formatters
Files | ` libdev.doc ` | Base64 / JSON handlers
&nbsp; | ` libdev.s3 ` | S3 file server functions
&nbsp; | ` libdev.img ` | Image processing
