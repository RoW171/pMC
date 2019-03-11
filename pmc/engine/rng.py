__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-11"
__version__ = "0.0.1"

from random import Random
from datetime import datetime
from pmc.resources.io import writeLine


class RNG(Random):
    def __init__(self, game, poolfile, logfile):
        self.game = game
        self._seed = int()
        self.pool = poolfile.unpack()
        self.logfile = logfile
        super(Random, self).__init__()

    def __repr__(self): return str(self._seed)

    __str__ = __repr__

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['game']
        return state

    def __setstate__(self, state):
        state['game'] = None
        self.__dict__ = state

    def createSeed(self):
        self.seed(datetime.now())
        return self.randint(1000000000, 9999999999)

    def setSeed(self, seed=None):
        # noinspection PyArgumentList
        manual = bool()
        if seed: seed = self.adjust(seed)
        else:
            manual = True
            seed = self.createSeed()
        self._seed = seed
        self.setstate(self.pool[self._seed % 10])
        self.log(self._seed, manual)
        self.seed(self._seed)

    __call__ = setSeed

    @staticmethod
    def adjust(nSeed, length=10):
        nSeed = str(nSeed)
        if nSeed.startswith('0'): nSeed = '1' + nSeed[:9]
        l = len(nSeed)
        if l < length: nSeed += ''.join(['0' for _ in range(length - l)])
        else: nSeed = nSeed[:length]
        return int(nSeed)

    def log(self, nSeed, manual=False):
        writeLine(self.logfile, '{} {} --- {}'.format('-' if manual else ' ', str(datetime.now())[:19], nSeed))


if __name__ == '__main__': pass
