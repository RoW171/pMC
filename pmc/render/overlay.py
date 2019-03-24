__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-24"
__version__ = "0.0.1"

from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.gl import GL_LINES, GL_QUADS


class Overlay:
    def __init__(self, game):
        self.game = game
        self.batch = Batch()

        self.width, self.height, = self.game.window.width, self.game.window.height,
        self.centerX, self.centerY, = self.width // 2, self.height // 2

        self.fpslist = []

        self.debug = DebugLabelHandler(self)
        self.saving = SavingLabelHandler(self)
        self.reticle = ReticleHandler(self)
        self.compass = CompassHandler(self)
        self.inventory = InventoryHandler(self)
        self.health = HealthHandler(self)
        self.endscreen = EndScreenHandler(self)

    def draw(self):
        self.debug()
        self.saving()
        self.reticle()
        self.compass()
        self.inventory()
        self.health()
        self.endscreen()

        self.batch.draw()

    __call__ = draw


class DebugLabelHandler:
    def __init__(self, overlay):
        self.overlay = overlay
        self.batch = self.overlay.batch
        self.debug_lbl = Label('', font_name='Consolas', font_size=12, color=(0, 0, 0, 255,), batch=self.batch,
                               x=10, y=self.overlay.height - 10, anchor_x='left', anchor_y='top')
        self.level = None
        self.setLevel(self.overlay.game.data.engine.core.debug_lvl)

    def __call__(self): self.level()

    def setLevel(self, lvl):
        if lvl == 0: self.level = self.level_0
        elif lvl == 1: self.level = self.level_1
        elif lvl == 2: self.level = self.level_2
        elif lvl == 3: self.level = self.level_3

    @staticmethod
    def fpsColor(fps):
        if fps >= 60: return 0, 0, 0, 255,
        elif fps >= 30: return 255, 120, 0, 255,
        else: return 255, 0, 0, 255,

    @staticmethod
    def level_0(): return

    def level_1(self):
            self.debug_lbl.begin_update()
            fps = self.overlay.game.clock.get_fps()
            self.debug_lbl.color = self.fpsColor(fps)
            self.debug_lbl.text = '%02d' % (fps,)
            self.debug_lbl.end_update()

    def level_2(self):
            self.debug_lbl.begin_update()
            fps = self.overlay.game.clock.get_fps()
            self.debug_lbl.color = self.fpsColor(fps)
            x, y, z, = self.overlay.game.player.position
            dy = self.overlay.game.player.dy
            r0, r1, = self.overlay.game.player.rotation
            self.debug_lbl.text = '%02d (%.2f, %.2f, %.2f // %.2f) (%.2f, %.2f) %d / %d (%.2f %s)' % (
                fps, x, y, z, dy, r0, r1,
                len(self.overlay.game.renderer.rendered), len(self.overlay.game.world),
                round(len(self.overlay.game.renderer.rendered) / len(self.overlay.game.world) * 100, 2), '%')
            self.debug_lbl.end_update()

    def level_3(self):
        self.level_2()
        self.overlay.fpslist.append(self.overlay.game.clock.get_fps())


class SavingLabelHandler:
    def __init__(self, overlay):
        self.overlay = overlay
        self.batch = self.overlay.batch
        self.counter = 0
        self.dots = ''
        self.saving_lbl = Label('', font_name='Consolas', font_size=20, color=(0, 0, 0, 255,),
                                batch=self.batch, anchor_x='center', anchor_y='center',
                                x=self.overlay.centerX, y=self.overlay.height - 30)

    def __call__(self):
        self.saving_lbl.begin_update()
        if self.overlay.game.savingstate.saving:
            self.counter += 1
            if self.counter % 5 == 0:
                if len(self.dots) == 3: self.dots = ''
                self.dots += '.'
            self.saving_lbl.text = 'speichert' + self.dots
        else: self.saving_lbl.text = ''
        self.saving_lbl.end_update()


