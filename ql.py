from rl_base import ReinforcementLearning
import numpy as np


class QLearning(ReinforcementLearning):

    def __init__(self, *args, **kwargs):
        super(QLearning, self).__init__(*args, **kwargs)
        self.Q = np.zeros(
            (self.world.number_of_states(), self.world.number_of_actions()))

    def best_action(self, state):
        return np.argmax(self.Q[state])

    def learn(self, state, action, new_state, reward):
        qmax = np.max(self.Q[new_state])
        if self.world._isterminal(new_state):
            self.Q[state, action] = reward
        else:
            # print reward + self.discount_rate * qmax
            self.Q[state, action] = reward + self.discount_rate * qmax
