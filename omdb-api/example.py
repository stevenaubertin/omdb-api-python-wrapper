import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"


def get_movie_data(title, year=None):
    """Fetch movie data from OMDB API by title and optional year.

    Args:
        title (str): Movie title to search for.
        year (Optional[int|str]): Year of release (optional).

    Returns:
        dict: Parsed JSON response from OMDB.
    """
    if not title or not str(title).strip():
        raise ValueError("title must be a non-empty string")
    title = str(title).strip()

    if year is not None:
        year = str(year).strip()
        if year == "":
            year = None

    if not OMDB_API_KEY:
        raise RuntimeError("OMDB_API_KEY not set in environment")
    params = {
        "t": title,
        "y": year,
        "r": "json",
        "plot": "short",
        "apikey": OMDB_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()


def main(argv):
    if len(argv) > 2 or len(argv) < 1:
        print("Usage: python example.py <movie_title> [year]")
        return 1

    movie_title = " ".join(argv)
    movie_data = get_movie_data(movie_title)
    print(movie_data)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))