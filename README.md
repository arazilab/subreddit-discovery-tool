# Subreddit Discovery Tool

Subreddit Discovery Tool is a Python package for finding Reddit communities and coding their relevance to a research question. It searches subreddit metadata with the Arctic Shift API, collects top posts, and uses the OpenAI API to label each subreddit as relevant or not relevant.

The tool is useful when you need a traceable list of candidate subreddits for research, data collection, or topic discovery.

## Features

- Search subreddit names by one or more keywords
- Collect top posts for each candidate subreddit
- Code relevance with a direct OpenAI API call
- Use any GPT model available to your OpenAI account
- Set reasoning effort for supported GPT models
- Save subreddit metadata, top posts, relevance labels, and short relevance reasons as JSON

## Requirements

- Python 3.9 or newer
- Access to the Arctic Shift API
- An OpenAI API key

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

## Parameters

| Name | Type | Default | Meaning |
| --- | --- | --- | --- |
| `keywords` | `list[str]` | required | Search terms used to find candidate subreddits |
| `question` | `str` | required | Yes or no question used for relevance coding |
| `top_n` | `int` | `10` | Number of subreddits to collect per keyword part |
| `top_k` | `int` | `5` | Number of top posts to collect per subreddit |
| `model` | `str` | `gpt-5.4-nano` | GPT model used for relevancy coding |
| `reasoning_effort` | `str` | `medium` | Effort level for supported GPT models |
| `output_path` | `str` | `output.json` | Path for the JSON output file |

Supported effort values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`.

Reasoning effort is sent for GPT-5 style models. Other GPT models can still be used, but the package does not send an effort setting for models that normally do not support it.

## Output

The output file is a JSON list. Each item contains subreddit metadata, top posts, a `relevant` field, and a `relevance_reason` field.

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
  "relevant": true,
  "relevance_reason": "The subreddit focuses on climate science discussion."
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
