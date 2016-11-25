import copy

from model import StateParser, World
import numpy as np
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

    def __init__(self, dim, target, *args, **kwargs):
        self.dim = dim
        self.target = target
        super(GridWorld, self).__init__(*args, **kwargs)

    def exe_action(self, state, action):
        new_state = copy.deepcopy(state)
        new_state += action
        reward = 0
        for i in range(2):
            if new_state[i] >= self.dim or new_state[i] < 0:
                new_state[i] = max(0, min(self.dim - 1, new_state[i]))
                reward = -1
        if self.isterminal(new_state):
            reward = 10
        else:
            dist = np.linalg.norm(self.target - new_state)
            reward = 1.0 / dist
        return new_state, reward

    def isterminal(self, state):
        return np.array_equal(state, self.target)

    def number_of_states(self):
        return self.dim * self.dim

    def gen_random_state(self):
        return np.random.random_integers(0, self.dim - 1, 2)


if __name__ == "__main__":
    actions = [
        np.array([0, -1]),
        np.array([0, 1]),
        np.array([1, 0]),
        np.array([-1, 0]),
    ]
    DIM = 13
    qlearning = QLearning(
        GridWorld(DIM, np.array([DIM / 2, DIM / 2]), actions,
                  GridWorldStateParser(DIM)))
    # qlearning.show_progress = False
    qlearning.random_prob = 0.75
    try:
        qlearning.train(300)
    finally:
        print "SAVING FILES...",
        qlearning.save_data("graph/ql_gw_" + str(DIM))
        print "DONE"
