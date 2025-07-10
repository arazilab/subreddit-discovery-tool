"""
Perform relevancy coding using BooleanConsensusAgent from OpenAI utils.
"""
from typing import Dict, Any
from bot_utils.boolean_consensus_agent import BooleanConsensusAgent
from tqdm import tqdm


def run_relevancy_coding(
    subs: Dict[str, Dict[str, Any]],
    question: str,
    method: str = "majority",
    model: str = "gpt-4.1-nano",
    **kwargs
) -> Dict[str, Dict[str, Any]]:
    """
    Annotate each subreddit as relevant or not.

    :param subs: Dict mapping subreddit name to its data.
    :param question: Yes/No question for relevancy.
    :param method: 'majority' or 'confidence'.
    :param model: OpenAI model name to use
    :param kwargs: Parameters for BooleanConsensusAgent.
    :return: Updated subs dict with 'relevant' field.
    """
    question = f"Using subreddit title, description and top posts, answer: {question}"
    pbar = tqdm(subs.items())
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
            agent = BooleanConsensusAgent(question=question, n_votes=n_votes, model=model)
        else:
            agent = BooleanConsensusAgent(
                question=question,
                model=model,
                target_confidence=kwargs.get("target_confidence"),
                min_votes=kwargs.get("min_votes", 5),
                max_votes=kwargs.get("max_votes", 11)
            )
        # Run and store result
        result = agent(text)
        data["relevant"] = bool(result)
        pbar.set_description(f"{name}: {bool(result)}")
    return subs
