__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-24"
__version__ = "0.0.1"

from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.gl import GL_LINES, GL_QUADS


class Overlay:
    def __init__(self, game):
        self.game = game
        self.batch = Batch()

        self.width, self.height, = self.game.window.width, self.game.window.height,
        self.centerX, self.centerY, = self.width // 2, self.height // 2

        self.fpslist = []

    def draw(self): pass

    __call__ = draw


class DebugLabelHandler: pass


class SavingLabelHandler: pass


class ReticleHandler: pass


class EndScreenHandler: pass


class CompassHandler: pass


class HealthHandler(list): pass


class InventoryHandler(list): pass


class InventorySlot: pass


if __name__ == '__main__': pass
