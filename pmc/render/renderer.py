__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-18"
__version__ = "0.0.1"

from pmc.world.block import cube_vertices
# from pmc.render.overlay import Overlay
from time import clock
from collections import deque
from pyglet.graphics import TextureGroup, Batch, draw
from pyglet.gl import GL_QUADS, glPolygonMode, GL_FRONT_AND_BACK, GL_LINE, GL_FILL


class Renderer:
    def __init__(self, game):
        self.game = game
        self.batch = Batch()
        self.group = TextureGroup(self.game.textures.texture)
        self.sector = None
        self.overlay = None
        self.rendered = {}
        self.queue = deque()

    def drawScene(self):
        self.batch.draw()
        self.drawFocusedBlock()

    __call__ = drawScene

    def drawFocusedBlock(self):
        block = self.game.world.hitTest(self.game.player.position, self.game.player.sightVector())[0]
        if block and self.game.world[block] != self.game.textures.edge:
            x, y, z, = block
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            draw(24, GL_QUADS, ('v3f/static', cube_vertices(x, y, z, 0.5),), ('c3B/static', (0, 0, 0,) * 24,))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def drawOverlay(self): self.overlay()

    def changeSectors(self, before, after):
        oldSector, newSector, = set(), set(),
        padding = 4
        for dx in range(-padding, padding + 1):
            for dy in range(-5, 7):
                for dz in range(-padding, padding + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (padding + 1) ** 2: continue
                    if before:
                        x, y, z, = before
                        oldSector.add((x + dx, y + dy, z + dz,))
                    if after:
                        x, y, z, = after
                        newSector.add((x + dx, y + dy, z + dz,))

        show = newSector - oldSector
        hide = oldSector - newSector
        for sector in show: self.game.world.showSector(sector)
        for sector in hide: self.game.world.hideSector(sector)

    def drawBlock(self, position, texture):
        x, y, z, = position
        self.rendered[position] = self.batch.add(24, GL_QUADS, self.group,
                                                 ('v3f/static', cube_vertices(x, y, z, 0.5),),
                                                 ('t2f/static', list(texture),))

    def undrawBlock(self, position): self.rendered.pop(position).delete()

    def enqueue(self, func, *args): self.queue.append((func, args,))

    def dequeue(self):
        func, args, = self.queue.popleft()
        func(*args)

    def processQueue(self):
        start = clock()
        while self.queue and clock() - start < 1.0 / self.game.data.engine.ticks: self.dequeue()

    def processEntireQueue(self):
        while self.queue: self.dequeue()


if __name__ == '__main__': pass
