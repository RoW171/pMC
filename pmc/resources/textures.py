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

    @staticmethod
    def loadTextures(path):
        collection = Collection()
        collection.exception = TextureSetNotFound
        for name, file, in path.get().items():
            tset = file.unzip(['texture.png', 'coords'])
            collection[name] = TextureSet(texture=tset['texture.png'], coords=tset['coords'])
        return collection

    @staticmethod
    def loadSprites(path):
        collection = Collection()
        collection.exception = SpriteNotFound
        for name, file, in path.get().items(): collection[file.name] = load(str(file))
        return collection


class TextureSet(dict):
    def __init__(self, texture, coords): pass




if __name__ == '__main__': pass
