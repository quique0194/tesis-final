import random

from mlp import MLP
import numpy as np
from rl_base import ReinforcementLearning


class DQN(ReinforcementLearning):
    buffer_size = 100
    batch_size = 10
    clone_network_steps = 100

    def __init__(self, *args, **kwargs):
        super(DQN, self).__init__(*args, **kwargs)
        state_size = self.world.state_parser.state_size()
        self.Q = MLP(state_size, state_size / 2,
                     self.world.number_of_actions())
        self.Q_ = self.Q.clone()
        self.D = []
        self.err = []
        self.updates = 0

    def best_action(self, state):
        y0 = self.Q.predict([state])
        return y0[0].argmax()

    def get_batch(self):
        states, actions, new_states, rewards = [], [], [], []
        for t in range(self.batch_size):
            i = random.randint(0, len(self.D) - 1)
            states.append(self.D[i][0])
            actions.append(self.D[i][1])
            new_states.append(self.D[i][2])
            rewards.append(self.D[i][3])
        return (np.array(states), np.array(actions), np.array(new_states),
                np.array(rewards))

    def learn(self, state, action, new_state, reward):
        self.D.append((state, action, new_state, reward))
        if len(self.D) > self.buffer_size:
            self.D = self.D[-self.buffer_size:]
        states, actions, new_states, rewards = self.get_batch()
        y1 = self.Q_.predict(new_states)
        qmaxs = y1.max(axis=1)
        obj = []
        for r, s1, qmax in zip(rewards, new_states, qmaxs):
            if self.world._isterminal(s1):
                obj.append(r)
            else:
                obj.append(r + self.discount_rate * qmax)
        obj = np.array(obj)
        y0 = self.Q.predict(states)
        y0[np.arange(len(y0)), actions] = obj
        e = self.Q.train(states, y0)
        self.updates += 1
        if self.updates >= self.clone_network_steps:
            self.updates = 0
            self.Q.clone_in_existing_mlp(self.Q_)
            self.graph_info()
        self.err.append(e.mean())

    def train_step(self, i):
        super(DQN, self).train_step(i)

    def save_data(self, name="rl"):
        super(DQN, self).save_data(name)
        np.savetxt(name + "_" + "error.csv",
                   self.err, delimiter=",")