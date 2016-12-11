import random
import os
from mlp import MLP
import numpy as np
from rl_base import ReinforcementLearning
import six.moves.cPickle as pickle


class DQN(ReinforcementLearning):
    buffer_size = 100   # how many (s, a, s', r) store to train
    batch_size = 10     # how many (s, a, s', r) train at the same time
    clone_network_steps = 100    # how many learn cycles to clone net
    save_network_steps = 1000    # how many learn cycles to save networkt
    backup_network_episodes = 100     # how many episodes to create a backup

    def __init__(self, folder,
                 batch_filename=None,
                 hidden_units=None,
                 add_more_experience=True,
                 make_net_learn=True,
                 teacher=None,
                 *args, **kwargs):
        super(DQN, self).__init__(*args, **kwargs)
        state_size = self.world.state_parser.state_size()
        if hidden_units is None:
            hidden_units = state_size / 2
        self.add_more_experience = add_more_experience
        self.teacher = teacher
        self.make_net_learn = make_net_learn
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.network_name = os.path.join(folder, "qmlp.pkl")
        self.data_filename = os.path.join(folder, "")
        self.batch_filename = os.path.join(folder, "batch.pkl")
        # TODO: do not hardcode this part
        if os.path.exists(self.batch_filename):
            print "LOADING BATCH FILE FROM", self.batch_filename
            with open(self.batch_filename, "rb") as f:
                self.D = pickle.load(f)
        else:
            self.D = []
        if self.network_name and os.path.exists(self.network_name):
            print "LOADING NETWORK FROM:", self.network_name
            with open(self.network_name, "rb") as f:
                self.Q = pickle.load(f)
        else:
            print "Creating MLP with %i hidden units" % hidden_units
            self.Q = MLP(state_size, hidden_units,
                         self.world.number_of_actions())
        self.Q_ = self.Q.clone()
        self.err = []
        self.updates = 0
        self.steps_since_last_save_net = 0

    def best_action(self, state):
        y0 = self.Q.predict([state])
        return y0[0].argmax()

    def choose_action(self, state):
        if self.teacher:
            # must return the index of an action
            if np.random.rand() <= self.random_prob:
                action = self.teacher.choose_action(state, self.world)
            else:
                action = self.best_action(state)
            return action
        else:
            return super(DQN, self).choose_action(state)

    def get_batch(self):
        states, actions, new_states, rewards, terminals = [], [], [], [], []
        for t in range(min(self.batch_size, len(self.D))):
            i = random.randint(0, len(self.D) - 1)
            states.append(self.D[i][0])
            actions.append(self.D[i][1])
            new_states.append(self.D[i][2])
            rewards.append(self.D[i][3])
            terminals.append(self.D[i][4])
        return (np.array(states), np.array(actions), np.array(new_states),
                np.array(rewards), np.array(terminals))

    def learn(self, state, action, new_state, reward, is_terminal=False):
        if self.add_more_experience:
            self.D.append((state, action, new_state, reward, is_terminal))
        if len(self.D) > self.buffer_size:
            self.D = self.D[-self.buffer_size:]
        states, actions, new_states, rewards, terminals = self.get_batch()
        y1 = self.Q_.predict(new_states)
        qmaxs = y1.max(axis=1)
        obj = []
        for r, s1, qmax, terminal in zip(rewards, new_states, qmaxs,
                                         terminals):
            if terminal:
                obj.append(r)
            else:
                obj.append(r + self.discount_rate * qmax)
        obj = np.array(obj)
        y0 = self.Q.predict(states)
        y0[np.arange(len(y0)), actions] = obj
        if self.make_net_learn:
            e = self.Q.train(states, y0)
        self.updates += 1
        if self.updates % self.clone_network_steps == 0:
            self.Q.clone_in_existing_mlp(self.Q_)
        if self.updates % self.save_network_steps == 0:
            self.save_net()
            self.save_data(self.data_filename or "rl")
        self.err.append(e.mean())

    def save_net(self, name=None):
        if name is None:
            name = self.network_name
        if name:
            if not name.endswith(".pkl"):
                name += ".pkl"
            print "SAVING NETWORK TO", name
            with open(name, "wb") as f:
                pickle.dump(self.Q, f)

    def train_episode(self, i):
        super(DQN, self).train_episode(i)
        if i % self.backup_network_episodes == 0:
            self.save_net(self.network_name + "_" + str(i))

    def save_data(self):
        super(DQN, self).save_data("rl")
        fhandle = open("rl_error.csv", "a")
        np.savetxt(fhandle, self.err, delimiter=",")
        self.err = []

        with open(self.batch_filename, "wb") as f:
            pickle.dump(self.D, f)
