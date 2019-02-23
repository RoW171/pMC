__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-23"
__version__ = "0.0.1"

from pyglet.media import Player, SourceGroup


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


if __name__ == '__main__': pass
