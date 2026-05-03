"""Perform relevancy coding using BooleanConsensusAgent from OpenAI utils."""
from inspect import Parameter, signature
from typing import Any, Dict

from bot_utils.boolean_consensus_agent import BooleanConsensusAgent
from tqdm import tqdm

DEFAULT_RELEVANCY_MODEL = "gpt-5.4-nano"
DEFAULT_REASONING_EFFORT = "medium"
VALID_REASONING_EFFORTS = {"minimal", "low", "medium", "high", "xhigh"}


def _agent_supports_kwargs() -> bool:
    """Return True when BooleanConsensusAgent accepts arbitrary kwargs."""
    params = signature(BooleanConsensusAgent).parameters.values()
    return any(param.kind == Parameter.VAR_KEYWORD for param in params)


def _agent_accepts_param(name: str) -> bool:
    """Return True when BooleanConsensusAgent accepts a named parameter."""
    return name in signature(BooleanConsensusAgent).parameters or _agent_supports_kwargs()


def _build_agent_kwargs(model: str, reasoning_effort: str) -> Dict[str, Any]:
    """Build constructor kwargs for the installed BooleanConsensusAgent."""
    if reasoning_effort not in VALID_REASONING_EFFORTS:
        valid = ", ".join(sorted(VALID_REASONING_EFFORTS))
        raise ValueError(f"reasoning_effort must be one of: {valid}")

    kwargs: Dict[str, Any] = {"model": model}
    if _agent_accepts_param("reasoning_effort"):
        kwargs["reasoning_effort"] = reasoning_effort
    elif _agent_accepts_param("effort"):
        kwargs["effort"] = reasoning_effort
    elif reasoning_effort != DEFAULT_REASONING_EFFORT:
        raise TypeError(
            "The installed BooleanConsensusAgent does not accept a reasoning "
            "effort parameter. Update openai_bot_utils to use this option."
        )
    return kwargs


def run_relevancy_coding(
    subs: Dict[str, Dict[str, Any]],
    question: str,
    method: str = "majority",
    model: str = DEFAULT_RELEVANCY_MODEL,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
    **kwargs
) -> Dict[str, Dict[str, Any]]:
    """
    Annotate each subreddit as relevant or not.

    :param subs: Dict mapping subreddit name to its data.
    :param question: Yes/No question for relevancy.
    :param method: 'majority' or 'confidence'.
    :param model: GPT model name to use.
    :param reasoning_effort: Reasoning effort to use when the agent supports it.
    :param kwargs: Parameters for BooleanConsensusAgent.
    :return: Updated subs dict with 'relevant' field.
    """
    question = f"Using subreddit title, description and top posts, answer: {question}"
    agent_kwargs = _build_agent_kwargs(model, reasoning_effort)
    pbar = tqdm(subs.items(), desc="Coding subreddit relevance")
    for name, data in pbar:
        # Build the prompt text
        title = data.get("display_name", name)
        if data.get("public_description", "") != "":
            desc = data.get("public_description", "No description provided")
        elif data.get("description", "") != "":
            desc = data.get("description", "No description provided")
        else:
            desc = "No description provided"
        posts = data.get("top_posts", [])
        content_parts = ["subreddit title:", title, "subreddit description:", desc]
        for p in posts:
            content_parts.append(p.get("title", ""))
            content_parts.append(p.get("selftext", ""))
        text = "\n".join(content_parts)

        # Initialize the consensus agent
        if method == "majority":
            n_votes = kwargs.get("n_votes", 5)
            agent = BooleanConsensusAgent(
                question=question,
                n_votes=n_votes,
                **agent_kwargs
            )
        elif method == "confidence":
            agent = BooleanConsensusAgent(
                question=question,
                target_confidence=kwargs.get("target_confidence"),
                min_votes=kwargs.get("min_votes", 5),
                max_votes=kwargs.get("max_votes", 11),
                **agent_kwargs
            )
        else:
            raise ValueError("method must be 'majority' or 'confidence'")
        # Run and store result
        result = agent(text)
        data["relevant"] = bool(result)
        pbar.set_description(f"{name}: {bool(result)}")
    return subs
