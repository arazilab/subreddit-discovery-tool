"""
subreddit_discovery_tool

A lightweight module for discovering and labeling relevant Reddit subreddits using
the Arctic Shift API and OpenAI's BooleanConsensusAgent. Provides tools to search
subreddits by keyword, fetch top posts, and run automated relevance coding based
on yes/no questions. Designed for research, data curation, and topic discovery.
"""

from .pipeline import SubredditFinder

__all__ = ["SubredditFinder"]
