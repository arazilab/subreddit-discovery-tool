"""Client for Arctic Shift API interactions."""
from typing import List, Dict, Any

import requests


class ArcticShiftClient:
    """
    Wrapper around Arctic Shift API endpoints.
    """
    BASE_URL = "https://arctic-shift.photon-reddit.com/api"
    TIMEOUT_SECONDS = 30

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
            resp = requests.get(url, params=params, timeout=self.TIMEOUT_SECONDS)
            resp.raise_for_status()
            data = resp.json()
            return data["data"] if isinstance(data, dict) and "data" in data else data
        except requests.exceptions.RequestException as exc:
            full_url = getattr(exc.response, "url", url)
            status_code = getattr(exc.response, "status_code", "unknown")
            message = getattr(exc.response, "text", str(exc))
            print(f"[!] Failed to fetch subreddits for keyword: '{keyword}'")
            print(f"    URL: {full_url}")
            print(f"    Status Code: {status_code}")
            print(f"    Message: {message}")
            return []

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
        try:
            resp = requests.get(url, params=params, timeout=self.TIMEOUT_SECONDS)
            resp.raise_for_status()
            return resp.json().get("data", [])
        except requests.exceptions.RequestException as exc:
            full_url = getattr(exc.response, "url", url)
            status_code = getattr(exc.response, "status_code", "unknown")
            message = getattr(exc.response, "text", str(exc))
            print(f"[!] Failed to fetch posts for subreddit: '{subreddit}'")
            print(f"    URL: {full_url}")
            print(f"    Status Code: {status_code}")
            print(f"    Message: {message}")
            return []
