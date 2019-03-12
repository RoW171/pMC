__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-12"
__version__ = "0.0.1"

from pmc.engine.peripherals import PeripheralDevice
from pyglet.window.mouse import *
from pyglet.window.key import MOD_CTRL


commands_default = (
    ('press', {}, ''),
    'release',
    ('motion', {}, ''),
    ('scroll', {}, ''),
)


class Mouse(PeripheralDevice):
    def __init__(self, game, commands=commands_default):
        super(Mouse, self).__init__(game, commands)

    def on_mouse_press(self, x, y, button, modifiers):
        self['press'][self.press](x, y, button, modifiers, self.game)

    def on_mouse_release(self, x, y, button, modifiers):
        self['release'][self.release](x, y, button, modifiers, self.game)

    def on_mouse_motion(self, x, y, dx, dy):
        self['motion'][self.motion](x, y, dx, dy, self.game)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self['scroll'][self.scroll](x, y, scroll_x, scroll_y, self.game)


if __name__ == '__main__': pass
