#!/usr/bin/env python3
"""
Setup script for Local Doc-Whisperer
Makes the CLI tool installable via pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="local-doc-whisperer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tiny Python CLI that digests documents with Claude AI and stores them in a local vector database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/local-doc-whisperer",
    py_modules=["main"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Education",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "doc-whisperer=main:app",
        ],
    },
    keywords="ai claude anthropic vector-database pdf text-analysis knowledge-base rag",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/local-doc-whisperer/issues",
        "Source": "https://github.com/yourusername/local-doc-whisperer",
    },
) 