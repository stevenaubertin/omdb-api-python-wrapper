"""Tests for movie_search module."""

import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Import the functions to test
from omdb_api.movie_search import get_movie_by_id_or_title, search_movies, main


class TestGetMovieByIdOrTitle:
    """Tests for get_movie_by_id_or_title function."""

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_get_movie_by_title(self, mock_get):
        """Test getting movie by title."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Title": "The Matrix",
            "Year": "1999",
            "Response": "True"
        }
        mock_get.return_value = mock_response

        result = get_movie_by_id_or_title(title="The Matrix")

        assert result["Title"] == "The Matrix"
        assert result["Year"] == "1999"
        mock_get.assert_called_once()
        call_params = mock_get.call_args[1]["params"]
        assert call_params["t"] == "The Matrix"
        assert call_params["apikey"] == "test_key"

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_get_movie_by_id(self, mock_get):
        """Test getting movie by IMDb ID."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Title": "The Matrix",
            "imdbID": "tt0133093",
            "Response": "True"
        }
        mock_get.return_value = mock_response

        result = get_movie_by_id_or_title(movie_id="tt0133093")

        assert result["Title"] == "The Matrix"
        assert result["imdbID"] == "tt0133093"
        call_params = mock_get.call_args[1]["params"]
        assert call_params["i"] == "tt0133093"

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_get_movie_with_year(self, mock_get):
        """Test getting movie with year parameter."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True"}
        mock_get.return_value = mock_response

        get_movie_by_id_or_title(title="Batman", year=2008)

        call_params = mock_get.call_args[1]["params"]
        assert call_params["y"] == "2008"

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_get_movie_with_plot_full(self, mock_get):
        """Test getting movie with full plot."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True"}
        mock_get.return_value = mock_response

        get_movie_by_id_or_title(title="Inception", plot="full")

        call_params = mock_get.call_args[1]["params"]
        assert call_params["plot"] == "full"

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_get_movie_with_media_type(self, mock_get):
        """Test getting movie with media type filter."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True"}
        mock_get.return_value = mock_response

        get_movie_by_id_or_title(title="Breaking Bad", media_type="series")

        call_params = mock_get.call_args[1]["params"]
        assert call_params["type"] == "series"

    def test_missing_title_and_id(self):
        """Test that ValueError is raised when both title and id are missing."""
        with pytest.raises(ValueError, match="Either 'title' or 'movie_id' must be provided"):
            get_movie_by_id_or_title()

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self):
        """Test that RuntimeError is raised when API key is not set."""
        with pytest.raises(RuntimeError, match="OMDB_API_KEY not set"):
            get_movie_by_id_or_title(title="Test")

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    def test_empty_title(self):
        """Test that ValueError is raised for empty title."""
        with pytest.raises(ValueError, match="title must be a non-empty string"):
            get_movie_by_id_or_title(title="   ")

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    def test_empty_movie_id(self):
        """Test that ValueError is raised for empty movie_id."""
        with pytest.raises(ValueError, match="movie_id must be a non-empty string"):
            get_movie_by_id_or_title(movie_id="   ")

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    def test_invalid_media_type(self):
        """Test that ValueError is raised for invalid media_type."""
        with pytest.raises(ValueError, match="media_type must be one of"):
            get_movie_by_id_or_title(title="Test", media_type="invalid")

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_whitespace_trimming(self, mock_get):
        """Test that whitespace is trimmed from inputs."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True"}
        mock_get.return_value = mock_response

        get_movie_by_id_or_title(title="  The Matrix  ", year="  1999  ")

        call_params = mock_get.call_args[1]["params"]
        assert call_params["t"] == "The Matrix"
        assert call_params["y"] == "1999"


