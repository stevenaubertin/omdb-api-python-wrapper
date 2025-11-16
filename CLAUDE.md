# CLAUDE.md - AI Assistant Guide for OMDB API Python Wrapper

This document provides comprehensive guidance for AI assistants working with the OMDB API Python Wrapper codebase.

## Project Overview

**Purpose:** A Python library for interacting with the OMDB (Open Movie Database) API. Enables searching for movies by title or IMDb ID, retrieving detailed movie information, and integrating movie data into Python applications.

**Language:** Python 3.7+

**Dependencies:**
- `requests>=2.31.0` - HTTP library for API calls
- `python-dotenv>=1.0.0` - Environment variable management

**External API:** OMDB API (http://www.omdbapi.com/)
- Requires API key (free tier: 1,000 requests/day)
- Get key at: http://www.omdbapi.com/apikey.aspx

## Repository Structure

```
omdb-api-python-wrapper/
├── omdb-api/
│   ├── movie_search.py      # Primary module: comprehensive API wrapper
│   ├── example.py            # Simple example: basic movie lookup
│   └── result-exmaple.json   # Sample API response (note: typo in filename)
├── .env                      # API key storage (git-ignored, user creates)
├── .env.example              # Template for .env file
├── .gitignore                # Standard Python gitignore
├── requirements.txt          # Python dependencies
├── README.md                 # User-facing documentation
└── CLAUDE.md                 # This file - AI assistant guide
```

## Code Architecture

### Primary Module: `omdb-api/movie_search.py`

**Core Functions:**

1. **`get_movie_by_id_or_title(title=None, movie_id=None, year=None, plot="short", media_type=None)`**
   - Location: movie_search.py:12-68
   - Purpose: Fetch detailed movie data by title or IMDb ID
   - Returns: Dict with full movie metadata
   - Parameters:
     - `title` (str, optional): Movie title
     - `movie_id` (str, optional): IMDb ID (e.g., "tt0133093")
     - `year` (int/str, optional): Release year filter
     - `plot` (str): "short" or "full" plot length
     - `media_type` (str, optional): "movie", "series", or "episode"
   - Validation:
     - Requires either `title` OR `movie_id` (not both required, but at least one)
     - Strips whitespace from all string inputs
     - Validates `media_type` is in allowed list
     - Raises `ValueError` for invalid inputs
     - Raises `RuntimeError` if `OMDB_API_KEY` not set

2. **`search_movies(search_query, year=None, media_type=None, page=1)`**
   - Location: movie_search.py:71-127
   - Purpose: Search for multiple movies by title
   - Returns: Dict with search results array
   - Parameters:
     - `search_query` (str): Search term (required)
     - `year` (int/str, optional): Filter by release year
     - `media_type` (str, optional): "movie", "series", or "episode"
     - `page` (int): Results page (1-100, default: 1)
   - Validation:
     - Strips whitespace from search_query
     - Validates page is 1-100
     - Same media_type validation as above

3. **`main(argv)`**
   - Location: movie_search.py:130-241
   - Purpose: CLI interface with argument parsing
   - Supports three modes:
     - Search mode: `--search "Title" [--year YEAR] [--type TYPE] [--page PAGE]`
     - ID mode: `--id tt1234567 [--plot full]`
     - Legacy mode: `"Title" [YEAR]` (positional arguments)

### Secondary Module: `omdb-api/example.py`

**Core Function:**

1. **`get_movie_data(title, year=None)`**
   - Location: example.py:11-40
   - Purpose: Simplified movie lookup (title only)
   - Simpler interface than movie_search.py
   - Similar validation pattern

### Environment Configuration

- **API Key Storage:** Uses `.env` file with `OMDB_API_KEY` variable
- **Loading:** `python-dotenv` loads environment variables at module import
- **Security:** `.env` is git-ignored to prevent key exposure

## Key Conventions and Patterns

### Code Style

1. **Input Validation:**
   - All string inputs are stripped of whitespace
   - Empty strings treated as missing values
   - Explicit type conversion (str(), int()) before validation
   - Raise `ValueError` for invalid inputs, `RuntimeError` for configuration issues

2. **API Interaction:**
   - Base URL: `http://www.omdbapi.com/`
   - All requests use `requests.get()` with params dict
   - Response format: JSON (specified via `r=json` parameter)
   - No error handling for network failures (requests exceptions propagate)

3. **Parameter Naming:**
   - Internal Python: snake_case (e.g., `movie_id`, `media_type`)
   - OMDB API: single letter params (e.g., `i`, `t`, `y`, `type`)
   - Mapping in params dict construction

4. **Documentation:**
   - All functions have comprehensive docstrings
   - Google-style docstring format
   - Includes Args, Returns, Raises sections

### Naming Conventions

- **Functions:** snake_case verbs (e.g., `get_movie_data`, `search_movies`)
- **Variables:** snake_case descriptive names
- **Constants:** UPPER_SNAKE_CASE (e.g., `OMDB_API_KEY`, `BASE_URL`)

### Error Handling Philosophy

- **Validation:** Fail fast with clear error messages
- **Network:** Let requests library exceptions propagate
- **API Errors:** Return OMDB error responses as-is (dict with `Response: "False"`)

## Development Workflows

### Initial Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd omdb-api-python-wrapper

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and add your OMDB API key

# 4. Test installation
python omdb-api/movie_search.py --search "The Matrix"
```

### Making Changes

**When modifying existing code:**
1. Read the existing implementation first
2. Maintain consistent validation patterns
3. Update docstrings if function signatures change
4. Test both success and error cases manually

**When adding new features:**
1. Follow existing code style and patterns
2. Add comprehensive docstrings
3. Implement input validation following existing patterns
4. Update README.md with new functionality

### Git Workflow

**Branch Naming:**
- Feature branches: `claude/claude-md-<session-id>`
- Always develop on designated feature branch
- Never push directly to main/master

**Commit Messages:**
- Use descriptive, concise messages
- Format: `<type>: <description>`
- Examples:
  - `feat: Add support for episode lookups`
  - `fix: Handle empty search queries correctly`
  - `docs: Update API reference in README`

**Pushing Changes:**
```bash
git add <files>
git commit -m "descriptive message"
git push -u origin <branch-name>
```

## Testing Guidelines

### Current State

**⚠️ IMPORTANT:** This repository currently has **NO automated tests**.

### Manual Testing Checklist

When making changes, manually test:

1. **Basic functionality:**
   ```bash
   # Test search by title
   python omdb-api/movie_search.py --search "The Matrix"

   # Test search by ID
   python omdb-api/movie_search.py --id tt0133093

   # Test with filters
   python omdb-api/movie_search.py --search "Batman" --year 2008 --type movie
   ```

2. **Error cases:**
   ```bash
   # Missing API key (temporarily rename .env)
   python omdb-api/movie_search.py --search "Test"

   # Empty search query
   python omdb-api/movie_search.py --search ""

   # Invalid page number
   python omdb-api/movie_search.py --search "Test" --page 101
   ```

3. **Module import:**
   ```python
   # Test Python API
   from omdb_api.movie_search import get_movie_by_id_or_title, search_movies
   movie = get_movie_by_id_or_title(title="Inception")
   print(movie)
   ```

### Future Testing Recommendations

If adding tests, consider:
- **Framework:** pytest
- **Coverage:** unittest.mock for requests
- **Structure:** Create `tests/` directory
- **Files:** `test_movie_search.py`, `test_example.py`

## Common Tasks

### Task: Add New API Parameter

**Example:** Add support for `tomatoes` parameter (Rotten Tomatoes ratings)

1. **Update function signature** (movie_search.py):
   ```python
   def get_movie_by_id_or_title(title=None, movie_id=None, year=None,
                                 plot="short", media_type=None, tomatoes=False):
   ```

2. **Add parameter to params dict**:
   ```python
   if tomatoes:
       params["tomatoes"] = "true"
   ```

3. **Update docstring** with new parameter

4. **Update README.md** with usage example

5. **Test manually** with and without the parameter

### Task: Improve Error Handling

**Example:** Add retry logic for network failures

1. Consider if it aligns with current "let exceptions propagate" philosophy
2. If adding retries, use a library like `tenacity` or `backoff`
3. Add to requirements.txt
4. Document retry behavior in docstrings

### Task: Add New Search Function

**Example:** Add `get_movie_by_title_exact()` for exact title matches

1. Follow existing function pattern in movie_search.py
2. Add comprehensive docstring
3. Implement validation following existing patterns
4. Add to `main()` CLI interface if applicable
5. Update README.md API Reference section

## Important Notes for AI Assistants

### Critical Considerations

1. **API Key Security:**
   - NEVER hardcode API keys in code
   - NEVER commit `.env` file
   - Always use environment variables
   - Recommend `.env.example` for templates

2. **OMDB API Limitations:**
   - Free tier: 1,000 requests/day
   - Respect rate limits
   - Consider caching for repeated queries (not currently implemented)

3. **Input Validation:**
   - Always strip whitespace from string inputs
   - Validate before making API calls
   - Provide clear, actionable error messages

4. **Backward Compatibility:**
   - `example.py` uses simpler interface than `movie_search.py`
   - Both modules should remain functional
   - Don't break existing CLI usage patterns

5. **Documentation:**
   - Keep README.md in sync with code changes
   - Update docstrings when modifying functions
   - Maintain example.py as a simple reference

### Common Pitfalls to Avoid

1. **Don't assume movie exists:**
   - Always check `Response` field in API response
   - Handle `Response: "False"` gracefully

2. **Don't modify global state:**
   - Keep functions pure where possible
   - Don't cache API key in mutable globals

3. **Don't add unnecessary dependencies:**
   - Keep dependencies minimal
   - Only add if genuinely needed

4. **Don't break CLI interface:**
   - Maintain backward compatibility for existing usage patterns
   - Support legacy mode (positional args)

### Code Quality Standards

1. **Type hints:** Not currently used, but would be beneficial to add
2. **Docstrings:** Comprehensive Google-style required
3. **Line length:** No strict limit, but keep reasonable (<120 chars preferred)
4. **Imports:** Standard library, then third-party, then local

### When to Ask for Clarification

1. **Breaking changes:** If modification would break existing usage
2. **New dependencies:** Before adding new libraries
3. **Architecture changes:** Before major refactoring
4. **API changes:** If OMDB API parameter behavior is unclear

## API Integration Details

### OMDB API Endpoints Used

**Get by Title/ID:**
- Parameters: `t` (title) OR `i` (IMDb ID), `y` (year), `plot`, `type`, `apikey`
- Returns: Single movie object

**Search:**
- Parameters: `s` (search query), `y` (year), `type`, `page`, `apikey`
- Returns: Object with `Search` array and `totalResults`

### Response Structure

**Success Response:**
```json
{
  "Title": "Movie Title",
  "Year": "2020",
  "imdbRating": "8.5",
  "Response": "True",
  ...
}
```

**Error Response:**
```json
{
  "Response": "False",
  "Error": "Movie not found!"
}
```

**Search Response:**
```json
{
  "Search": [
    {"Title": "...", "Year": "...", "imdbID": "...", ...}
  ],
  "totalResults": "123",
  "Response": "True"
}
```

### Known API Quirks

1. **Year parameter:** Can be a single year or range (e.g., "2000-2010")
2. **Type parameter:** "movie", "series", or "episode" (lowercase)
3. **Page limits:** Maximum 100 pages for search results
4. **Plot parameter:** "short" or "full" (affects response size)

## Troubleshooting and Common Issues

### Issue: "OMDB_API_KEY not set in environment"

**Cause:** `.env` file missing or incorrectly configured

**Solution:**
```bash
cp .env.example .env
# Edit .env and add your API key:
# OMDB_API_KEY=your_actual_key_here
```

### Issue: Response "False" with "Movie not found!"

**Cause:** Movie doesn't exist in OMDB database or title is misspelled

**Solution:**
- Try IMDb ID instead of title
- Check spelling and year
- Search first, then get details with exact title/ID

### Issue: ImportError when using as module

**Cause:** Module not in Python path

**Solution:**
```python
# Add parent directory to path
import sys
sys.path.insert(0, '/path/to/omdb-api-python-wrapper')
from omdb_api.movie_search import get_movie_by_id_or_title
```

Or install as package (requires setup.py, not yet implemented).

### Issue: Rate limit exceeded

**Cause:** Exceeded 1,000 daily requests on free tier

**Solution:**
- Wait 24 hours for reset
- Consider upgrading API plan
- Implement local caching (not currently in codebase)

## Future Enhancements to Consider

### High Priority

1. **Automated Testing:**
   - Add pytest suite
   - Mock API calls
   - Test error handling

2. **Packaging:**
   - Add setup.py or pyproject.toml
   - Enable pip installation
   - Publish to PyPI

3. **Type Hints:**
   - Add type annotations
   - Enable mypy checking

### Medium Priority

1. **Caching:**
   - Implement response caching
   - Reduce API calls
   - Use Redis or local file cache

2. **Async Support:**
   - Add async/await functions
   - Support concurrent requests
   - Use aiohttp or httpx

3. **Better Error Handling:**
   - Custom exception classes
   - Retry logic with exponential backoff
   - Detailed error messages

### Low Priority

1. **Additional Features:**
   - Batch operations
   - Export to CSV/JSON
   - Rating aggregation utilities

2. **Documentation:**
   - Add examples directory
   - Create Sphinx docs
   - Add tutorials

3. **CI/CD:**
   - GitHub Actions workflow
   - Automated testing
   - Code quality checks (flake8, black)

## File Reference Quick Guide

| File | Purpose | Key Functions |
|------|---------|---------------|
| `omdb-api/movie_search.py` | Primary API wrapper | `get_movie_by_id_or_title()`, `search_movies()`, `main()` |
| `omdb-api/example.py` | Simple example | `get_movie_data()` |
| `omdb-api/result-exmaple.json` | Sample response | N/A (data file) |
| `.env.example` | API key template | N/A (config) |
| `requirements.txt` | Dependencies | N/A (config) |
| `README.md` | User documentation | N/A (docs) |

## Version History

- **Initial Commit** (e3e10d0): OMDB API Python wrapper
  - Core functionality implemented
  - Two modules: movie_search.py and example.py
  - CLI interface
  - Comprehensive README

---

**Last Updated:** 2025-11-16

**Document Version:** 1.0.0

**For Questions:** Refer to README.md for user documentation, this file for development guidance.
