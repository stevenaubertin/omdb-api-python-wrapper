import requests
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"


def get_movie_by_id_or_title(title=None, movie_id=None, year=None, plot="short", media_type=None):
    """Fetch movie data from OMDB API by ID or title.

    Args:
        title (Optional[str]): Movie title to search for.
        movie_id (Optional[str]): A valid IMDb ID (e.g. tt1285016).
        year (Optional[int|str]): Year of release (optional).
        plot (str): Return short or full plot. Options: 'short' (default), 'full'.
        media_type (Optional[str]): Type of result to return. Options: 'movie', 'series', 'episode'.

    Returns:
        dict: Parsed JSON response from OMDB.

    Raises:
        ValueError: If neither title nor movie_id is provided, or if both are invalid.
        RuntimeError: If OMDB_API_KEY is not set.
    """
    if not movie_id and not title:
        raise ValueError("Either 'title' or 'movie_id' must be provided")

    if not OMDB_API_KEY:
        raise RuntimeError("OMDB_API_KEY not set in environment")

    params = {
        "r": "json",
        "plot": plot,
        "apikey": OMDB_API_KEY
    }

    # Use ID if provided, otherwise use title
    if movie_id:
        movie_id = str(movie_id).strip()
        if movie_id:
            params["i"] = movie_id
        else:
            raise ValueError("movie_id must be a non-empty string")
    else:
        title = str(title).strip()
        if not title:
            raise ValueError("title must be a non-empty string")
        params["t"] = title

    # Add optional parameters
    if year is not None:
        year = str(year).strip()
        if year:
            params["y"] = year

    if media_type:
        media_type = str(media_type).strip().lower()
        if media_type in ["movie", "series", "episode"]:
            params["type"] = media_type
        else:
            raise ValueError("media_type must be one of: 'movie', 'series', 'episode'")

    response = requests.get(BASE_URL, params=params)
    return response.json()


def search_movies(search_query, year=None, media_type=None, page=1):
    """Search for movies by title using OMDB API.

    Args:
        search_query (str): Movie title to search for (required).
        year (Optional[int|str]): Year of release (optional).
        media_type (Optional[str]): Type of result to return. Options: 'movie', 'series', 'episode'.
        page (int): Page number to return (1-100). Default: 1.

    Returns:
        dict: Parsed JSON response from OMDB containing search results.

    Raises:
        ValueError: If search_query is empty or invalid.
        RuntimeError: If OMDB_API_KEY is not set.
    """
    if not search_query:
        raise ValueError("search_query must be a non-empty string")

    search_query = str(search_query).strip()
    if not search_query:
        raise ValueError("search_query must be a non-empty string")

    if not OMDB_API_KEY:
        raise RuntimeError("OMDB_API_KEY not set in environment")

    params = {
        "s": search_query,
        "r": "json",
        "apikey": OMDB_API_KEY
    }

    # Add optional parameters
    if year is not None:
        year = str(year).strip()
        if year:
            params["y"] = year

    if media_type:
        media_type = str(media_type).strip().lower()
        if media_type in ["movie", "series", "episode"]:
            params["type"] = media_type
        else:
            raise ValueError("media_type must be one of: 'movie', 'series', 'episode'")

    if page is not None:
        try:
            page = int(page)
            if 1 <= page <= 100:
                params["page"] = str(page)
            else:
                raise ValueError("page must be between 1 and 100")
        except (ValueError, TypeError):
            raise ValueError("page must be a valid integer between 1 and 100")

    response = requests.get(BASE_URL, params=params)
    return response.json()


def main(argv):
    """Main entry point for command-line usage.

    Usage:
        python movie_search.py --search "Movie Title" [--year YEAR] [--type TYPE] [--page PAGE]
        python movie_search.py --id tt1285016 [--year YEAR] [--type TYPE] [--plot full]
        python movie_search.py "Movie Title" [YEAR]  (legacy mode: search by title)
    """
    if len(argv) == 0:
        print("Usage:")
        print("  Search mode: python movie_search.py --search 'Movie Title' [--year YEAR] [--type TYPE] [--page PAGE]")
        print("  ID mode:     python movie_search.py --id tt1285016 [--year YEAR] [--type TYPE] [--plot full]")
        print("  Legacy mode: python movie_search.py 'Movie Title' [YEAR]")
        return 1

    # Parse arguments
    args = {
        'search_query': None,
        'movie_id': None,
        'year': None,
        'media_type': None,
        'plot': 'short',
        'page': 1,
    }

    i = 0
    while i < len(argv):
        arg = argv[i]

        if arg in ['--search', '-s']:
            i += 1
            if i < len(argv):
                args['search_query'] = argv[i]
        elif arg in ['--id', '-i']:
            i += 1
            if i < len(argv):
                args['movie_id'] = argv[i]
        elif arg in ['--year', '-y']:
            i += 1
            if i < len(argv):
                args['year'] = argv[i]
        elif arg in ['--type', '-t']:
            i += 1
            if i < len(argv):
                args['media_type'] = argv[i]
        elif arg in ['--plot', '-p']:
            i += 1
            if i < len(argv):
                args['plot'] = argv[i]
        elif arg in ['--page']:
            i += 1
            if i < len(argv):
                args['page'] = argv[i]
        elif arg.startswith('--'):
            print(f"Unknown option: {arg}")
            return 1
        else:
            # Legacy mode: first positional argument is the title
            if args['search_query'] is None and args['movie_id'] is None:
                args['search_query'] = arg
            # Second positional argument is the year
            elif args['year'] is None:
                args['year'] = arg

        i += 1

    # Execute the appropriate function
    try:
        if args['movie_id']:
            # Search by ID or title
            result = get_movie_by_id_or_title(
                title=args['search_query'],
                movie_id=args['movie_id'],
                year=args['year'],
                plot=args['plot'],
                media_type=args['media_type']
            )
        elif args['search_query']:
            # Determine if it's a search or direct lookup
            # If only search_query is provided and no year, try as direct lookup first
            if args['year'] is None and not args['media_type'] and args['page'] == 1:
                result = get_movie_by_id_or_title(
                    title=args['search_query'],
                    year=args['year'],
                    plot=args['plot'],
                    media_type=args['media_type']
                )
            else:
                # Use search mode
                result = search_movies(
                    search_query=args['search_query'],
                    year=args['year'],
                    media_type=args['media_type'],
                    page=args['page']
                )
        else:
            print("Error: No movie title or ID provided")
            return 1

        print(json.dumps(result, indent=2))
        return 0

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
