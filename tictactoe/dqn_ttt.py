from dqn import DQN
from model import StateParser
from model_ttt import TicTacToeWorld
import numpy as np
import tictactoe


class TicTacToeStateParser(StateParser):

    def __init__(self, dim, *args, **kwargs):
        self.dim = dim
        super(TicTacToeStateParser, self).__init__(*args, **kwargs)

    def dump(self, state):
        ret = []
        for mark in state.data:
            temp = [0, 0]
            if mark == 1:
                temp[0] = 1
            elif mark == 2:
                temp[1] = 1
            ret += temp
        return np.array(ret)

    def load(self, n):
        state = tictactoe.State(self.dim)
        sublists = [n[i:i + 2] for i in xrange(0, len(n), 2)]
        for i, temp in enumerate(sublists):
            if temp[0]:
                state.data[i] = 1
            elif temp[1]:
                state.data[i] = 2
        return state

    def state_size(self):
        return 2 * (self.dim * self.dim)


if __name__ == "__main__":
    DIM = 4
    MARK = "O"
    actions = []
    for pos in xrange(DIM**2):
        actions.append(tictactoe.Action(pos, MARK))

    opp = tictactoe.RandomPlayer("X")
    state_parser = TicTacToeStateParser(DIM)
    world = TicTacToeWorld(DIM, MARK, opp, actions, state_parser)
    rl = DQN(world, state0=tictactoe.State(DIM))

    rl.buffer_size = 10000
    rl.batch_size = 100
    rl.clone_network_steps = 50

    try:
        rl.train(4000)
    finally:
        print "SAVING FILES...",
        rl.save_data("graph/dqn_ttt_" + str(DIM))
        print "DONE"
