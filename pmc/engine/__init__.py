__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-25"
__version__ = "0.0.1"

from pathlib import Path

# must run before any opengl or audio stuff
from pyglet import options
with Path('./res/data/internal').open('r') as internal:
    _data = list(map(lambda line: line.strip(), internal.readlines()))

gl_debug = bool(int(_data.pop(0)))
audio_drivers = tuple(_data)

options['audio'] = audio_drivers
options['debug_gl'] = gl_debug

from atexit import register
from pmc.resources import Ressources
from pmc.resources.settings import Settings
from pmc.resources.audio import AudioEngine
from pmc.resources.textures import TextureEngine


class Engine:
    def __init__(self):
        self.closemessage = []
        register(self.cleanup)

        self.resources = Ressources(Path('./res'))
        self.data = Settings(self.resources.data.settings)

        if 'client' not in self.__dict__: self.client = False

        self.window = None
        self.renderer = None
        if self.client: self.audio = AudioEngine(self.resources.audio, self.resources.libs.avbin)
        else: self.audio = None
        self.textures = TextureEngine(self.resources.textures, self.resources.img)
        self.world = None
        self.peripherals = None

    def cleanup(self, message=None):
        if message is None: message = self.closemessage
        print('-' * 10, 'cleanup', '-' * 10, sep='')
        for m in message: print(m, end='\n\n')
        # TODO: show average fps here later
        del self.resources
        del self.data
        del self.audio
        del self.textures
        del self.window
        del self.peripherals


if __name__ == '__main__': pass
