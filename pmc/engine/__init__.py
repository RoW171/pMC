__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-25"
__version__ = "0.0.1"

from pathlib import Path

# must run before any opengl or audio stuff
from pyglet import options
with Path('./res/data/internal').open('r') as internal: _data = ''.join(internal.readlines()).split('\n')
gl_debug = bool(int(_data.pop(0)))
audio_drivers = tuple(_data)

options['audio'] = audio_drivers
options['debug_gl'] = gl_debug


if __name__ == '__main__': pass
