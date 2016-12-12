from model import StateParser

from model_ttt import TicTacToeWorld

from ql import QLearning

import tictactoe


class TicTacToeStateParser(StateParser):

    def __init__(self, dim, *args, **kwargs):
        self.dim = dim
        super(TicTacToeStateParser, self).__init__(*args, **kwargs)

    def dump(self, state):
        ret = 0
        for i, v in enumerate(state.data):
            ret += v * 3**i
        return ret

    def load(self, n):
        i = self.dim**2 - 1
        state = tictactoe.State(self.dim)
        while n != 0:
            d = 3**i
            state.data[i] = n // d
            n = n % d
            i -= 1
        return state


if __name__ == "__main__":
    DIM = 4
    MARK = "O"
    actions = []
    for pos in xrange(DIM**2):
        actions.append(tictactoe.Action(pos, MARK))

    opp = tictactoe.RandomPlayer("X")
    state_parser = TicTacToeStateParser(DIM)
    world = TicTacToeWorld(DIM, MARK, opp, actions, state_parser)
    qlearning = QLearning(world, state0=tictactoe.State(DIM))

    try:
        qlearning.train(4000)
    finally:
        print "SAVING FILES...",
        qlearning.save_data("graph/ql_ttt_" + str(DIM))
        print "DONE"