class TestSearchMovies:
    """Tests for search_movies function."""

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_basic_search(self, mock_get):
        """Test basic movie search."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Search": [
                {"Title": "Batman Begins", "Year": "2005"},
                {"Title": "The Dark Knight", "Year": "2008"}
            ],
            "totalResults": "2",
            "Response": "True"
        }
        mock_get.return_value = mock_response

        result = search_movies("Batman")

        assert result["Response"] == "True"
        assert len(result["Search"]) == 2
        call_params = mock_get.call_args[1]["params"]
        assert call_params["s"] == "Batman"

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_search_with_year(self, mock_get):
        """Test search with year filter."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True", "Search": []}
        mock_get.return_value = mock_response

        search_movies("Batman", year=2008)

        call_params = mock_get.call_args[1]["params"]
        assert call_params["y"] == "2008"

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_search_with_media_type(self, mock_get):
        """Test search with media type filter."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True", "Search": []}
        mock_get.return_value = mock_response

        search_movies("Star Trek", media_type="series")

        call_params = mock_get.call_args[1]["params"]
        assert call_params["type"] == "series"

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_search_with_page(self, mock_get):
        """Test search with pagination."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True", "Search": []}
        mock_get.return_value = mock_response

        search_movies("The", page=2)

        call_params = mock_get.call_args[1]["params"]
        assert call_params["page"] == "2"

    def test_empty_search_query(self):
        """Test that ValueError is raised for empty search query."""
        with pytest.raises(ValueError, match="search_query must be a non-empty string"):
            search_movies("")

    def test_whitespace_search_query(self):
        """Test that ValueError is raised for whitespace-only search query."""
        with pytest.raises(ValueError, match="search_query must be a non-empty string"):
            search_movies("   ")

    @patch.dict(os.environ, {}, clear=True)
    def test_search_missing_api_key(self):
        """Test that RuntimeError is raised when API key is not set."""
        with pytest.raises(RuntimeError, match="OMDB_API_KEY not set"):
            search_movies("Test")

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    def test_invalid_page_number(self):
        """Test that ValueError is raised for invalid page numbers."""
        with pytest.raises(ValueError, match="page must be between 1 and 100"):
            search_movies("Test", page=0)

        with pytest.raises(ValueError, match="page must be between 1 and 100"):
            search_movies("Test", page=101)

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    def test_invalid_page_type(self):
        """Test that ValueError is raised for invalid page type."""
        with pytest.raises(ValueError, match="page must be a valid integer"):
            search_movies("Test", page="invalid")

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    def test_search_invalid_media_type(self):
        """Test that ValueError is raised for invalid media_type."""
        with pytest.raises(ValueError, match="media_type must be one of"):
            search_movies("Test", media_type="invalid")


class TestMain:
    """Tests for main CLI function."""

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_search_mode(self, mock_get, capsys):
        """Test CLI search mode."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Title": "The Matrix",
            "Response": "True"
        }
        mock_get.return_value = mock_response

        exit_code = main(["--search", "The Matrix"])

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "The Matrix" in captured.out

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_id_mode(self, mock_get, capsys):
        """Test CLI ID mode."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "imdbID": "tt0133093",
            "Response": "True"
        }
        mock_get.return_value = mock_response

        exit_code = main(["--id", "tt0133093"])

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "tt0133093" in captured.out

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_legacy_mode(self, mock_get, capsys):
        """Test CLI legacy mode (positional arguments)."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Title": "Inception",
            "Response": "True"
        }
        mock_get.return_value = mock_response

        exit_code = main(["Inception", "2010"])

        assert exit_code == 0

    def test_no_arguments(self, capsys):
        """Test CLI with no arguments shows usage."""
        exit_code = main([])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    def test_error_handling(self, capsys):
        """Test CLI error handling."""
        exit_code = main(["--search", ""])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.movie_search.requests.get")
    def test_all_options(self, mock_get, capsys):
        """Test CLI with all options."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True", "Search": []}
        mock_get.return_value = mock_response

        exit_code = main(["--search", "Batman", "--year", "2008",
                         "--type", "movie", "--page", "1"])

        assert exit_code == 0
