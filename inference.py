import os
import requests
from openai import OpenAI

# =========================
# ENV VARIABLES (IMPORTANT)
# =========================
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://deepti2005-smart-grocery-dashboard.hf.space"
)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# OpenAI client
client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

# =========================
# HELPER FUNCTION (AI DECISION)
# =========================
def get_ai_action(state):
    prompt = f"""
You are an inventory optimization AI.

State:
Stock: {state['stock']}
Demand: {state['demand']}
Expiry: {state['expiry']}

Choose action:
0 = Do nothing
1 = Small stock
2 = Large stock

Only return number (0/1/2)
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5
        )

        action = int(response.choices[0].message.content.strip())
        return action

    except:
        # fallback rule-based
        if state["stock"] < state["demand"]:
            return 2
        elif state["stock"] < 25:
            return 1
        else:
            return 0

# =========================
# MAIN LOOP
# =========================
def run():

    print("START")

    # Reset environment
    res = requests.post(f"{API_BASE_URL}/reset")
    state = res.json()["state"]

    total_reward = 0

    for step in range(20):

        action = get_ai_action(state)

        res = requests.post(
            f"{API_BASE_URL}/step",
            json={"action": action}
        )

        data = res.json()

        state = data["state"]
        reward = data["reward"]
        total_reward += reward

        print(f"STEP {step+1}")
        print(f"State: {state}")
        print(f"Action: {action}")
        print(f"Reward: {reward}")
        print("------")

        if data["done"]:
            break

    print("END")
    print("Total Reward:", total_reward)


if __name__ == "__main__":
    run()