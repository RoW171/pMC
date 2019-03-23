__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-20"
__version__ = "0.0.1"

from math import degrees, radians, sin, cos, atan2, sqrt
from pmc.player.health import Health
from pmc.player.inventory import Inventory
from pmc.resources.io.serializer import pickle


class Player:
    def __init__(self, game):
        self.game = game
        self.alive = True
        self.health = Health[self.game.data.gameplay.health_enabled]
        self.inventory = Inventory[self.game.data.gameplay.inventory_type]
        self.showInventory = False
        self.showCompass = False
        self.position = self.game.data.player.start_pos
        self.rotation = self.game.data.player.start_rot
        self.height = self.game.data.player.height
        self.strafe = [0, 0]
        self.dy = 0.0
        self.flying = False
        self.fallbffer = 0.0
        self.jump_speed = sqrt(2 * self.game.data.engine.physics.gravity * self.game.data.game.player.max_jump_height)

    def loadSaveData(self): pass

    def getSaveData(self):
        return {
            'health': pickle.dumpObject(self.health),
            'inventory': pickle.dumpObject(self.inventory),
            'position': self.position,
            'rotation': self.rotation,
            'height': self.height
        }

    def update(self, deltatime):
        if not -self.game.data.physics.map_reset < self.position[1] < self.game.data.physics.map_reset:
            self.position = (0, 5, 0,)
        speed = self.game.data.player.flying_speed if self.flying else self.game.data.player.walking_speed
        distance = speed * deltatime
        if not self.flying: pass
        dx, dy, dz, = tuple(i * distance for i in self.motionVector())
        x, y, z, = self.position
        self.position = self.game.world.collide(self, (x + dx, y + dy, z + dz,))

    __call__ = update

    def die(self):
        if self.game.data.gameplay.health_enabled and self.alive:
            self.alive = False
            # TODO: block input
            self.strafe = [0, 0]
            self.game.audio('die')
            if self.game.data.gameplay.save_on_death: self.game.save()

    def jump(self):
        if self.dy == 0:
            self.game.audio('jump')
            self.dy = self.jump_speed

    def stopFalling(self): self.dy = 0

    def toggleFlight(self): self.flying = not self.flying

    def sightVecor(self):
        x, y, = self.rotation
        x, y, = radians(x - 90), radians(y)
        m = cos(y)
        return cos(x) * m, sin(y), sin(x) * m,

    def motionVector(self):
        if any(self.strafe):
            x, y, = self.rotation
            strafe = degrees(atan2(*self.strafe))
            y_angle = radians(y)
            x_angle = radians(x + strafe)
            if self.flying:
                if self.strafe[1]: return cos(x_angle), 0.0, sin(x_angle)
                if self.strafe[0] > 0: return cos(x_angle) * cos(y_angle), -sin(y_angle), sin(x_angle) * cos(y_angle)
                else: return cos(x_angle) * cos(y_angle), sin(y_angle), sin(x_angle) * cos(y_angle)
            else: return cos(x_angle), 0.0, sin(x_angle),
        else: return 0.0, 0.0, 0.0,


if __name__ == '__main__': pass
