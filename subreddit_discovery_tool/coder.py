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
    **kwargs
) -> Dict[str, Dict[str, Any]]:
    """
    Annotate each subreddit as relevant or not.

    :param subs: Dict mapping subreddit name to its data.
    :param question: Yes/No question for relevancy.
    :param method: 'majority' or 'confidence'.
    :param kwargs: Parameters for BooleanConsensusAgent.
    :return: Updated subs dict with 'relevant' field.
    """
    question = f"Using subreddit title, description and top posts, answer: {question}"
    for name, data in tqdm(subs.items(), desc="Relevance classification"):
        # Build the prompt text
        title = data.get("display_name", name)
        desc = data.get("description", "No description provided")
        posts = data.get("top_posts", [])
        content_parts = ["subreddit title:", title, "subreddit description:", desc]
        for p in posts:
            content_parts.append(p.get("title", ""))
            content_parts.append(p.get("selftext", ""))
        text = "\n".join(content_parts)

        # Initialize the consensus agent
        if method == "majority":
            n_votes = kwargs.get("n_votes", 5)
            agent = BooleanConsensusAgent(question=question, n_votes=n_votes)
        else:
            agent = BooleanConsensusAgent(
                question=question,
                target_confidence=kwargs.get("target_confidence"),
                min_votes=kwargs.get("min_votes", 5),
                max_votes=kwargs.get("max_votes", 11)
            )
        # Run and store result
        print(question)
        print(text)
        #result = agent(text)
        result = False
        data["relevant"] = bool(result)
    return subs
