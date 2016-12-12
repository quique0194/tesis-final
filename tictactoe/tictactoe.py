import copy
import numpy as np

# 0 | 1 | 2
# 3 | 4 | 5
# 6 | 7 | 8

# Empty: 0
# X: 1
# O: 2


class Action(object):
    pos = None  # [0, ..., 8]
    mark = None  # 'X' or 'O'

    def __init__(self, pos, mark):
        mark = mark.upper()
        assert(mark == 'X' or mark == 'O')
        self.pos = pos
        self.mark = mark


class State(object):

    def __init__(self, dim=3):
        self.dim = dim
        self.data = [0] * (dim ** 2)

    def get_empty_boxes(self):
        ret = []
        for i, val in enumerate(self.data):
            if val == 0:
                ret.append(i)
        return ret

    def inv(self):
        inv_state = copy.deepcopy(self)
        for i, val in enumerate(self.data):
            if inv_state.data[i] == 1:
                inv_state.data[i] = 2
            elif inv_state.data[i] == 2:
                inv_state.data[i] = 1
        return inv_state

    def winner(self):
        def equal(l):
            for i in l:
                if i != l[0]:
                    return False
            return True

        # check rows
        for i in range(self.dim):
            row = []
            for j in range(self.dim):
                row.append(self.data[self.dim * i + j])
            if equal(row) and row[0]:
                return self.to_mark(row[0])
        # check columns
            col = []
            for j in range(self.dim):
                col.append(self.data[self.dim * j + i])
            if equal(col) and col[0]:
                return self.to_mark(col[0])
        # check diagonal
        diag1 = []
        diag2 = []
        for i in range(self.dim):
            diag1.append(self.data[self.dim * i + i])
            diag2.append(self.data[self.dim * i + (self.dim - i - 1)])
        if equal(diag1) and diag1[0]:
            return self.to_mark(diag1[0])
        if equal(diag2) and diag2[0]:
            return self.to_mark(diag2[0])

        return None

    def full(self):
        for i in self.data:
            if i == 0:
                return False
        return True

    def finished(self):
        return self.full() or (self.winner() is not None)

    def to_mark(self, val):
        if val == 1:
            return "X"
        elif val == 2:
            return "O"
        else:
            return "-"

    def from_mark(self, mark):
        if mark == "X":
            return 1
        elif mark == "O":
            return 2
        else:
            return 0

    def exe_action(self, action):
        assert(type(action) == Action)
        if self.data[action.pos] == 0:
            self.data[action.pos] = self.from_mark(action.mark)
            return 1
        return 0

    def __repr__(self):
        ret = ""
        for i, val in enumerate(self.data):
            ret += str(self.to_mark(val))
            if (i + 1) % 3 == 0:
                ret += '\n'
        return ret


#############################################################
# PLAYERS
#############################################################


class Player(object):

    def __init__(self, mark):
        assert(type(mark) == str)
        self.mark = mark

    def on_finish(self, winner):
        pass


class RandomPlayer(Player):

    def play(self, state):
        options = state.get_empty_boxes()
        pos = np.random.choice(options)
        a = Action(pos, self.mark)
        state.exe_action(a)
        return a


class HumanPlayer(Player):

    def play(self, state):
        print state
        exe = False
        while not exe:
            pos = raw_input("Jugar[0-8]:")
            a = Action(int(pos), self.mark)
            exe = state.exe_action(a)
        return a

#############################################################
# INTERFACE
#############################################################


def game(p1, p2):
    s = State()
    while True:
        p1.play(s)
        if s.winner() or s.full():
            break
        p2.play(s)
        if s.winner() or s.full():
            break
    p1.on_finish(s.winner())
    p2.on_finish(s.winner())
    return s.winner()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'auto':
        p1 = RandomPlayer("X")
        p2 = RandomPlayer("O")
    else:
        p1 = RandomPlayer("X")
        p2 = HumanPlayer("O")

    game(p1, p2)
