import time

class timewith():
    def __init__(self, name=''):
        self.name = name
        self.start = time.time()
        self.last = self.start
        self.curr = self.start

    @property
    def elapsed(self):
        return self.curr - self.last

    def checkpoint(self, nitems=1):
        self.last = self.curr
        self.curr = time.time()
        if nitems == 0:
            return ('     {:14.8f} seconds'.format(self.elapsed) )
        else:
            return ('     {:14.8f} seconds  {:14.8f} per item'.format(self.elapsed, self.elapsed / nitems) )

    def finalize(self):
        self.curr = time.time()
        return ('     {:14.4f} seconds'.format(self.curr - self.start))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
