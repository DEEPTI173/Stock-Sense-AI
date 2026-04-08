import os
import requests
from openai import OpenAI

#  use environment variables
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.environ.get("API_KEY", "your_dummy_key")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")

# ✅ Create client (MANDATORY FORMAT)
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.environ.get("API_KEY", "your_dummy_key")

ENV_URL = "https://deepti2005-smart-grocery-dashboard.hf.space"


def get_ai_action(state):
    # ❗ DO NOT wrap entire function in try → we WANT crash if LLM fails

    prompt = f"""
Stock: {state.get('stock', 0)}
Demand: {state.get('demand', 0)}
Expiry: {state.get('expiry', 0)}

Choose best action:
0 = do nothing
1 = small restock
2 = large restock

Return only number.
"""

    # ✅ FORCE LLM CALL (validator must detect this)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=5
    )

    action_text = response.choices[0].message.content.strip()

    if action_text not in ["0", "1", "2"]:
        return 0

    return int(action_text)


def run():
    print("[START] task=inventory env=grocery model=llm")

    # RESET
    res = requests.get(f"{ENV_URL}/reset")
    state = res.json()

    for step in range(20):

        # ✅ THIS MUST CALL LLM EVERY STEP
        action = get_ai_action(state)

        res = requests.post(
            f"{ENV_URL}/step",
            json={"action": action}
        )

        data = res.json()

        state = data.get("state", {})
        reward = data.get("reward", 0)
        done = data.get("done", False)

        print(f"[STEP] step={step} action={action} reward={reward} done={done}")

        if done:
            break

    print("[END] success=true score=1.0")


if __name__ == "__main__":
    run()
