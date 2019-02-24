__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-24"
__version__ = "0.0.1"

from pyglet.window.event import WindowEventLogger


class WindowEventHandler(WindowEventLogger):
    def __init__(self, path):
        self.obj = path.open('w')
        super(WindowEventHandler, self).__init__(self.obj)

    def __del__(self): self.obj.close()


if __name__ == '__main__': pass
