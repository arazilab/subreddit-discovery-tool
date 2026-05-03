#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.env"
EXAMPLE_CONFIG="${SCRIPT_DIR}/config.env.example"

cd "${SCRIPT_DIR}"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  cp "${EXAMPLE_CONFIG}" "${CONFIG_FILE}"
  echo "Created package_test/config.env. Add your OpenAI key there, then run this again."
  exit 1
fi

set -a
source "${CONFIG_FILE}"
set +a

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is empty in package_test/config.env."
  exit 1
fi

python3 -m venv "${SCRIPT_DIR}/.venv"
source "${SCRIPT_DIR}/.venv/bin/activate"

python -m pip install -qqq --upgrade pip
python -m pip install -qqq --no-build-isolation -e "${REPO_ROOT}"

python "${SCRIPT_DIR}/run_ai_subreddit_discovery.py"

echo "Output written to ${SCRIPT_DIR}/${OUTPUT_PATH:-outputs/ai_subreddit_discovery.json}"
