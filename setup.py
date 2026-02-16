"""
Mythos Programming Language Setup
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mythos-lang",
    version="1.0.0",
    author="Mythos Team",
    author_email="team@mythos-lang.org",
    description="A powerful, expressive programming language for building anything",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mythos-lang/mythos",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
        "web": [
            "aiohttp>=3.8",
        ],
        "graphics": [
            "pygame>=2.0",
            "PyOpenGL>=3.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "mythos=mythos_cli.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
