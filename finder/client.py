"""
Client for Arctic Shift API interactions.
"""
import requests
from typing import List, Dict, Any


class ArcticShiftClient:
    """
    Wrapper around Arctic Shift API endpoints.
    """
    BASE_URL = "https://arctic-shift.photon-reddit.com/api"

    def search_subreddits(self, keyword: str, limit: int) -> List[Dict[str, Any]]:
        """
        Search for subreddits by prefix.

        :param keyword: Keyword to search.
        :param limit: Max number of results.
        :return: List of subreddit dictionaries.
        """
        url = f"{self.BASE_URL}/subreddits/search"
        params = {"subreddit_prefix": keyword, "limit": limit}

        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            return data["data"] if isinstance(data, dict) and "data" in data else data
        except requests.exceptions.HTTPError as e:
            print(f"[!] Failed to fetch subreddits for keyword: '{keyword}'")
            print(f"    URL: {resp.url}")
            print(f"    Status Code: {resp.status_code}")
            print(f"    Message: {resp.text}")
            return []  # Fail silently with an empty list

    def get_top_posts(self, subreddit: str, limit: int) -> List[Dict[str, Any]]:
        """
        Get top posts from a subreddit using Arctic Shift API.

        :param subreddit: Name of the subreddit.
        :param limit: Number of posts to return.
        :return: List of post dicts.
        """
        url = f"{self.BASE_URL}/posts/search"
        params = {
            "subreddit": subreddit,
            "limit": limit
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()["data"]  # Arctic Shift returns a 'data' key
