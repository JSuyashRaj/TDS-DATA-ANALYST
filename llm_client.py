import os, re, requests
from prompts import SYSTEM_PROMPT

AIPIPE_ENDPOINT = os.getenv("AIPIPE_ENDPOINT", "https://aipipe.org/openrouter/v1/chat/completions")
AIPIPE_API_KEY = os.getenv("AIPIPE_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")

if not AIPIPE_API_KEY:
    raise RuntimeError("AIPIPE_API_KEY not set in environment")

def generate_code_from_llm(user_prompt: str) -> str:
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    }
    headers = {
        "Authorization": f"Bearer {AIPIPE_API_KEY}",
        "Content-Type": "application/json"
    }

    resp = requests.post(AIPIPE_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    if "choices" not in data or not data["choices"]:
        raise ValueError("No choices in LLM response")

    raw_output = data["choices"][0]["message"]["content"]

    # Extract Python code if wrapped in ```python ... ```
    match = re.search(r"```python\s*(.*?)```", raw_output, re.DOTALL)
    return match.group(1).strip() if match else raw_output.strip()

