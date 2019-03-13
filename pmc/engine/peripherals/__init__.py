__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-12"
__version__ = "0.0.1"


class PeripheralDeviceHandler:
    def __init__(self, game):
        self.game = game
        self.devices = {}
        self.disabled = {}

    def add(self, device, enable=True):
        self.devices[device.__name__] = device
        if enable: self.enable(device.__name__)

    def enable(self, device):
        device = self.devices.get(device, None)
        if device is None: return
        self.game.window.push_handlers(device)
        try: del self.disabled[device.__name__]
        except (KeyError,): pass

    def disable(self, device):
        device = self.devices.get(device, None)
        if device is None: return
        self.game.window.remove_handler(device.__name__, device)
        self.disabled[device.__name__] = device


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

    def __repr__(self): return '{obj}-Device'.format(obj=type(self).__name__)

    __str__ = __repr__


if __name__ == '__main__': pass
