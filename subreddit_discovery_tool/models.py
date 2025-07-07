"""
Data classes for Subreddit and Post metadata.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class PostData:
    """
    Represents a Reddit post with full raw data and selected fields.
    """
    id: str
    title: str
    score: int
    selftext: str
    data: Dict[str, Any]  # All raw fields

@dataclass
class SubredditData:
    """
    Represents a subreddit with metadata, top posts, and relevancy status.
    """
    id: str
    display_name: str
    title: str
    description: str
    subscribers: int
    data: Dict[str, Any]  # All raw fields from API
    top_posts: List[PostData] = field(default_factory=list)
    relevant: Any = "not_annotated"  # Will become True or False
