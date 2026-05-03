"""
subreddit_discovery_tool

A lightweight module for discovering and labeling relevant Reddit subreddits using
the Arctic Shift API and the OpenAI API. Provides tools to search
subreddits by keyword, fetch top posts, and run automated relevance coding based
on yes/no questions. Designed for research, data curation, and topic discovery.
"""

from .coder import DEFAULT_REASONING_EFFORT, DEFAULT_RELEVANCY_MODEL
from .pipeline import SubredditFinder

__version__ = "0.3.0"

__all__ = [
    "DEFAULT_REASONING_EFFORT",
    "DEFAULT_RELEVANCY_MODEL",
    "SubredditFinder",
]
