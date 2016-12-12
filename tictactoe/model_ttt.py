
import copy

from model import World


class TicTacToeWorld(World):

    def __init__(self, dim, mark, opp, *args, **kwargs):
        self.dim = dim
        self.mark = mark
        self.opp = opp
        super(TicTacToeWorld, self).__init__(*args, **kwargs)

    def exe_action(self, state, action):
        new_state = copy.deepcopy(state)
        success = new_state.exe_action(action)
        if not success:
            return new_state, -1
        if new_state.winner() == self.mark:
            return new_state, 1
        if new_state.full() and new_state.winner() is None:
            return new_state, 0.5
        if not new_state.full():
            self.opp.play(new_state)
            winner = new_state.winner()
            if winner is not None and winner != self.mark:
                return new_state, -1
        return new_state, 0

    def isterminal(self, state):
        return state.finished()

    def number_of_states(self):
        return 3 ** (self.dim * self.dim)
