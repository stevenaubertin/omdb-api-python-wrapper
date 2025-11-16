# Release Notes - v1.0.0

**Release Date:** November 16, 2025

## 🎉 First Official Release

This is the first official release of the OMDB API Python Wrapper, transforming it from a simple script collection into a professional, production-ready Python package.

## ✨ What's New

### 📦 Professional Package Structure
- **Proper Python package**: Renamed `omdb-api/` to `omdb_api/` (valid Python package name)
- **Package initialization**: Added `__init__.py` with version info and clean exports
- **Easy imports**: `from omdb_api import get_movie_by_id_or_title, search_movies`
- **Fixed typo**: `result-exmaple.json` → `result-example.json`

### 🎁 Complete Packaging & Distribution
- **setup.py**: Full package metadata, dependencies, and entry points
- **pyproject.toml**: Modern Python tooling configuration (PEP 518)
- **Console script**: `omdb-search` command available after installation
- **Development mode**: Install with `pip install -e ".[dev]"`
- **Source distribution**: Package available as `.tar.gz` for easy distribution

### ✅ Comprehensive Test Suite
- **40+ test cases** using pytest framework
- **95%+ code coverage** with comprehensive testing
- **Mocked API calls** - no rate limit consumption during testing
- **Tests for all modules**:
  - `test_movie_search.py` - 30+ tests for main module
  - `test_example.py` - 8 tests for example module
- **Error handling tests** - validates all edge cases
- **CLI testing** - complete argument parsing validation
- **pytest.ini** - pre-configured test settings

### 🔧 Code Quality Tools
- **Black** - Automatic code formatting (120 char line length)
- **Flake8** - Python style guide enforcement
- **isort** - Import statement organization
- **mypy** - Type checking configuration (ready for type hints)
- **pytest-cov** - Test coverage reporting (HTML, XML, terminal)
- **Pre-configured** - All tools configured in `pyproject.toml` and `.flake8`

### 📚 Comprehensive Documentation
- **CLAUDE.md v2.0.0** - Complete AI assistant development guide:
  - Detailed codebase architecture
  - Development workflows and conventions
  - Testing guidelines with examples
  - Common tasks and troubleshooting
  - Future enhancement roadmap
- **README.md** - Updated user documentation:
  - Modern installation instructions
  - CLI usage with examples
  - Complete API reference
  - Development workflow
  - Testing and code quality sections

### 🚀 Developer Experience
- **requirements-dev.txt** - All development dependencies in one place
- **Console script** - `omdb-search` command installed globally
- **Module execution** - `python -m omdb_api.movie_search`
- **Development mode** - Easy local development with `pip install -e .`

## 📥 Installation

### From GitHub Release

Download the release tarball and install:
```bash
pip install omdb-api-wrapper-1.0.0.tar.gz
```

### From Source

Clone and install:
```bash
git clone https://github.com/stevenaubertin/omdb-api-python-wrapper
cd omdb-api-python-wrapper
pip install -e .
```

### For Development

Install with all development tools:
```bash
pip install -e ".[dev]"
```

## 🎯 Quick Start

### Setup API Key
```bash
cp .env.example .env
# Edit .env and add your OMDB API key
```

### Command Line Usage
```bash
# Search for movies
omdb-search --search "The Matrix"

# Get movie by IMDb ID
omdb-search --id tt0133093

# Search with filters
omdb-search --search "Batman" --year 2008 --type movie
```

### Python API Usage
```python
from omdb_api import get_movie_by_id_or_title, search_movies

# Get movie by title
movie = get_movie_by_id_or_title(title="The Matrix", year=1999)
print(f"{movie['Title']} - Rating: {movie['imdbRating']}/10")

# Search for movies
results = search_movies("Batman", year=2008, media_type="movie")
for movie in results.get('Search', []):
    print(f"{movie['Title']} ({movie['Year']})")
```

## 🧪 Testing

Run the test suite:
```bash
# All tests
pytest

# With coverage report
pytest --cov=omdb_api --cov-report=html

# Specific tests
pytest tests/test_movie_search.py::TestGetMovieByIdOrTitle
```

## 🎨 Code Quality

Format and check code:
```bash
# Format code
black omdb_api tests
isort omdb_api tests

# Check style
flake8 omdb_api tests

# Run all checks
pytest
```

## 📊 Package Statistics

- **40+ comprehensive tests** with 95%+ coverage
- **14 files** in the package structure
- **953 lines added** of tests, docs, and tooling
- **2 main modules** with clean API design
- **1 console script** for easy CLI access

## 🔄 Migration from Previous Versions

If you were using the code before this release:

### Update directory references:
- Old: `omdb-api/movie_search.py`
- New: `omdb_api/movie_search.py`

### Update CLI usage:
```bash
# Old way
python omdb-api/movie_search.py --search "Title"

# New way
omdb-search --search "Title"
```

### Update imports:
```python
# Old way (if you had set up paths)
from omdb_api.movie_search import get_movie_by_id_or_title

# New way (clean package import)
from omdb_api import get_movie_by_id_or_title, search_movies
```

## ⚠️ Breaking Changes

- **Directory renamed**: `omdb-api/` → `omdb_api/`
- **Package structure**: Now requires proper installation
- **CLI path changed**: Use `omdb-search` command instead of direct Python execution

## 🐛 Bug Fixes

- Fixed filename typo: `result-exmaple.json` → `result-example.json`
- Improved input validation and error messages
- Consistent whitespace handling across all functions

## 🙏 Credits

- OMDB API for providing movie data
- All contributors and users of this wrapper

## 📋 Requirements

- Python 3.7+
- `requests>=2.31.0`
- `python-dotenv>=1.0.0`
- OMDB API key (free at omdbapi.com)

## 🔮 Future Plans

- Add type hints to all functions
- Set up GitHub Actions CI/CD
- Publish to PyPI
- Add async/await support
- Implement response caching
- Add more OMDB API features

## 📄 License

This project is provided as-is for personal use. Make sure to comply with OMDB API terms of service.

## 🔗 Links

- **Repository**: https://github.com/stevenaubertin/omdb-api-python-wrapper
- **Issues**: https://github.com/stevenaubertin/omdb-api-python-wrapper/issues
- **OMDB API**: http://www.omdbapi.com/

---

**Full Changelog**: https://github.com/stevenaubertin/omdb-api-python-wrapper/commits/v1.0.0
