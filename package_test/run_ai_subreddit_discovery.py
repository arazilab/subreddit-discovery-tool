"""Run the AI subreddit discovery test case."""
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from subreddit_discovery_tool import SubredditFinder


KEYWORDS = [
    "chatgpt",
    "claude",
    "gemini",
    "llama",
    "gpt",
    "llm",
    "genai",
    "openai",
    "anthropic",
    "googleai",
    "aitools",
    "aichatbot",
    "aiassistant",
    "conversationalai",
    "aicompanion",
    "aigirlfriend",
    "aiboyfriend",
    "virtualpartner",
    "romanticai",
    "aidating",
    "parasocialai",
    "emotionalai",
    "aifriend",
    "chatbotcompanion",
    "roleplayai",
    "aiaddiction",
    "ailoneliness",
    "chatbotexperience",
    "aiethics",
    "aidependency",
    "aisocial",
    "aimentalhealth",
    "aicompanionship",
    "humanai",
    "characterai",
    "replika",
    "kindroid",
    "nomiai",
    "janitorai",
    "chaiai",
    "cai",
    "airoleplay",
]

QUESTION = (
    "Is the primary focus of this subreddit on interacting with, discussing, "
    "or sharing experiences about AI systems?"
)


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name, str(default)).strip()
    return int(value)


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY in package_test/config.env first.")

    output_path = Path(os.environ.get("OUTPUT_PATH", "outputs/ai_subreddit_discovery.json"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    finder = SubredditFinder(
        keywords=KEYWORDS,
        question=QUESTION,
        top_n=env_int("TOP_N", 10),
        top_k=env_int("TOP_K", 5),
        model=os.environ.get("MODEL", "gpt-5.4-nano").strip(),
        reasoning_effort=os.environ.get("REASONING_EFFORT", "medium").strip(),
        output_path=str(output_path),
    )
    finder.run()


if __name__ == "__main__":
    main()
