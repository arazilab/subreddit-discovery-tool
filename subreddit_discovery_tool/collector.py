"""
Collects subreddit and post data using the API client.
"""
from typing import List, Dict
from .client import ArcticShiftClient
from tqdm import tqdm
import urllib.parse


def collect_subreddits(keywords: List[str], top_n: int) -> Dict[str, Dict]:
    """
    Collect top N subreddits for each keyword.

    :param keywords: List of search keywords.
    :param top_n: Number of subreddits per keyword.
    :return: Dict mapping subreddit name to raw data.
    """
    client = ArcticShiftClient()
    subs: Dict[str, Dict] = {}
    for kw in tqdm(keywords, desc="Searching keywords"):
        encoded_kw = urllib.parse.quote(kw)
        results = client.search_subreddits(encoded_kw, top_n)
        if not results:
            print(f"[!] No subreddits found or API failed for: {kw}")
            continue
        for item in results:
            name = item.get("display_name") or item.get("subreddit")
            # Deduplicate by name
            if name not in subs:
                subs[name] = item
    return subs


def collect_top_posts(subs: Dict[str, Dict], top_k: int) -> Dict[str, List[Dict]]:
    """
    Collect top K posts for each subreddit.

    :param subs: Dict of subreddit raw data.
    :param top_k: Number of posts per subreddit.
    :return: Dict mapping subreddit name to list of post dicts.
    """
    client = ArcticShiftClient()
    posts_map: Dict[str, List[Dict]] = {}
    for name in tqdm(subs, desc="Fetching posts per subreddit"):
        results = client.get_top_posts(name, top_k)
        posts_map[name] = results
    return posts_map
