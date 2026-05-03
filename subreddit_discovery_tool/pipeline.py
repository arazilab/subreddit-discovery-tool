"""High-level pipeline orchestrator for Subreddit Finder."""
import time
from typing import List

from .collector import collect_subreddits, collect_top_posts
from .coder import (
    DEFAULT_REASONING_EFFORT,
    DEFAULT_RELEVANCY_MODEL,
    run_relevancy_coding,
)
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
        model: str = DEFAULT_RELEVANCY_MODEL,
        reasoning_effort: str = DEFAULT_REASONING_EFFORT,
        output_path: str = "output.json"
    ):
        self.keywords = keywords
        self.question = question
        self.top_n = top_n
        self.top_k = top_k
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.output_path = output_path

    def run(self) -> None:
        """
        Execute the full pipeline and save results.
        """
        start_time = time.time()
        print(f"[+] Starting subreddit discovery for keywords: {self.keywords}")

        # Step 1: Get subreddits
        print("[*] Collecting subreddits...")
        subs = collect_subreddits(self.keywords, self.top_n)
        print(f"[✓] Collected {len(subs)} unique subreddits.")

        # Step 2: Get top posts
        print("[*] Collecting top posts for each subreddit...")
        posts_map = collect_top_posts(subs, self.top_k)
        for name, data in subs.items():
            data["top_posts"] = posts_map.get(name, [])
        print(f"[✓] Top posts added.")

        # Step 3: Relevancy coding
        print(
            "[*] Running relevancy coding with "
            f"{self.model}, effort={self.reasoning_effort}..."
        )
        updated = run_relevancy_coding(
            subs=subs,
            question=self.question,
            model=self.model,
            reasoning_effort=self.reasoning_effort,
        )
        print("[✓] Relevancy coding complete.")

        # Step 4: Save to JSON
        print(f"[*] Saving results to {self.output_path} ...")
        save_json(list(updated.values()), self.output_path)
        print(f"[✓] Output saved.")

        print(f"[✓] All done in {round(time.time() - start_time, 2)} seconds.")
