import inspect
import time


class Timer(object):
    def __init__(self, name="", verbose=True):
        self.name = name or inspect.stack()[1][3]
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print '%s: %f ms' % (self.name, self.msecs)
