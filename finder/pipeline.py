"""
High-level pipeline orchestrator for Subreddit Finder.
"""
from typing import List, Dict, Any
from .collector import collect_subreddits, collect_top_posts
from .coder import run_relevancy_coding
from .utils import save_json


class SubredditFinder:
    """
    Main class to run the subreddit finding and coding pipeline.
    """
    def __init__(
        self,
        keywords: List[str],
        question: str,
        top_n: int = 10,
        top_k: int = 5,
        sort_by: str = "score",
        method: str = "majority",
        method_kwargs: Dict[str, Any] = None,
        output_path: str = "output.json"
    ):
        self.keywords = keywords
        self.question = question
        self.top_n = top_n
        self.top_k = top_k
        self.method = method
        self.method_kwargs = method_kwargs or {}
        self.output_path = output_path

    def run(self) -> None:
        """
        Execute the full pipeline and save results.
        """
        # Step 1: Get subreddits
        subs = collect_subreddits(self.keywords, self.top_n)

        # Step 2: Get top posts
        posts_map = collect_top_posts(subs, self.top_k)
        for name, data in subs.items():
            data["top_posts"] = posts_map.get(name, [])

        # Step 3: Relevancy coding
        updated = run_relevancy_coding(subs, self.question, self.method, **self.method_kwargs)

        # Step 4: Save to JSON
        save_json(list(updated.values()), self.output_path)
