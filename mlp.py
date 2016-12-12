import sys
import numpy as np
import theano
import theano.tensor as T
from theano import shared
from theano import function
import six.moves.cPickle as pickle

# theano.config.optimizer="None"
theano.config.floatX = 'float64'


class MLP(object):

    def __init__(self, n_input, n_hidden, n_out, lr=0.3, lr_decay=1):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.n_out = n_out
        self.lr = lr

        lrs = shared(np.asarray(lr, dtype=theano.config.floatX))
        lr_decay = shared(np.asarray(lr_decay, dtype=theano.config.floatX))
        self.lrs = lrs

        rng = np.random.RandomState(1234)
        self.W0 = shared(np.asarray(rng.uniform(-0.1, 0.1, (n_input, n_hidden)), dtype=theano.config.floatX),
                         borrow=True,
                         name="self.W0")
        self.W1 = shared(np.asarray(rng.uniform(-0.1, 0.1, (n_hidden, n_out)), dtype=theano.config.floatX),
                         borrow=True,
                         name="self.W1")
        self.b0 = shared(np.asarray(rng.uniform(-0.1, 0.1, n_hidden), dtype=theano.config.floatX),
                         borrow=True,
                         name="self.b0")
        self.b1 = shared(np.asarray(rng.uniform(-0.1, 0.1, n_out), dtype=theano.config.floatX),
                         borrow=True,
                         name="self.b1")

        l0 = T.dmatrix("l0")
        l1 = T.tanh(T.dot(l0, self.W0) + self.b0)
        # l1 = T.nnet.relu(T.dot(l0,self.W0) + self.b0)
        # l1 = T.nnet.sigmoid(T.dot(l0,self.W0) + self.b0)
        # l1 = T.dot(l0,self.W0) + self.b0
        # l2 = T.nnet.relu(T.dot(l1,self.W1) + self.b1)
        # l2 = T.nnet.sigmoid(T.dot(l1,self.W1) + self.b1)
        # l2 = T.tanh(T.dot(l1,self.W1) + self.b1)
        l2 = T.dot(l1, self.W1) + self.b1

        x = l0
        y = T.dmatrix("y")
        W_penalization = 0.0001 * ((self.W0**2).sum() + (self.W1**2).sum())
        err = T.mean((l2 - y)**2)  # + W_penalization
        self.W_penalization = function([], W_penalization)

        g_W0 = T.grad(err, self.W0)
        g_W1 = T.grad(err, self.W1)
        g_b0 = T.grad(err, self.b0)
        g_b1 = T.grad(err, self.b1)
        self.train = function([x, y], err, updates=[
            (self.W0, self.W0 - lrs * g_W0),
            (self.W1, self.W1 - lrs * g_W1),
            (self.b0, self.b0 - lrs * g_b0),
            (self.b1, self.b1 - lrs * g_b1),
            (lrs, lrs * lr_decay)
        ])
        self.predict = function([x], l2)

    def clone(self):
        clon = MLP(self.n_input, self.n_hidden, self.n_out, self.lr)
        clon.W0.set_value(self.W0.get_value())
        clon.W1.set_value(self.W1.get_value())
        clon.b0.set_value(self.b0.get_value())
        clon.b1.set_value(self.b1.get_value())
        return clon

    def clone_in_existing_mlp(self, mlp):
        mlp.W0.set_value(self.W0.get_value())
        mlp.W1.set_value(self.W1.get_value())
        mlp.b0.set_value(self.b0.get_value())
        mlp.b1.set_value(self.b1.get_value())


if __name__ == "__main__":

    train_x = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ], dtype=theano.config.floatX)

    train_y = np.array([
        [0, 0],
        [1, 0],
        [1, 0],
        [0, 1]
    ], dtype=theano.config.floatX)

    if len(sys.argv) == 2:
        print "... Loading model from file ", sys.argv[1]
        with open(sys.argv[1], "rb") as f:
            mlp = pickle.load(f)
    else:
        print "... Creating model"
        mlp = MLP(2, 4, 2)

        print "... Training model"

        for i in xrange(300):
            sys.stdout.write(".")
            sys.stdout.flush()
            err = mlp.train(train_x, train_y)

        print "... Saving model"

        with open("xor_mlp.pkl", "wb") as f:
            pickle.dump(mlp, f)

    print "... Testing model"

    for i in zip(train_x, mlp.predict(train_x)):
        print i
