import sys
import os
import copy
import matplotlib.pyplot as plt
import numpy as np
from timer import Timer


class ReinforcementLearning(object):
    # Learning params
    discount_rate = 0.99
    random_prob = 1.0
    random_prob_decay = 0.95
    min_random_prob = 0.1

    # Interface params
    print_episodes = True
    train_info_steps = 10
    show_graph = None
    show_progress = True

    def __init__(self, world, state0=None, folder="rl_data"):
        self.world = world
        if state0:
            self.state0 = self.world.state_parser.dump(state0)
        else:
            self.state0 = None
        self.avg_reward = []
        self.cumulative_reward = [0]
        self.folder = folder

        # Files
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        else:
            ans = raw_input("The folder %s already exists, if you say 'y' "
                            "we will use the files in folder to continue "
                            "learning. Continue (y|n):")
            if ans != "y":
                sys.exit()
        self.cumulative_reward_filename = os.path.join(folder,
                                                       "avg_reward.csv")
        self.avg_reward_filename = os.path.join(folder,
                                                "cumulative_reward.csv")

    def choose_action(self, state):
        if np.random.rand() <= self.random_prob:
            action = self.world.random_action()
        else:
            action = self.best_action(state)
        return action

    def run_episode(self, state0):
        """Run an episode from the initial state to a terminal state."""
        if state0 is None:
            state = self.world._gen_random_state()
        else:
            state = state0
        steps = 0
        with Timer():
            while not self.world.isterminal():
                steps += 1
                state_backup = copy.deepcopy(state)
                action = self.choose_action(state)
                new_state, reward = self.world._exe_action(action)
                self.curr_episode_rewards.append(reward)
                self.learn(state_backup, action, new_state, reward,
                           self.world.isterminal())
                state = new_state
        return steps

    def get_info(self):
        return self.cumulative_reward

    def graph_info(self):
        plt.cla()
        plt.plot(self.get_info())
        plt.draw()
        plt.pause(0.0001)

    def train_episode(self, i):
        if i % self.train_info_steps == 0 and self.print_episodes:
            print "Episode", i, "Random prob:", self.random_prob
        if i % self.train_info_steps == 0 and self.show_progress:
            self.graph_info()
        self.curr_episode_rewards = []
        steps = 0
        while steps == 0:
            steps = self.run_episode(self.state0)
        self.avg_reward.append(np.average(self.curr_episode_rewards))
        self.cumulative_reward.append(
            self.cumulative_reward[-1] + self.avg_reward[-1])
        self.random_prob *= self.random_prob_decay
        self.random_prob = max(self.random_prob, self.min_random_prob)

    def train(self, episodes=100):
        for i in xrange(episodes):
            self.train_episode(i)
        if self.show_progress:
            plt.show()

    ###########################################################################
    # OVERRIDE THE FOLLOWING METHODS
    ###########################################################################
    def save_data(self, name="rl"):
        with Timer():
            cr_handle = file(self.cumulative_reward_filename, "a")
            np.savetxt(cr_handle,
                       self.cumulative_reward[:-1], delimiter=",")
            self.cumulative_reward = self.cumulative_reward[-1:]

            ar_handle = file(self.avg_reward_filename, "a")
            np.savetxt(ar_handle, self.avg_reward[:-1], delimiter=",")
            self.avg_reward = self.avg_reward[-1:]

    def best_action(self, state):
        """Return index of best action given a state."""
        raise NotImplementedError()

    def learn(self, state, action, new_state, reward):
        raise NotImplementedError()
