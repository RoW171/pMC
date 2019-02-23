__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-23"
__version__ = "0.0.1"

from pyglet.media import load, Player, SourceGroup
from pyglet.media.drivers.base import AbstractAudioDriver
from pyglet.lib import load_library
import pyglet


class AudioFileNotFound(FileNotFoundError): pass


class AmbientPlayer(Player):
    def __init__(self, engine):
        self.engine = engine
        super(AmbientPlayer, self).__init__()

    def __repr__(self): return 'AmbientPlayer, now playing: {}'.format(self.source.__name__ if self else 'None')

    __str__ = __repr__

    def __bool__(self): return self.playing

    def __float__(self): return self.volume

    def queue(self, source):
        source = self.engine[source]
        looper = SourceGroup(source.audio_format, None)
        looper.loop = True
        looper.queue(source)
        super(AmbientPlayer, self).queue(looper)

    __call__ = queue

    def __iadd__(self, other):
        self.volume += other
        return self

    def __isub__(self, other):
        self.volume -= other
        return self


class AudioEngine(dict):
    def __init__(self, audioPath, avbinPath=None):
        super(AudioEngine, self).__init__()
        self.audioPath = audioPath
        if avbinPath:
            load_library(str(avbinPath))
            pyglet.has_avbin = True
        self._volume = 1.0
        self.listener = AbstractAudioDriver.get_listener()

        self.ambientPlayer = AmbientPlayer(self)

    def __call__(self, item):
        try: self[item].play()
        except (KeyError,): raise AudioFileNotFound("'{}' was not loaded into the audioengine".format(item))

    def __repr__(self): return 'AudioEngine, volume: {}'.format(self.volume)

    __str__ = __repr__

    def __float__(self): return self.volume

    def __delitem__(self, key): self[key].delete()

    def append(self, name, item): self[name] = load(str(item), streaming=False)

    def load(self):
        for name, file, in self.audioPath.get().items(): self.append(name, file)

    @property
    def volume(self): return self._volume

    @volume.setter
    def volume(self, nVolume):
        if 0 < nVolume < 1:
            self._volume = nVolume
            self.listener.volume = self._volume

    def __iadd__(self, other):
        self.volume += other
        return self

    def __isub__(self, other):
        self.volume -= other
        return self


if __name__ == '__main__': pass
