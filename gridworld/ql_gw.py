import copy
import numpy as np
from model import StateParser, World
from ql import QLearning


class GridWorldStateParser(StateParser):

    def __init__(self, dim, *args, **kwargs):
        self.dim = dim
        super(GridWorldStateParser, self).__init__(*args, **kwargs)

    def load(self, n):
        return np.array([n // self.dim, n % self.dim])

    def dump(self, state):
        return state[0] * self.dim + state[1]


class GridWorld(World):

    def __init__(self, dim, *args, **kwargs):
        self.dim = dim
        self.state_parser = GridWorldStateParser(self.dim)
        super(GridWorld, self).__init__(*args, **kwargs)

    def exe_action(self, state, action):
        # from numbers
        new_state = copy.deepcopy(state)
        new_state += action
        reward = 0
        for i in range(2):
            if new_state[i] >= self.dim or new_state[i] < 0:
                new_state[i] = max(0, min(self.dim - 1, new_state[i]))
                reward = -1
        if self.isterminal(new_state):
            reward = 1
        return new_state, reward

    def isterminal(self, state):
        return np.array_equal(state, np.array([self.dim - 1, self.dim - 1]))

    def number_of_states(self):
        return self.dim * self.dim


if __name__ == "__main__":
    actions = [
        np.array([0, -1]),
        np.array([0, 1]),
        np.array([1, 0]),
        np.array([-1, 0]),
    ]

    qlearning = QLearning(GridWorld(5, actions), np.array([0, 0]))
    # qlearning.show_progress = False
    qlearning.train(100)
    # print qlearning.Q
