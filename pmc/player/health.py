__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-22"
__version__ = "0.0.1"


class Health:
    def __init__(self, controller, health=100, dieFunc=None):
        self.controller = controller
        self.health = health
        self.dieFunc = dieFunc if dieFunc is not None else self.controller.die

        if self.controller.data.gameplay.health_enabled:
            self.heal = self.healEnabled
            self.suffer = self.sufferEnabled
            Health.__call__ = self.callEnabled
        else:
            self.heal = self.healDisabled
            self.suffer = self.sufferDisabled
            Health.__call__ = self.callDisabled

    def __repr__(self): return str(self.health)

    __str__ = __repr__

    def get(self):
        result = []
        health = self.health / 20
        for h in range(1, 6):
            if health >= 1: result.append(2)
            elif health >= 0.5: result.append(1)
            else: result.append(0)
            health -= 1
        return result

    def callEnabled(self, change=0):
        self.health += change * 10
        if self.health <= 0: self.dieFunc()
        return self.health

    def sufferEnabled(self, modifier=1):
        self.controller.game.audio('hurt')
        self(-modifier)

    def healEnabled(self, modifier=1):
        self.controller.game.audio('heal')
        self(modifier)

    def callDisabled(self, change=0): pass

    def sufferDisabled(self, modifier=1): pass

    def healDisabled(self, modifier=1): pass


if __name__ == '__main__': pass
