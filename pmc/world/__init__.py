__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-17"
__version__ = "0.0.1"

from pmc.world.block import sectorize, normalize, FACES


class World(dict):
    def __init__(self, game):
        super(World, self).__init__()
        self.game = game
        self.textures = None
        self.shown, self.sectors, = dict(), dict(),

    def __getstate__(self):
        d = self.__dict__.copy()
        del d['game']
        del d['textures']
        return d

    def __setstate__(self, d):
        d['textures'] = None
        d['game'] = None
        self.__dict__ = d


if __name__ == '__main__': pass
