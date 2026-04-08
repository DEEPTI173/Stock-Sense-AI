import random

class QLearningAgent:
    def choose_action(self, state):
        if state['stock'] < state['demand']:
            return 2
        elif state['stock'] > state['demand'] + 20:
            return 0
        else:
            return 1

    def confidence(self, state):
        return min(100, int((state['stock'] / (state['demand']+1)) * 50))