__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-13"
__version__ = "0.0.1"

from pyglet.window import Window as GameWindow, get_platform
from pyglet.gl import *
from math import sin, cos, radians


class Window(GameWindow):
    def __init__(self, game):
        self.game = game
        screen = get_platform().get_default_display().get_default_screen()
        super(Window, self).__init__(caption='pMC',
                                     width=screen.width, height=screen.height,
                                     resizable=False, fullscreen=True,
                                     vsync=False)  # TODO: add settings look-up here
        self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR))
        self.set_icon(self.game.textures.sprites['ico16'], self.game.textures.sprites['ico32'])
        self.exclusive = False
        self.setExclusive(True)

        self.register_event_type('on_draw')
        self.register_event_type('on_resize')

    def on_draw(self):
        self.clear()
        self.mode_3d()
        self.game.renderer()
        self.mode_2d()
        self.game.renderer.overlay()

    def mode_2d(self):
        width, height, = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def mode_3d(self):
        width, height, = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.game.data.engine.rendering.fov,
                       width / float(height),
                       self.game.data.engine.rendering.perspective_near,
                       self.game.data.engine.rendering.perspective_far)
        # TODO: second is nearest third is farest, tweak those, especially the latter
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        rx, ry, = self.game.player.rotation
        glRotatef(rx, 0, 1, 0)
        glRotatef(-ry, cos(radians(rx)), 0, sin(radians(rx)))
        x, y, z, = self.game.player.position
        glTranslatef(-x, -y, -z)

    def setup(self):
        glClearColor(*self.game.data.game.world.sky_color)
        glEnable(GL_CULL_FACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        if self.game.data.engine.rendering.antialiasing:
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        magnification = GL_NEAREST if self.game.data.engine.rendering.magnification == 'near' else GL_LINEAR
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, magnification)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magnification)
        if self.game.data.game.world.fog_enabled: self.setup_fog()

    def setup_fog(self):
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (GLfloat * 4)(*self.game.data.game.world.sky_color))
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, self.game.data.engine.rendering.fog_start)
        glFogf(GL_FOG_END, self.game.data.engine.rendering.fog_end)

    def setExclusive(self, state):
        super(Window, self).set_exclusive_mouse(state)
        self.exclusive = state

    def toggleExclusive(self): self.setExclusive(not self.exclusive)


if __name__ == '__main__': pass
