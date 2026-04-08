import os
import requests
from openai import OpenAI

# -------- ENV VARIABLES --------
API_BASE_URL = os.getenv("API_BASE_URL", "https://your-hf-space.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# -------- OPENAI CLIENT --------
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

# -------- START LOG --------
print(f"[START] task=inventory env=stocksense model={MODEL_NAME}")

# -------- RESET --------
res = requests.post(f"{API_BASE_URL}/reset")
state = res.json()["state"]

total_reward = 0

# -------- LOOP --------
for step in range(10):

    # 🔹 Policy (simple + safe)
    if state["stock"] < state["demand"]:
        action = "Large Restock"
    elif state["stock"] < state["demand"] + 5:
        action = "Small Restock"
    else:
        action = "Do Nothing"

    # 🔹 Call API
    res = requests.post(
        f"{API_BASE_URL}/step",
        json={"action": action}
    )

    data = res.json()

    state = data["state"]
    reward = data["reward"]
    done = data["done"]

    total_reward += reward

    # -------- OPENAI EXPLANATION --------
    prompt = f"""
    You are an AI inventory assistant.
    
    Current Stock: {state['stock']}
    Current Demand: {state['demand']}
    Action Taken: {action}
    
    Explain in 1 line why this decision is good.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        explanation = response.choices[0].message.content.strip()
    except:
        explanation = "Optimizing stock to match demand."

    # -------- STEP LOG --------
    print(f"[STEP] step={step} action={action} reward={reward} done={done}")
    print(f"[AI] {explanation}")

    if done:
        break

# -------- END LOG --------
print(f"[END] total_reward={total_reward} success=true")