class ReticleHandler:
    def __init__(self, overlay):
        self.overlay = overlay
        self.batch = self.overlay.batch
        self.flyshown = True
        self.reticle = self.batch.add(4, GL_LINES, None,
                                      ('v2i/static', self.getReticleCoords(self.overlay.centerX, self.overlay.centerY)),
                                      ('c4B/static', (0, 0, 0, 255,) * 4))
        self.flyframe = self.batch.add(8, GL_LINES, None,
                                       ('v2i/dynamic', (0,) * len(self.getFlyFrameCoords(self.overlay.centerX,
                                                                                         self.overlay.centerY))),
                                       ('c4B/static', (0, 0, 0, 255,) * 8))

    def __call__(self):
        if self.overlay.game.player.flying and not self.flyshown:
            self.flyshown = True
            self.flyframe.vertices[:] = self.getFlyFrameCoords(self.overlay.centerX, self.overlay.centerY)
        elif not self.overlay.game.player.flying and self.flyshown:
            self.flyshown = False
            self.flyframe.vertices[:] = (0,) * len(self.getFlyFrameCoords(self.overlay.centerX, self.overlay.centerY))

    @staticmethod
    def getReticleCoords(x, y, n=10): return (x - n, y,
                                              x + n, y,
                                              x, y - n,
                                              x, y + n,)

    @staticmethod
    def getFlyFrameCoords(x, y, n=30, m=50): return (x + n, y + n,
                                                     x + m, y,
                                                     x + m, y,
                                                     x + n, y - n,
                                                     x - n, y - n,
                                                     x - m, y,
                                                     x - m, y,
                                                     x - n, y + n,)


class EndScreenHandler:
    def __init__(self, overlay):
        self.overlay = overlay
        self.batch = self.overlay.batch
        self.sizeX, self.sizeY, = self.overlay.width // 4, self.overlay.height // 4,
        self.shown = True
        self.text = 'YOU DIED\n\npress [space] to close'
        self.endscreen = self.batch.add(4, GL_QUADS, None,
                                        ('v2i/static', (0,) * len(self.getCoords())),
                                        ('c4B/static', (100, 100, 100, 150,) * 4))
        self.endscreenLabel = Label('', font_name='Consolas', font_size=50, width=self.sizeX * 2,
                                    color=(200, 0, 0, 255,), batch=self.batch, anchor_x='center', anchor_y='center',
                                    x=self.overlay.centerX, y=self.overlay.centerY + 30, align='center', multiline=True)

    def __call__(self):
        if not self.overlay.game.player.alive and not self.shown:
            self.shown = True
            self.endscreen.vertices[:] = self.getCoords()
            self.endscreenLabel.begin_update()
            self.endscreenLabel.text = self.text
            self.endscreenLabel.end_update()
        elif self.overlay.game.player.alive and self.shown:  # if self.shown:
            self.shown = False
            self.endscreen.vertices[:] = (0,) * len(self.getCoords())
            self.endscreenLabel.begin_update()
            self.endscreenLabel.text = ''
            self.endscreenLabel.end_update()

    def getCoords(self): return (self.overlay.centerX - self.sizeX, self.overlay.centerY - self.sizeY,
                                 self.overlay.centerX + self.sizeX, self.overlay.centerY - self.sizeY,
                                 self.overlay.centerX + self.sizeX, self.overlay.centerY + self.sizeY,
                                 self.overlay.centerX - self.sizeX, self.overlay.centerY + self.sizeY)


class CompassHandler:
    def __init__(self, overlay):
        self.overlay = overlay
        compass_img = self.overlay.game.textures.sprites['compass']
        compass_img.anchor_x, compass_img.anchor_y, = compass_img.width // 2, compass_img.height // 2,
        self.compass = Sprite(compass_img, x=80, y=80, batch=self.overlay.batch)
        self.compass.scale = 0.5
        self.compass.visible = False

    def __call__(self):
        if self.overlay.game.player.showCompass:
            self.compass.visible = True
            angle = self.overlay.game.player.rotation[0]
            self.compass.rotation = angle % 360
        elif self.compass.visible: self.compass.visible = False


