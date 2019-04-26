__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-02"
__version__ = "0.0.1"


class InvalidSaveGameName(Exception): pass


class SaveState:
    def __init__(self, state=False, name=None):
        self.saving = state
        self.savename = name

    def __call__(self): self.saving = not self.saving

    def __repr__(self): return str(self.saving)

    __str__ = __repr__

    def __setattr__(self, key, value):
        if key is 'savename' and value is not None and value.isdigit():
            raise InvalidSaveGameName('Savegames cannot only consist out of digits')
        else: return super(SaveState, self).__setattr__(key, value)

    @staticmethod
    def get(parent):
        pass
        # if isinstance()


if __name__ == '__main__': pass
