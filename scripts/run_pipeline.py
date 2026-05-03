"""Run the subreddit discovery pipeline from the command line."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Ensure external utils are in path
sys.path.append(str(ROOT / "openai_bot_utils"))
sys.path.append(str(ROOT / "relevancy_coding_tool"))


def parse_args():
    parser = argparse.ArgumentParser(description="Run subreddit discovery.")
    parser.add_argument("--keyword", action="append", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--output-path", default="subreddits.json")
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--method", choices=["majority", "confidence"], default="majority")
    parser.add_argument("--model", default="gpt-5.4-nano")
    parser.add_argument(
        "--reasoning-effort",
        choices=["minimal", "low", "medium", "high", "xhigh"],
        default="medium"
    )
    parser.add_argument("--n-votes", type=int, default=5)
    parser.add_argument("--min-votes", type=int, default=5)
    parser.add_argument("--max-votes", type=int, default=11)
    parser.add_argument("--target-confidence", type=float, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    from subreddit_discovery_tool.pipeline import SubredditFinder

    method_kwargs = (
        {"n_votes": args.n_votes}
        if args.method == "majority"
        else {
            "min_votes": args.min_votes,
            "max_votes": args.max_votes,
            "target_confidence": args.target_confidence,
        }
    )
    finder = SubredditFinder(
        keywords=args.keyword,
        question=args.question,
        top_n=args.top_n,
        top_k=args.top_k,
        method=args.method,
        method_kwargs=method_kwargs,
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        output_path=args.output_path
    )
    finder.run()


if __name__ == '__main__':
    main()
