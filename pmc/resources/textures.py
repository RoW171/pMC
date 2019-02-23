__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-23"
__version__ = "0.0.1"

from pyglet.image import load


def tex_coord(x, y, n=4):
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m,


def tex_coords(top, bottom, side, map_size):
    tx, ty, = top
    bx, by, = bottom
    sx, sy, = side
    top = tex_coord(tx, ty, map_size)
    bottom = tex_coord(bx, by, map_size)
    side = tex_coord(sx, sy, map_size)
    return [top, bottom, side * 4]


class CorruptedTextureSet(Exception): pass


class TextureSetNotFound(Exception): pass




if __name__ == '__main__': pass
