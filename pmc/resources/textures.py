__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-23"
__version__ = "0.0.1"

from pyglet.image import load
from pmc.resources.io.config import Config

TSETVERSION = 0


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


class SpriteNotFound(Exception): pass


class Collection(dict):
    exception = None

    def __getitem__(self, item):
        try: return super().__getitem__(item)
        except (KeyError,): raise self.exception("TextureEngine: '{}' not found".format(item))


class TextureEngine:
    def __init__(self, texturePath, spritePath):
        self.selectedSet = None
        self.texturePath = texturePath
        self.spritePath = spritePath

        self.textures = self.loadTextures(self.texturePath)
        self.sprites = self.loadSprites(self.spritePath)

    def __getitem__(self, item):
        if self.selectedSet is None: return self.textures[item]
        else: return self.textures[self.selectedSet][item]

    def __setattr__(self, key, value):
        if key == 'selectedSet' and value is not None and value.corrupted:
            raise CorruptedTextureSet('')
        super(TextureEngine, self).__setattr__(key, value)

    @staticmethod
    def loadTextures(path):
        collection = Collection()
        collection.exception = TextureSetNotFound
        for name, file, in path.get().items():
            tset = file.unzip(['texture.png', 'data'])
            collection[name] = TextureSet(texture=tset['texture.png'], coords=tset['data'])
        return collection

    @staticmethod
    def loadSprites(path):
        collection = Collection()
        collection.exception = SpriteNotFound
        for name, file, in path.get().items(): collection[file.name] = load(str(file))
        return collection


class TextureSet(dict):
    def __init__(self, texture, coords):
        super(TextureSet, self).__init__()
        self.corrupted = False
        self.data = Config([coords.read().decode('utf-8')])
        self.texture = load(texture.name, file=texture).get_texture()
        if self.data.loadEntry('info', 'tset-version', 0, int) == TSETVERSION:
            try:
                self.texture_size = self.data.loadEntry('info', 'size', 4, int)
                for name in self.data.options('coords'):
                    top, bottom, side, = self.data.loadTexCoords(name)
                    self[name.upper()] = tex_coords(top, bottom, side, self.texture_size)

                for value in self.data.options('fixed'):
                    self.__dict__[value + '_name'] = self.data.loadEntry('fixed', value).upper()
                    self.__dict__[value] = tuple(self[self.__dict__[value + '_name']])

                for value in self.data.options('lists'):
                    self.__dict__[value + '_name'] = self.data.loadEntry('lists', value, None, list).upper()
                    self.__dict__[value] = tuple(self[self.__dict__[value + '_name']])

                for value in self.data.options('vlists'):
                    self.__dict__[value + '_name'] = self.data.loadEntry('vlists', value, None, list).upper()
                    l = list()
                    for item in self.__dict__[value + '_name']:
                        l.append(tuple(self[item]))
                    self.__dict__[value] = l

            except (Exception,): self.corrupted = True
            finally:
                self.data.close()
                self.texture.close()
        else: self.corrupted = True

    def __bool__(self): return not self.corrupted

    def getRandom(self, function, l): return self[function(l)]


if __name__ == '__main__': pass
