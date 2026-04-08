from grocery_env import GroceryEnv
import random

def choose_action(state):
    """Smart policy with slight randomness"""

    # 20% exploration
    if random.random() < 0.2:
        return random.choice([
            "Do Nothing",
            "Small Restock",
            "Large Restock"
        ])

    # Exploitation (smart logic)
    if state["stock"] < state["demand"]:
        return "Large Restock"
    elif state["stock"] < state["demand"] + 5:
        return "Small Restock"
    else:
        return "Do Nothing"


def grade():
    env = GroceryEnv()
    state = env.reset()

    total_reward = 0
    steps = 0

    print("\n🚀 Grading Started...\n")

    for step in range(20):

        action = choose_action(state)

        state, reward, done, waste = env.step(action)

        total_reward += reward
        steps += 1

        print(f"Step {step+1}: Action={action}, Reward={reward}, Stock={state['stock']}, Demand={state['demand']}")

        if done:
            break

    print("\n🎯 Final Result:")
    print("Total Reward:", total_reward)

    # 🎯 SCORING LOGIC (IMPROVED)
    if total_reward >= 100:
        print("🔥 Grade: Excellent")
        return 1
    elif total_reward >= 60:
        print("👍 Grade: Good")
        return 1
    elif total_reward >= 30:
        print("⚖️ Grade: Average")
        return 0
    else:
        print("⚠️ Grade: Poor")
        return 0


if __name__ == "__main__":
    score = grade()
    print("\nFinal Score:", score)