"""Run GPT based relevancy coding with the OpenAI API."""
import json
from typing import Any, Dict, Optional

from tqdm import tqdm

DEFAULT_RELEVANCY_MODEL = "gpt-5.4-nano"
DEFAULT_REASONING_EFFORT = "medium"
VALID_REASONING_EFFORTS = {"none", "minimal", "low", "medium", "high", "xhigh"}


def _uses_reasoning_effort(model: str) -> bool:
    """Return True when the model name commonly supports reasoning effort."""
    return model.startswith("gpt-5")


def _subreddit_text(name: str, data: Dict[str, Any]) -> str:
    title = data.get("display_name", name)
    desc = (
        data.get("public_description")
        or data.get("description")
        or "No description provided"
    )
    content_parts = [
        f"Subreddit title: {title}",
        f"Subreddit description: {desc}",
        "Top posts:",
    ]
    for post in data.get("top_posts", []):
        post_title = post.get("title", "")
        post_text = post.get("selftext", "")
        content_parts.append(f"- {post_title}\n{post_text}".strip())
    return "\n".join(content_parts)


def _parse_response_text(response: Any) -> Dict[str, Any]:
    text = getattr(response, "output_text", None)
    if not text:
        raise ValueError("OpenAI response did not include output_text.")
    return json.loads(text)


def _openai_client() -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError(
            "The openai package is required for relevancy coding. "
            "Install this package with `pip install -qqq -e .`."
        ) from exc
    return OpenAI()


def code_subreddit_relevance(
    text: str,
    question: str,
    model: str = DEFAULT_RELEVANCY_MODEL,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
    client: Optional[Any] = None,
) -> Dict[str, Any]:
    """Code one subreddit as relevant or not relevant."""
    if reasoning_effort not in VALID_REASONING_EFFORTS:
        valid = ", ".join(sorted(VALID_REASONING_EFFORTS))
        raise ValueError(f"reasoning_effort must be one of: {valid}")

    openai_client = client or _openai_client()
    request: Dict[str, Any] = {
        "model": model,
        "instructions": (
            "You are coding Reddit communities for a research project. "
            "Answer the user's yes or no relevance question using only the "
            "subreddit title, description, and top posts. Return JSON only."
        ),
        "input": (
            f"Question: {question}\n\n"
            f"Subreddit information:\n{text}\n\n"
            "Return true if the subreddit is relevant. Return false if it is "
            "not relevant or there is not enough evidence."
        ),
        "text": {
            "format": {
                "type": "json_schema",
                "name": "subreddit_relevance",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "relevant": {"type": "boolean"},
                        "reason": {"type": "string"},
                    },
                    "required": ["relevant", "reason"],
                },
            }
        },
    }
    if _uses_reasoning_effort(model):
        request["reasoning"] = {"effort": reasoning_effort}

    result = _parse_response_text(openai_client.responses.create(**request))
    return {
        "relevant": bool(result["relevant"]),
        "reason": str(result["reason"]).strip(),
    }


def run_relevancy_coding(
    subs: Dict[str, Dict[str, Any]],
    question: str,
    model: str = DEFAULT_RELEVANCY_MODEL,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
    client: Optional[Any] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Annotate each subreddit as relevant or not.

    :param subs: Dict mapping subreddit name to its data.
    :param question: Yes or no question for relevance coding.
    :param model: GPT model name to use.
    :param reasoning_effort: Effort level for GPT-5 style models.
    :param client: Optional OpenAI client.
    :return: Updated subs dict with relevance fields.
    """
    pbar = tqdm(subs.items(), desc="Coding subreddit relevance")
    for name, data in pbar:
        result = code_subreddit_relevance(
            text=_subreddit_text(name, data),
            question=question,
            model=model,
            reasoning_effort=reasoning_effort,
            client=client,
        )
        data["relevant"] = result["relevant"]
        data["relevance_reason"] = result["reason"]
        pbar.set_description(f"{name}: {result['relevant']}")
    return subs
