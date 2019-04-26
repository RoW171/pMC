__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-12"
__version__ = "0.0.1"


class PeripheralDeviceHandler:
    def __init__(self, game):
        self.game = game
        self.devices = {}

    def __getitem__(self, item): return self.devices[item]

    def __setitem__(self, key, value): self.devices[key] = value

    def __getattribute__(self, item):
        if item == 'game': return super().__getattribute__(item)
        else: return self.devices[item]

    def __setattribute__(self, key, value):
        if key == 'game': super().__setattrib__(key, value)
        else: self.devices[key] = value

    def add(self, name, device, *args): self.devices[name] = device(*args)

    def push(self, item): self.game.window.push_handlers(self.devices[item])

    def pushAll(self):
        for device in self.devices.values(): self.game.window.push_handlers(device)


def default(*args, **kwargs): pass


class PeripheralDevice(dict):
    def __init__(self, game, commands):
        super(PeripheralDevice, self).__init__()
        self.game = game

        for command in commands:
            if isinstance(command, tuple):
                name, d, start, = command
                d.update({None: default})
            else:
                name, d, start, = command, {None: default}, None,
            self[name] = d
            self.__dict__[name] = start

    def commands(self):
        c = self.__dict__.copy()
        c.remove('game')

    def __call__(self, **kwargs):
        for key, value, in kwargs.items(): self.__dict__[key] = value

    def __repr__(self): return '{obj}-Device'.format(obj=self.__class__.__name__)

    __str__ = __repr__


if __name__ == '__main__': pass
