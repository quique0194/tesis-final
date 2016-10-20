import numpy as np
import matplotlib.pyplot as plt


class ReinforcementLearning(object):
    # Learning params
    discount_rate = 0.9
    random_prob = 1.0
    random_prob_decay = 0.95
    min_random_prob = 0.1

    # Interface params
    print_episodes = True
    show_progress = True
    train_info_steps = 10

    def __init__(self, world, state0):
        self.world = world
        self.state0 = self.world.state_parser.dump(state0)
        self.cumulative_reward = [0]

    def run_episode(self, state0):
        """ Run an episode from the initial state to a terminal state """
        state = state0
        while not self.world._isterminal(state):
            if np.random.rand() <= self.random_prob:
                action = self.world.random_action()
            else:
                action = self.best_action(state)
            new_state, reward = self.world._exe_action(state, action)
            self.cumulative_reward.append(self.cumulative_reward[-1] + reward)
            self.learn(state, action, new_state, reward)
            state = new_state

    def train_step(self, i):
        if i % self.train_info_steps == 0 and self.print_episodes:
            print "Episode", i
        if i % self.train_info_steps == 0 and self.show_progress:
            plt.cla()
            plt.plot(self.cumulative_reward)
            plt.draw()
            plt.pause(0.0001)
        self.run_episode(self.state0)
        self.random_prob *= self.random_prob_decay
        self.random_prob = max(self.random_prob, self.min_random_prob)

    def train(self, episodes=100):
        for i in xrange(episodes):
            self.train_step(i)
        if self.show_progress:
            plt.show()

    ###########################################################################
    # OVERRIDE THE FOLLOWING METHODS
    ###########################################################################

    def best_action(self, state):
        """ Return index of best action given a state """
        raise NotImplementedError()

    def learn(self, state, action, new_state, reward):
        raise NotImplementedError()
