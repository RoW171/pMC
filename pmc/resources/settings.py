__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-24"
__version__ = "0.0.1"

from pmc.resources.io.serializer import json


class SettingsFile(dict):
    def __init__(self, file):
        self._file = file
        super(SettingsFile, self).__init__(self.load())

    def __getattribute__(self, item):
        if item in ['_file', 'load', 'save']: return super(SettingsFile, self).__getattribute__(item)
        else: return super(SettingsFile, self).__getitem__(item.replace('_', '-'))

    def __setitem__(self, key, value):
        super(SettingsFile, self).__setitem__(key.replace('_', '-'), value)
        self.save()

    __setattribute__ = __setitem__

    def load(self): return self._file.json()

    def save(self): self._file.json(self.copy())


class Settings:
    def __init__(self, settingsPath):
        for name, file, in settingsPath.get().items():
            self.__dict__[name] = SettingsFile(file)

    def __len__(self): return len(self.__dict__)

    def __bool__(self): return bool(self.__dict__)

    def __contains__(self, item): return item in self.__dict__

    def __getitem__(self, item): return self.__getattribute__(item)


if __name__ == '__main__': pass
