# 🧭 Subreddit Discovery Tool

A modular Python tool to search, collect, and label relevant subreddits using keywords. It connects to the **Arctic Shift Reddit API** and uses **Our lab's BooleanConsensusAgent** to automatically tag subreddits as relevant or not based on a yes/no criterion.

---

## 📦 Features

- Search Reddit subreddits by keyword using Arctic Shift API
- Automatically collect top posts for each subreddit
- Use OpenAI to run yes/no **relevancy coding**
- Output clean JSON with all metadata, posts, and relevance
- Easy to run programmatically or from script

---

## 🧠 How It Works

### 1. Input:
- A list of keywords (e.g. `["climate", "environment"]`)
- A yes/no question for evaluating relevance (e.g. _"Is this subreddit about climate change?"_)

### 2. Processing:
- Finds top N subreddits per keyword (`top_n`, default = 10)
- Collects top K posts for each subreddit (`top_k`, default = 5)
- Feeds subreddit description + post titles to OpenAI agent
- Runs majority or confidence-based voting to decide if relevant

### 3. Output:
- A `.json` file containing:
  - All raw subreddit metadata
  - List of top posts
  - Boolean `"relevant"` field (`true`, `false`, or `"not_annotated"`)

---

## 🗂️ File Structure

```
subreddit-discovery-tool/
├── subreddit_discovery_tool/
│   ├── __init__.py
│   ├── client.py
│   ├── collector.py
│   ├── coder.py
│   ├── models.py
│   ├── pipeline.py
│   └── utils.py
│
├── scripts/
│   └── run_pipeline.py
│
├── README.md
└── .gitignore
```

---

## 📥 Usage

### Clone the repo:

```bash
git clone https://github.com/arazilab/subreddit-discovery-tool.git
```

Also clone dependencies:

```bash
git clone https://github.com/arazilab/openai_bot_utils.git
```

Make sure they are either in the same folder or added to `sys.path`.

---

### Python Example

```python
import sys
sys.path.append('./openai_bot_utils')
sys.path.append('./subreddit-discovery-tool')

from subreddit_discovery_tool import SubredditFinder

finder = SubredditFinder(
    keywords=["mental health", "therapy"],
    question="Is this subreddit focused on mental health?",
    output_path="output.json"
)
finder.run()
```

Then open the result:

```python
import json
with open("output.json") as f:
    data = json.load(f)
print(data[0])
```

---

## ⚙️ Parameters

| Parameter       | Type     | Description                                                                 |
|----------------|----------|-----------------------------------------------------------------------------|
| `keywords`       | `List[str]` | List of strings to search subreddits by                                   |
| `question`       | `str`    | Yes/no question used for relevance coding                                   |
| `top_n`          | `int`    | Max subreddits to fetch per keyword (default: 10)                          |
| `top_k`          | `int`    | Max posts to fetch per subreddit (default: 5)                              |
| `method`         | `str`    | Voting method: `"majority"` (default) or `"confidence"`                    |
| `method_kwargs`  | `dict`   | Extra arguments for `BooleanConsensusAgent` (e.g., `n_votes`, `min_votes`) |
| `output_path`    | `str`    | File path for the output JSON                                               |

---

## 🧰 Output Format

Each subreddit looks like this:

```json
{
  "id": "abc123",
  "display_name": "climatescience",
  "title": "Climate Science",
  "description": "For discussion of climate topics...",
  "subscribers": 125000,
  "created_utc": 1354230000,
  "top_posts": [
    {
      "id": "xyz789",
      "title": "The Earth just hit a major CO2 milestone",
      "score": 4921,
      "selftext": "...",
      "data": {...}
    }
  ],
  "relevant": true
}
```
