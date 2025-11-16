"""OMDB API Python Wrapper - A library for interacting with the OMDB API.

This package provides functions to search for movies and retrieve detailed
information from the Open Movie Database (OMDB) API.
"""

__version__ = "1.0.0"
__author__ = "OMDB API Wrapper Contributors"

from .movie_search import get_movie_by_id_or_title, search_movies

__all__ = ["get_movie_by_id_or_title", "search_movies"]
