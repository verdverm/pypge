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
            print '     {:14.8f} seconds'.format(self.elapsed)
        else:
            print '     {:14.8f} seconds, {:14.8f} per item'.format(self.elapsed, self.elapsed / nitems)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.curr = time.time()
        print '  TOTAL {:14.3f} seconds'.format(self.curr - self.start)
        pass
