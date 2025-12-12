"""
Setup the Python package
"""

import pathlib
import re

from setuptools import find_packages, setup


WORK_DIR = pathlib.Path(__file__).parent

with open(WORK_DIR / "README.md", "r", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()


def get_version():
    """Extract version from package init."""

    txt = (WORK_DIR / "libdev" / "__init__.py").read_text("utf-8")
    match = re.search(r'^__version__ = "([^"]+)"', txt, re.M)
    if not match:
        raise RuntimeError("Unable to determine version")
    return match.group(1)


setup(
    name="libdev",
    version=get_version(),
    description="Set of standard functions for development",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/chilleco/lib",
    author="Alex Poloz",
    author_email="alexypoloz@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    keywords=(
        "standard, lib, dev, development, cfg, config, generate, codes, "
        "tokens, ids, passwords, generator, ciphers, time, formatter, nlp, "
        "natural language, aws, s3, upload file, file server"
    ),
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.10, <4",
    install_requires=[
        "aiohttp>=3.13.2",
        "python-dotenv>=1.2.1",
        "boto3>=1.42.0",
        "Pillow>=12.0.0",
        "pillow-heif>=1.0.0",
        "loguru>=0.7.3",
    ],
    project_urls={
        "Source": "https://github.com/chilleco/lib",
    },
    license="MIT",
    include_package_data=False,
)
