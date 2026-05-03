# AI Subreddit Discovery Test

This folder runs a small live test of the `subreddit-discovery-tool` package.

## How To Run

Run the script from the repository root.

```bash
bash package_test/run_test.sh
```

The first run creates `package_test/config.env`.

Add your OpenAI API key to that file, then run the script again.

```bash
bash package_test/run_test.sh
```

The script creates a virtual environment, installs this package, runs the discovery script, and writes the output JSON.

Default output file.

```text
package_test/outputs/ai_subreddit_discovery.json
```

## Method

The script searches Reddit subreddit metadata through the Arctic Shift API.

For each keyword, it asks the package to collect candidate subreddits.

For each candidate subreddit, it collects top posts.

Then it sends the subreddit title, description, and top post text to the OpenAI API.

The model answers the yes or no research question. The package stores the label in `relevant` and a short explanation in `relevance_reason`.

## Model

Default model.

```text
gpt-5.4-nano
```

Default reasoning effort.

```text
medium
```

## Main Settings

```text
TOP_N=10
TOP_K=5
MODEL=gpt-5.4-nano
REASONING_EFFORT=medium
```

`TOP_N` controls how many subreddit search results are collected for each keyword.

`TOP_K` controls how many top posts are collected for each subreddit.
