__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-24"
__version__ = "0.0.1"

from configparser import ConfigParser
from io import StringIO, TextIOWrapper
from pathlib import Path


class Section:
    __config = None
    __name = str()
    __internal = ['__config', '__name', '__internal', '__ignore', '__path', '__laoding']

    def __getattribute__(self, item): return super(Section, self).__getattribute__(item)

    def __setattr__(self, key, value):
        if key not in self.__internal and not self.__config.__loading:
            self.__config.saveHintedEntry(self.__name, key, value)
        super(Section, self).__setattr__(key, value)

    __getitem__ = __getattribute__

    __setitem__ = __setattr__

    def __contains__(self, item): return item in self.__dict__


class Config(Section, ConfigParser):
    def __init__(self, path, ignoreExist=False, loadNow=True):
        super(Config, self).__init__()
        self.__ignore = ignoreExist
        self.__path = path
        self.__loading = False
        if loadNow: self(self.__path)

    def __call__(self, nFile=None):
        if isinstance(nFile, dict):
            self.read_dict(nFile)
            self.__path = 'dict'
        elif isinstance(nFile, (StringIO, TextIOWrapper,)):
            self.read_file(nFile)
            self.__path = 'memory: ' + str(nFile)
        elif isinstance(nFile, list):
            self.read_string(nFile.pop())
            self.__path = 'string'
        elif isinstance(nFile, str): nFile = Path(nFile)
        elif isinstance(nFile, Path):
            if not nFile.is_file():
                if self.__ignore: nFile.touch()
                else: raise FileNotFoundError("File '{}' not found".format(nFile))
            self.read(nFile)
            self.__path = nFile
        else: pass
        self.load()

    def __repr__(self): return str(self.__path)

    __str__ = __repr__

    def load(self):
        self.__loading = True
        for section in self.sections():
            s = Section()
            s.__config = self
            s.__name = section
            for option in self.options(section):
                s[option] = self.loadHintedEntry(section, option)
            self[section] = s
        self.__loading = False

    def loadEntry(self, section, option, fallback=None, datatype=str, subdatatype=str, chunksize=None):
        try:
            loadedItem = self.get(section, option, fallback=fallback)
            if datatype == list or datatype == tuple:
                loadedItem = loadedItem.replace('(', '').replace(')', '')
                if loadedItem == '': return datatype([])
                loadedItem = datatype(map(subdatatype, loadedItem.split(', ')))
                if chunksize is not None: loadedItem = datatype((zip(*[iter(loadedItem)] * chunksize)))
            elif datatype == bool: loadedItem = bool(int(loadedItem))
            else: loadedItem = datatype(loadedItem)
            return loadedItem
        except (Exception,): return fallback

    def loadHintedEntry(self, section, option, fallback=None, datatype=str, subdatatype=str, chunksize=None, sep='_'):
        hints = option.split(sep)
        clean = hints.pop(0)
        return self.loadEntry(section, option,
                              datatype=self.datatypes(hints.pop(0)) if len(hints) > 0 else datatype,
                              subdatatype=self.datatypes(hints.pop(0)) if len(hints) > 0 else subdatatype,
                              chunksize=int(hints.pop(0)) if len(hints) > 0 else chunksize,
                              fallback=hints.pop(0) if len(hints) > 0 else fallback,), clean,

    def save(self):
        with open(self.__path, 'w') as configfile: self.write(configfile)

    def saveEntry(self, section, option, value, saveToFile=True):
        if isinstance(value, (list, tuple,)):
            value = ', '.join(value)
        elif type(value) == bool:
            value = str(int(value))
        self[section] = {option: value}
        if saveToFile: self.save()

    def saveHintedEntry(self, section, option, value, sep='_', saveToFile=False):
        datatype = sep + self.datatypes(value)
        if isinstance(value, (list, tuple,)):
            subdatatype = sep + self.datatypes(value[0])
            if isinstance(value[0], (list, tuple,)):
                chunksize = sep + str(len(value[0]))
                subdatatype = sep + self.datatypes(value[0][0])
            else: chunksize = ''
        else:
            subdatatype = ''
            chunksize = ''
        self.saveEntry(section, option + datatype + subdatatype + chunksize, value, saveToFile=saveToFile)

if __name__ == '__main__': pass
