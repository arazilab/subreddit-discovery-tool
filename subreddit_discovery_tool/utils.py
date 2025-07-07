"""
Utility functions for JSON I/O and data handling.
"""
import json
from typing import Any


def save_json(data: Any, path: str) -> None:
    """
    Save Python object to JSON file with pretty formatting.

    :param data: Data to serialize (e.g., list or dict).
    :param path: File path to save JSON.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path: str) -> Any:
    """
    Load JSON data from file.

    :param path: Path to JSON file.
    :return: Python object (list, dict, etc.).
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
