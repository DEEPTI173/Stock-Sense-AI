from grocery_env import GroceryEnv
import random


# 🟢 EASY TASK
def grade_easy():
    env = GroceryEnv()
    state = env.reset()

    total_reward = 0

    for _ in range(20):
        action = 0  # do nothing baseline
        state, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            break

    score = total_reward / 200
    return max(0.1, min(score, 0.9))


# 🟡 MEDIUM TASK
def grade_medium():
    env = GroceryEnv()
    state = env.reset()

    total_reward = 0

    for _ in range(20):
        if state["stock"] < state["demand"]:
            action = 2
        elif state["stock"] < 25:
            action = 1
        else:
            action = 0

        state, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            break

    score = total_reward / 200
    return max(0.1, min(score, 0.9))


# 🔴 HARD TASK
def grade_hard():
    env = GroceryEnv()
    state = env.reset()

    total_reward = 0

    for _ in range(20):
        # harder: randomness + smarter logic
        if random.random() < 0.3:
            action = random.choice([0, 1, 2])
        else:
            if state["stock"] < state["demand"]:
                action = 2
            elif state["stock"] > 60:
                action = 0
            else:
                action = 1

        state, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            break

    score = total_reward / 200
    return max(0.1, min(score, 0.9))
