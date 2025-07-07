"""
Example script to run the pipeline from command line.
"""
import sys

# Ensure external utils are in path
sys.path.append('./openai_bot_utils')
sys.path.append('./relevancy_coding_tool')

from finder.pipeline import SubredditFinder


def main():
    # Example usage; replace with argparse if needed
    keywords = ["python", "data science"]
    question = "Is this subreddit relevant to learning Python?"
    finder = SubredditFinder(
        keywords=keywords,
        question=question,
        output_path="subreddits.json"
    )
    finder.run()

if __name__ == '__main__':
    main()
