"""Tests for example module."""

import pytest
from unittest.mock import patch, MagicMock
import os

from omdb_api.example import get_movie_data, main


class TestGetMovieData:
    """Tests for get_movie_data function."""

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.example.requests.get")
    def test_get_movie_basic(self, mock_get):
        """Test basic movie data retrieval."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Title": "Jackie",
            "Year": "2016",
            "Response": "True"
        }
        mock_get.return_value = mock_response

        result = get_movie_data("Jackie")

        assert result["Title"] == "Jackie"
        assert result["Year"] == "2016"
        call_params = mock_get.call_args[1]["params"]
        assert call_params["t"] == "Jackie"

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.example.requests.get")
    def test_get_movie_with_year(self, mock_get):
        """Test movie data retrieval with year."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True"}
        mock_get.return_value = mock_response

        get_movie_data("Jackie", year=2016)

        call_params = mock_get.call_args[1]["params"]
        assert call_params["y"] == "2016"

    def test_empty_title(self):
        """Test that ValueError is raised for empty title."""
        with pytest.raises(ValueError, match="title must be a non-empty string"):
            get_movie_data("")

    def test_whitespace_title(self):
        """Test that ValueError is raised for whitespace title."""
        with pytest.raises(ValueError, match="title must be a non-empty string"):
            get_movie_data("   ")

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key(self):
        """Test that RuntimeError is raised when API key is not set."""
        with pytest.raises(RuntimeError, match="OMDB_API_KEY not set"):
            get_movie_data("Test")

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.example.requests.get")
    def test_year_stripped(self, mock_get):
        """Test that year is stripped if it's whitespace."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Response": "True"}
        mock_get.return_value = mock_response

        get_movie_data("Test", year="   ")

        call_params = mock_get.call_args[1]["params"]
        assert call_params["y"] is None


class TestExampleMain:
    """Tests for example.py main function."""

    @patch.dict(os.environ, {"OMDB_API_KEY": "test_key"})
    @patch("omdb_api.example.requests.get")
    def test_main_with_title(self, mock_get, capsys):
        """Test main function with movie title."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Title": "Test Movie",
            "Response": "True"
        }
        mock_get.return_value = mock_response

        exit_code = main(["Test", "Movie"])

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Test Movie" in captured.out

    def test_main_no_args(self, capsys):
        """Test main function with no arguments."""
        exit_code = main([])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_main_too_many_args(self, capsys):
        """Test main function with too many arguments."""
        exit_code = main(["arg1", "arg2", "arg3"])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Usage:" in captured.out
