from flask import Flask, render_template, jsonify, request
from grocery_env import GroceryEnv
from q_learning import QLearningAgent

app = Flask(__name__)

env = GroceryEnv()
agent = QLearningAgent()

human_score = 0
ai_score = 0

# ---------------- UI ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- RESET (FIXED ✅ POST REQUIRED) ----------------
@app.route("/reset", methods=["POST"])
def reset():
    global human_score, ai_score
    human_score = 0
    ai_score = 0

    state = env.reset()

    return jsonify({
        "state": state
    })


# ---------------- STEP (HUMAN) ----------------
@app.route("/step", methods=["POST"])
def step():
    global human_score

    data = request.get_json()
    action = data.get("action", "Do Nothing")

    state, reward, done, waste = env.step(action)

    human_score += reward

    return jsonify({
        "state": state,
        "reward": reward,
        "done": done,
        "info": {
            "executed_action": action,
            "waste": waste
        }
    })


# ---------------- AI STEP ----------------
@app.route("/ai_step", methods=["POST"])
def ai_step():
    global ai_score

    state_now = env.get_state()
    action = agent.choose_action(state_now)

    state, reward, done, waste = env.step(action)

    ai_score += reward

    return jsonify({
        "state": state,
        "reward": reward,
        "done": done,
        "info": {
            "executed_action": action,
            "confidence": agent.confidence(state),
            "waste": waste
        }
    })


# ---------------- STATE (REQUIRED ✅) ----------------
@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(env.get_state())


# ---------------- SET DEMAND ----------------
@app.route("/set_demand", methods=["POST"])
def set_demand():
    data = request.get_json()

    env.demand = int(data["demand"])
    env.manual_demand = True

    return jsonify({"demand": env.demand})


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)