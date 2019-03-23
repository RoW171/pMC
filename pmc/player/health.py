__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-22"
__version__ = "0.0.1"

__all__ = ['Health']


class HealthBase:
    def __init__(self, player, health, dieFunc):
        self.player = player
        self.health = health
        self.dieFunc = dieFunc if dieFunc is not None else self.player.die

    def __call__(self, change=0): pass

    def __repr__(self): return str(self.health)

    __str__ = __repr__

    def suffer(self, modifier=1): pass

    def heal(self, modifier=1): pass


class HealthEnabled(HealthBase):
    def __init__(self, player, health=100, dieFunc=None): super(HealthEnabled, self).__init__(player, health, dieFunc)

    def get(self):
        result = []
        health = self.health / 20
        for h in range(1, 6):
            if health >= 1: result.append(2)
            elif health >= 0.5: result.append(1)
            else: result.append(0)
            health -= 1
        return result

    def suffer(self, modifier=1):
        self.player.game.audio('hurt')
        self(-modifier)

    def heal(self, modifier=1):
        self.player.game.audio('heal')
        self(modifier)


class HealthDisabled(HealthBase):
    def __init__(self, player, health=100, dieFunc=None): super(HealthDisabled, self).__init__(player, health, dieFunc)


Health = {
    True: HealthEnabled,
    False: HealthDisabled
}


if __name__ == '__main__': pass
