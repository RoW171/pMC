__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-12"
__version__ = "0.0.1"

from pmc.engine.peripherals import PeripheralDevice
from pyglet.window.key import *
from pyglet.window.key import _1, _2, _3, _4, _5, _6, _7, _8, _9, _0

numkeys = [_1, _2, _3, _4, _5, _6, _7, _8, _9, _0]
numpadkeys = [NUM_1, NUM_2, NUM_3, NUM_4, NUM_5, NUM_6, NUM_7, NUM_8, NUM_9, NUM_0]


commands_default = (
    ('press', {}, ''),
    ('release', {}, ''),
)


class KeyBoard(KeyStateHandler, PeripheralDevice):
    def __init__(self, game, commands=commands_default):
        super(KeyBoard, self).__init__(game, commands)

    def on_key_press(self, symbol, modifiers): self['press'][self.press](symbol, modifiers, self.game)

    def on_key_release(self, symbol, modifiers): self['release'][self.release](symbol, modifiers, self.game)


if __name__ == '__main__': pass
