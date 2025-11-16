"""Setup configuration for OMDB API Python Wrapper."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="omdb-api-wrapper",
    version="1.0.0",
    author="OMDB API Wrapper Contributors",
    description="A Python library for interacting with the OMDB (Open Movie Database) API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stevenaubertin/omdb-api-python-wrapper",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "omdb-search=omdb_api.movie_search:main",
        ],
    },
    keywords="omdb api movie imdb search wrapper",
    project_urls={
        "Bug Reports": "https://github.com/stevenaubertin/omdb-api-python-wrapper/issues",
        "Source": "https://github.com/stevenaubertin/omdb-api-python-wrapper",
    },
)
