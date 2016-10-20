import numpy as np


class StateParser(object):

    ###########################################################################
    # OVERRIDE THE FOLLOWING METHODS
    ###########################################################################

    def load(self, n):
        """ Convert a state representation usable by learning to a state """
        raise NotImplementedError()

    def dump(self):
        """ Convert a state to a representation usable by learning """
        raise NotImplementedError()


class World(object):
    state_parser = StateParser()

    def __init__(self, actions):
        self.actions = actions

    def _exe_action(self, state, action):
        """ To be called with state and action representations """
        state = self.state_parser.load(state)
        action = self.actions[action]
        new_state, reward = self.exe_action(state, action)
        return self.state_parser.dump(new_state), reward

    def _isterminal(self, state):
        """ To be called with a state representation """
        state = self.state_parser.load(state)
        return self.isterminal(state)

    def number_of_actions(self):
        return len(self.actions)

    def random_action(self):
        # Always return a number
        return np.random.randint(len(self.actions))

    ###########################################################################
    # OVERRIDE THE FOLLOWING METHODS
    ###########################################################################

    def exe_action(self, state, action):
        """
            Called with real state and action
            Must return (new_state, reward)
        """
        raise NotImplementedError()

    def isterminal(self, state):
        """ To be called with a real state """
        raise NotImplementedError()

    def number_of_states(self):
        raise NotImplementedError()
