__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-17"
__version__ = "0.0.1"

from pmc.world.block import sectorize, normalize, FACES


class World(dict):
    def __init__(self, game):
        super(World, self).__init__()
        self.game = game
        self.textures = self.game.textures
        self.shown, self.sectors, = dict(), dict(),

    def getSaveData(self):
        data = self.__dict__.copy()
        del data['game'], data['textures']
        data['world'] = self.copy()
        return data

    def load(self, data):
        self.update(data.pop('world'))
        self.shown = data['shown']
        self.sectors = data['sectors']
        for position, texture, in self.items(): self.addBlock(position, texture, immediate=position in self.shown)

    def collision(self, player, position, padding=None):
        if padding is None: padding = self.game.data.engine.physics.collision_padding
        position = list(position)
        normalposition = normalize(position)
        for face in FACES:
            for axis in range(3):
                if not face[axis]: continue
                distance = (position[axis] - normalposition[axis]) * face[axis]
                if distance < padding: continue
                for heightUnit in range(player.height):
                    np = list(normalposition)
                    np[1] -= heightUnit
                    np[axis] += face[axis]
                    if tuple(np) not in self: continue
                    position[axis] -= (distance - padding) * face[axis]
                    if face == (0, -1, 0,) or face == (0, 1, 0,): player.stopFalling()
                    break
        return tuple(position)

    def hitTest(self, position, vector, maxDistance=None):
        if maxDistance is None: maxDistance = self.game.data.game.player.arm_range
        m = 8
        x, y, z, = position
        vx, vy, vz, = vector
        previous = None
        for _ in range(maxDistance * m):
            block = normalize((x, y, z,))
            if block != previous and block in self: return block, previous,
            previous = block
            x, y, z, = x + vx / m, y + vy / m, z + vz / m,
        return None, None,

    def exposed(self, position, sides=FACES):
        x, y, z, = position
        for dx, dy, dz, in sides:
            if (x + dx, y + dy, z + dz,) not in self or self[(x + dx, y + dy, z + dz,)] in self.textures.transparent:
                return True
        else: return False

    def checkNeighbors(self, position):
        x, y, z, = position
        for dx, dy, dz, in FACES:
            block_coords = (x + dx, y + dy, z + dz,)
            if block_coords not in self: continue
            if self.exposed(block_coords):
                if block_coords not in self.shown: self.showBlock(block_coords)
            elif block_coords in self.shown: self.hideBlock(block_coords)

    def addBlock(self, position, texture, immediate=True):
        texture = tuple(texture)
        if not self.exposed(position, [(0, 1, 0,)]) and texture in self.textures.ontop_rules:
            self[position] = self.textures.ontop_rules[texture]
        else: self[position] = texture
        self.sectors.setdefault(sectorize(position, self.game.data.engine.physics.sector_size), []).append(position)
        if immediate:
            if self.exposed(position): self.showBlock(position)
            self.checkNeighbors(position)

    def removeBlock(self, position, immediate=True):
        del self[position]
        self.sectors[sectorize(position, self.game.data.engine.physics.sector_size)].remove(position)
        if immediate:
            if position in self.shown: self.hideBlock(position)
            self.checkNeighbors(position)

    def showBlock(self, position, immediate=True):
        try: texture = self[position]
        except (KeyError,): return
        self.shown[position] = texture
        if immediate: self.game.renderer.drawBlock(position, texture)
        else: self.game.renderer.enqueue(self.game.renderer.drawBlock, position, texture)

    def hideBlock(self, position, immediate=True):
        self.shown.pop(position)
        if immediate: self.game.renderer.undrawBlock(position)
        else: self.game.renderer.enqueue(self.game.renderer.undrawBlock, position)

    def showSector(self, sector):
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position): self.showBlock(position, False)

    def hideSector(self, sector):
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position): self.hideBlock(position, False)


if __name__ == '__main__': pass
