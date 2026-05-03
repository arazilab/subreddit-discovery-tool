# Subreddit Discovery Tool

Subreddit Discovery Tool is a Python package for finding Reddit communities and coding their relevance to a research question. It searches subreddit metadata with the Arctic Shift API, collects top posts, and uses a GPT powered Boolean consensus agent to label each subreddit as relevant or not relevant.

The tool is useful when you need a traceable list of candidate subreddits for research, data collection, or topic discovery.

## Features

- Search subreddit names by one or more keywords
- Collect top posts for each candidate subreddit
- Code relevance with majority voting or confidence based voting
- Use any GPT model available to your OpenAI account
- Set reasoning effort for supported GPT models
- Save subreddit metadata, top posts, and relevance labels as JSON

## Requirements

- Python 3.9 or newer
- Access to the Arctic Shift API
- An OpenAI API key
- The lab `openai_bot_utils` package, available on your Python path

The default relevancy model is `gpt-5.4-nano`.

The default reasoning effort is `medium`.

## Installation

Clone this repository.

```bash
git clone https://github.com/arazilab/subreddit-discovery-tool.git
cd subreddit-discovery-tool
```

Install the package in editable mode.

```bash
pip install -qqq -e .
```

Make sure `openai_bot_utils` is also installed or added to your Python path.

Set your OpenAI API key in your shell.

```bash
export OPENAI_API_KEY="your_api_key"
```

## Python Usage

```python
from subreddit_discovery_tool import SubredditFinder

finder = SubredditFinder(
    keywords=["mental health", "therapy"],
    question="Is this subreddit focused on mental health support?",
    top_n=10,
    top_k=5,
    method="majority",
    method_kwargs={"n_votes": 5},
    model="gpt-5.4-nano",
    reasoning_effort="medium",
    output_path="subreddits.json",
)

finder.run()
```

You can use another GPT model by changing `model`.

```python
finder = SubredditFinder(
    keywords=["python", "data science"],
    question="Is this subreddit useful for learning Python?",
    model="gpt-5.4",
    reasoning_effort="high",
    output_path="python_subreddits.json",
)
```

## Command Line Usage

Run the example pipeline script from the repository root.

```bash
python scripts/run_pipeline.py \
  --keyword "mental health" \
  --keyword therapy \
  --question "Is this subreddit focused on mental health support?" \
  --model gpt-5.4-nano \
  --reasoning-effort medium \
  --output-path subreddits.json
```

For confidence based voting, use `--method confidence`.

```bash
python scripts/run_pipeline.py \
  --keyword climate \
  --question "Is this subreddit about climate change?" \
  --method confidence \
  --min-votes 5 \
  --max-votes 11 \
  --target-confidence 0.8
```

## Parameters

| Name | Type | Default | Meaning |
| --- | --- | --- | --- |
| `keywords` | `list[str]` | required | Search terms used to find candidate subreddits |
| `question` | `str` | required | Yes or no question used for relevance coding |
| `top_n` | `int` | `10` | Number of subreddits to collect per keyword part |
| `top_k` | `int` | `5` | Number of top posts to collect per subreddit |
| `method` | `str` | `majority` | Voting method, either `majority` or `confidence` |
| `method_kwargs` | `dict` | `{}` | Voting settings such as `n_votes`, `min_votes`, `max_votes`, or `target_confidence` |
| `model` | `str` | `gpt-5.4-nano` | GPT model used for relevancy coding |
| `reasoning_effort` | `str` | `medium` | Effort level for supported GPT models |
| `output_path` | `str` | `output.json` | Path for the JSON output file |

Supported effort values are `minimal`, `low`, `medium`, `high`, and `xhigh`.

## Output

The output file is a JSON list. Each item contains subreddit metadata, top posts, and a `relevant` field.

```json
{
  "id": "abc123",
  "display_name": "climatescience",
  "title": "Climate Science",
  "description": "For discussion of climate topics",
  "subscribers": 125000,
  "top_posts": [
    {
      "id": "xyz789",
      "title": "The Earth just hit a major CO2 milestone",
      "score": 4921,
      "selftext": ""
    }
  ],
  "relevant": true
}
```

## Package Layout

```text
subreddit_discovery_tool/
  client.py
  collector.py
  coder.py
  models.py
  pipeline.py
  utils.py
scripts/
  run_pipeline.py
```

`client.py` talks to Arctic Shift. `collector.py` gathers subreddit and post data. `coder.py` runs GPT based relevance coding. `pipeline.py` connects the steps into one workflow.
