# OMDB API - Python Wrapper

A Python library for interacting with the OMDB (Open Movie Database) API. Search for movies, get detailed information, and easily integrate movie data into your Python applications.

## Features

- Search movies by title or IMDb ID
- Filter by year and media type (movie, series, episode)
- Get detailed movie information including ratings, plot, and metadata
- Paginated search results
- Command-line interface for quick lookups
- Easy-to-use Python API
- Type hints and comprehensive error handling

## Requirements

- Python 3.7+
- `requests` library
- `python-dotenv` library
- OMDB API key (free at [omdbapi.com](http://www.omdbapi.com/))

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd omdb-api
   ```

2. Install dependencies:
   ```bash
   pip install requests python-dotenv
   ```

3. Create a `.env` file in the project root with your OMDB API key:
   ```env
   OMDB_API_KEY=your_api_key_here
   ```

   Get a free API key at [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)

## Usage

### As a Python Module

```python
from omdb_api.movie_search import get_movie_by_id_or_title, search_movies

# Get movie by title
movie = get_movie_by_id_or_title(title="The Matrix", year=1999)
print(f"{movie['Title']} - Rating: {movie['imdbRating']}/10")

# Get movie by IMDb ID
movie = get_movie_by_id_or_title(movie_id="tt0133093")
print(f"Plot: {movie['Plot']}")

# Search for multiple movies
results = search_movies("Batman", year=2008, media_type="movie", page=1)
if results.get('Response') == 'True':
    for movie in results.get('Search', []):
        print(f"{movie['Title']} ({movie['Year']})")
```

### Command Line Interface

```bash
# Search by title
python omdb-api/movie_search.py --search "The Matrix" --year 1999

# Get movie by IMDb ID
python omdb-api/movie_search.py --id tt0133093

# Search with filters
python omdb-api/movie_search.py --search "Batman" --type movie --year 2008

# Get full plot
python omdb-api/movie_search.py --id tt0133093 --plot full

# Legacy mode (simple title search)
python omdb-api/movie_search.py "The Matrix" 1999
```

### Example Response

```json
{
  "Title": "The Matrix",
  "Year": "1999",
  "Rated": "R",
  "Released": "31 Mar 1999",
  "Runtime": "136 min",
  "Genre": "Action, Sci-Fi",
  "Director": "Lana Wachowski, Lilly Wachowski",
  "Writer": "Lilly Wachowski, Lana Wachowski",
  "Actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
  "Plot": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
  "Language": "English",
  "Country": "United States, Australia",
  "Awards": "Won 4 Oscars. 42 wins & 52 nominations total",
  "Poster": "https://m.media-amazon.com/images/M/...",
  "Ratings": [...],
  "Metascore": "73",
  "imdbRating": "8.7",
  "imdbVotes": "1,900,000",
  "imdbID": "tt0133093",
  "Type": "movie",
  "DVD": "21 Sep 1999",
  "BoxOffice": "$172,076,928",
  "Production": "N/A",
  "Website": "N/A",
  "Response": "True"
}
```

## API Reference

### `get_movie_by_id_or_title(title=None, movie_id=None, year=None, plot="short", media_type=None)`

Fetch movie data from OMDB API by ID or title.

**Parameters:**
- `title` (str, optional): Movie title to search for
- `movie_id` (str, optional): IMDb ID (e.g., "tt1285016")
- `year` (int/str, optional): Year of release
- `plot` (str): "short" or "full" plot (default: "short")
- `media_type` (str, optional): "movie", "series", or "episode"

**Returns:** Dictionary with movie data

**Raises:**
- `ValueError`: If neither title nor movie_id is provided
- `RuntimeError`: If OMDB_API_KEY is not set

**Example:**
```python
# By title
movie = get_movie_by_id_or_title(title="Inception", year=2010)

# By IMDb ID
movie = get_movie_by_id_or_title(movie_id="tt1375666")

# With full plot
movie = get_movie_by_id_or_title(title="Inception", plot="full")

# Filter by type
series = get_movie_by_id_or_title(title="Breaking Bad", media_type="series")
```

### `search_movies(search_query, year=None, media_type=None, page=1)`

Search for movies by title.

**Parameters:**
- `search_query` (str): Movie title to search for
- `year` (int/str, optional): Year of release
- `media_type` (str, optional): "movie", "series", or "episode"
- `page` (int): Page number (1-100, default: 1)

**Returns:** Dictionary with search results containing a list of movies

**Raises:**
- `ValueError`: If search_query is empty or page is out of range
- `RuntimeError`: If OMDB_API_KEY is not set

**Example:**
```python
# Basic search
results = search_movies("Star Wars")

# Filter by year and type
results = search_movies("Batman", year=2008, media_type="movie")

# Paginated results
results = search_movies("The", page=2)

# Process results
if results.get('Response') == 'True':
    for movie in results['Search']:
        print(f"{movie['Title']} ({movie['Year']}) - {movie['imdbID']}")
    print(f"Total results: {results['totalResults']}")
```

## Project Structure

```
omdb-api/
├── omdb-api/
│   ├── movie_search.py    # Main OMDB API wrapper
│   └── example.py          # Simple usage example
├── .env.example           # Environment variable template
├── .env                   # Your API key (create this, not tracked by git)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Troubleshooting

### "OMDB_API_KEY not set in environment"
Make sure you have a `.env` file in the project root with your API key:
```env
OMDB_API_KEY=your_api_key_here
```

You can copy `.env.example` to `.env` and add your key.

### "Response": "False" in results
This usually means:
1. The movie/title wasn't found in OMDB
2. Your API key is invalid or has exceeded its daily limit
3. The search parameters are too restrictive

Check the `"Error"` field in the response for more details.

### Import errors
Make sure you've installed the required dependencies:
```bash
pip install requests python-dotenv
```

## OMDB API Limits

The free OMDB API key has a daily limit of 1,000 requests. For higher limits, consider upgrading at [omdbapi.com](http://www.omdbapi.com/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for personal use. Make sure to comply with OMDB API terms of service.

## Acknowledgments

- [OMDB API](http://www.omdbapi.com/) for providing movie data
- Inspired by the need for a simple Python wrapper for movie information
