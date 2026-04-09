from grocery_env import GroceryEnv
import random

def grade():
    env = GroceryEnv()
    state = env.reset()

    total_reward = 0

    for _ in range(20):

        # 🤖 Simple intelligent policy
        if state["stock"] < state["demand"]:
            action = 2
        elif state["stock"] < 25:
            action = 1
        else:
            action = 0

        # 🎲 small randomness (important for realism)
        if random.random() < 0.2:
            action = random.choice([0, 1, 2])

        # ✅ FIX: your env returns 4 values
        state, reward, done, waste = env.step(action)

        total_reward += reward

        if done:
            break

    # 🎯 Convert reward → score (MUST be between 0 and 1, not exact 0/1)
    score = total_reward / 200

    # 🚨 VERY IMPORTANT 
    if score <= 0:
        score = 0.1
    elif score >= 1:
        score = 0.9

    return score


# optional (for local testing)
if __name__ == "__main__":
    print("Score:", grade())
