__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-02"
__version__ = "0.0.1"

from pmc.engine import Engine
from pmc.engine.peripherals import PeripheralDeviceHandler
from pmc.engine.peripherals.keyboard import KeyBoard
from pmc.engine.peripherals.mouse import Mouse

from pmc.render import Window
from pmc.render.renderer import Renderer

from pmc.game import SaveState

from pmc.world import World
from pmc.world.block import sectorize

from pmc.player import Player

from pyglet.app import run


class OfflineGame(Engine):
    def __init__(self, seed, savegame, name):
        super(OfflineGame, self).__init__()
        self.savingstate = SaveState(name=name)
        self.window = Window(self)
        self.renderer = Renderer(self)

        if not savegame:
            self.player = Player(self)
            self.world = World(self)
            self.world.create(seed)
        else:
            self.savingstate.savename = name
            self.player = Player(self)



        # self.renderer.overlay.inventory.create
        self.peripherals = PeripheralDeviceHandler(self)
        self.peripherals.add('keyboard', KeyBoard, (self,))
        self.peripherals.add('mouse', Mouse, (self,))
        self.peripherals.pushAll()
        self.run()

        run()

    def run(self): pass

    def update(self, dt):
        self.renderer.processQueue()
        sector = sectorize(self.player.position, self.data.physics.sector_size)
        if sector != self.renderer.sector:
            self.renderer.changeSectors(self.renderer.sector, sector)
            if self.renderer.sector is None: self.renderer.processEntireQueue()
            self.renderer.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in range(m): self.player.update(dt / m)


def start(startmethod): return OfflineGame(*startmethod)


if __name__ == '__main__': pass
