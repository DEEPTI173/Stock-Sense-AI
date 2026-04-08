import random

class GroceryEnv:
    def __init__(self):
        self.max_steps = 20
        self.reset()

    def reset(self):
        self.stock = random.randint(20, 40)
        self.demand = random.randint(15, 30)
        self.expiry = random.randint(2, 5)

        self.step_count = 0
        self.total_reward = 0

        # ✅ NEW (manual demand control)
        self.manual_demand = False

        return self.get_state()

    def step(self, action):
        self.step_count += 1

        # Actions
        if action == 1:
            self.stock += 15
        elif action == 2:
            self.stock += 40

        # Demand consumption
        if self.stock >= self.demand:
            self.stock -= self.demand
            reward = 10
        else:
            reward = -10
            self.stock = 0

        # Waste
        waste = max(0, self.stock - 60)

        # Expiry
        self.expiry -= 1
        if self.expiry <= 0:
            reward -= 5

        # ✅ FIX: Only random if NOT manual
        if not self.manual_demand:
            self.demand = random.randint(15, 35)

        self.total_reward += reward

        done = self.step_count >= self.max_steps

        return self.get_state(), reward, done, waste

    def get_state(self):
        return {
            "stock": self.stock,
            "demand": self.demand,
            "expiry": self.expiry,
            "step": self.step_count
        }