class HealthHandler(list):
    def __init__(self, overlay):
        super(HealthHandler, self).__init__()
        self.overlay = overlay
        self.batch = self.overlay.batch
        self.hidden = True
        self.heart = self.overlay.game.textures.sprites['heart']
        self.heart.anchor_x, self.heart.anchor_y, = self.heart.width // 2, self.heart.height // 2,
        self.half_heart = self.overlay.game.textures.sprites['half-heart']
        self.half_heart.anchor_x, self.half_heart.anchor_y, = self.half_heart.width // 2, self.half_heart.height // 2,
        scale = 0.2
        size = scale * 256
        offset = 10
        space = size * 5 + offset * 5
        start = self.overlay.width - space
        y = self.overlay.height - size * 0.8
        for _ in range(5):
            x = start + ((size + offset) * _)
            sprite = Sprite(self.heart, batch=self.batch, x=x, y=y)
            sprite.scale = scale
            sprite.visible = False
            self.append(sprite)

    def __call__(self):
        if self.overlay.game.data.game.gameplay.health_enabled:
            self.hidden = True
            health = self.overlay.game.player.health.get()
            health.reverse()
            for index, h in enumerate(health):
                if h == 0: self[index].visible = False
                elif h == 1:
                    self[index].image = self.half_heart
                    self[index].visible = True
                elif h == 2:
                    self[index].image = self.heart
                    self[index].visible = True
        elif self.hidden:
            self.hidden = False
            for h in self: h.visible = False


class InventoryHandler(list):
    def __init__(self, overlay):
        super(InventoryHandler, self).__init__()
        self.overlay = overlay
        self.batch = self.overlay.batch
        self.currentSlot = 1
        self.inventory = self.overlay.game.player.inventory

    def __call__(self):
        if self.overlay.game.player.showInventory:
            if len(self) > 0:
                if self.currentSlot != self.inventory.selectedIndex: self.updateSelection(self.inventory.selectedIndex)
            else: self.createSlot(self.inventory.selectedIndex)
        else: self.clear()

    def __getitem__(self, item): return super().__getitem__(item - 1)

    def __setitem__(self, key, value): super().__setitem__(key - 1, value)

    def updateSelection(self, index):
        self[self.currentSlot].unselect()
        self.currentSlot = index
        self[self.currentSlot].select()

    def createSlot(self, slotnumber):
        length = len(self.inventory)
        for index, slot in enumerate(reversed(self.inventory)):
            self.insert(0, InventorySlot(self, index + 1, (self.overlay.width - 100) - 120 * index, 100, slot.name, slot.get()))
            length -= 1
        self.updateSelection(slotnumber)


class InventorySlot:
    def __init__(self, handler, index, x, y, name, count=0, framesize=50):
        self.handler, self.index, = handler, index,
        self.x, self.y, = x, y,

        self.frame = self.createFrame(framesize)
        self.label = Label('{}\n{}'.format(name, count), anchor_x='center', anchor_y='center', align='center',
                           font_name='Impact', font_size=16, color=(255, 255, 255, 255), bold=False,
                           multiline=True, batch=self.handler.batch, width=100, height=100, x=x, y=100)

    def __del__(self):
        self.label.delete()
        self.frame.delete()

    def createFrame(self, size): return self.handler.batch.add(4, GL_QUADS, None,
                                                               ('v2i/static', (self.x - size, self.y - size,
                                                                               self.x + size, self.y - size,
                                                                               self.x + size, self.y + size,
                                                                               self.x - size, self.y + size,)),
                                                               ('c4B/static', (150, 150, 150, 180,) * 4))

    def updateText(self, selected=False, count=False):
        self.label.begin_update()
        if count: self.label.text = '{}\n{}'.format(self.handler.inventory[self.index].name,
                                                    self.handler.inventory[self.index].get())
        if selected: self.label.font_size = 18
        else: self.label.font_size = 16
        self.label.bold = selected
        self.label.end_update()

    def select(self):
        self.updateText(True)
        self.setFrame(True)

    def unselect(self):
        self.updateText(False)
        self.setFrame(False)

    def setFrame(self, selected):
        self.frame.delete()
        self.frame = self.createFrame(65 if selected else 50)


if __name__ == '__main__': pass
