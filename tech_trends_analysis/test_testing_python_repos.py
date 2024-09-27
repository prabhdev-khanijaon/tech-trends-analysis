import requests
import plotly.express as px
import pytest


def python_repos_status_code() :
    """Get the status code of the github API call."""
    # Make an API call and check the response.
    url = "https://api.github.com/search/repositories"
    url += "?q=language:python+sort:stars+stars:>10000"

    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    return r.status_code


def test_python_repos_status_code() :
    """Test the status code of the python repos github API call."""
    x = python_repos_status_code()
    assert x == 200


def python_repos_fn() :
    """Make an API call, get a response, and create a dictionary from
    the response."""
    # Make an API call and check the response.
    url = "https://api.github.com/search/repositories"
    url += "?q=language:python+sort:stars+stars:>10000"

    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    # Convert the response object to a dictionary.
    response_dict = r.json()

    # Explore information about the repositories.
    repo_dicts = response_dict['items']
    return repo_dicts


def test_total_repository_count() :
    """Test if the length of the python repos dictionary is greater than 20."""
    repos_len = python_repos_fn()
    assert len(repos_len) > 20