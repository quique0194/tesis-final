import numpy as np


class StateParser(object):

    ###########################################################################
    # OVERRIDE THE FOLLOWING METHODS
    ###########################################################################

    def dump(self):
        """Convert a state to a representation usable by learning."""
        raise NotImplementedError()

    def state_size(self):
        """Implement in case state is a np.array instead of an int."""
        return 1


class World(object):

    def __init__(self, actions, state_parser):
        self.actions = actions
        self.state_parser = state_parser

    def _exe_action(self, action):
        """To be called with state and action representations."""
        action = self.actions[action]
        new_state, reward = self.exe_action(action)
        return self.state_parser.dump(new_state), reward

    def _gen_random_state(self):
        state = self.gen_random_state()
        return self.state_parser.dump(state)

    def number_of_actions(self):
        return len(self.actions)

    def random_action(self):
        # Always return a number
        return np.random.randint(len(self.actions))

    ###########################################################################
    # OVERRIDE THE FOLLOWING METHODS
    ###########################################################################

    def exe_action(self, action):
        """
        Called with real action. Must return (new_state, reward).

        Must move World to the next step automatically
        """
        raise NotImplementedError()

    def isterminal(self):
        """To be called with a real state."""
        raise NotImplementedError()

    def number_of_states(self):
        raise NotImplementedError()

    def gen_random_state(self):
        raise NotImplementedError()
