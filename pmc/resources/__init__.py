__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-23"
__version__ = "0.0.1"

from pathlib import Path
from shutil import rmtree
from os import walk, remove
from pmc.resources.io.serializer import loadFile
from pmc.resources.io.zipper import openZip
from pmc.resources.io.config import Config
from pmc.resources.io.sql import DataBase
from pmc.resources.io.markup import XML


class Base:
    path = None
    parent = None

    def __getattribute__(self, item): return super().__getattribute__(item)

    __getitem__ = __getattribute__

    def __repr__(self): return '{} at location \'{}\''.format(type(self).__name__, self.path)

    __str__ = __repr__

    def createFile(self, name, ignore=False): pass

    def createDirectory(self, name, ignore=False): pass

    def remove(self):
        if self.path.is_dir():
            assert rmtree(str(self.path)) != -1
        else:
            assert remove(str(self.path)) != -1
        del self.parent.__dict__[self.path.stem]


class Directory(Base):
    def __init__(self, name, path, parent):
        self.path = Path(path).resolve() / name
        self.parent = parent
        self.ignore = []

    def get(self):
        d = self.__dict__.copy()
        del d['path']
        for i in self.ignore: del d[i]
        del d['ignore']
        del d['parent']
        return d

    def __len__(self): return len(self.__dict__) - 3 - len(self.ignore)

    def count(self, instance):
        if instance == 'dir': instance = Directory
        if instance == 'file': instance = File
        counter = 0
        for item in self.get().values():
            if isinstance(item, instance): counter += 1
        return counter

    def loadIgnore(self):
        if 'resignore' in self.__dict__:
            with self['resignore'].open() as ignores:
                for file in ignores.readlines():
                    del self.__dict__[Path(file.strip()).stem]
                    # del self.__dict__['.'.join(file.split('.')[:-1])]
            del self.__dict__['resignore']

    def createFile(self, name, ignore=False):
        path = self.path / name
        # if not ignore and path.is_file(): raise FileExistsError
        path.touch(exist_ok=ignore)
        self.__dict__[Path(name).stem] = File('', path, self)
        return self.__dict__[Path(name).stem]

    def createDirectory(self, name, ignore=False):
        path = self.path / name
        if not ignore and path.is_dir(): raise IsADirectoryError
        path.mkdir()
        self.__dict__[name] = Directory('', path, self)

    @property
    def size(self): return sum([f.size for f in self.get().values()])


class File(Base):
    def __init__(self, name, path, parent):
        self.path = Path(path).resolve() / name
        self.parent = parent
        self.name = self.path.stem
        self.suffix = self.path.suffix
        self.size = int()
        self.times = dict()
        self.update()

    def update(self):
        stats = self.path.stat()
        self.size = stats.st_size
        self.times = {
            'creation': stats.st_ctime,
            'modified': stats.st_mtime,
        }
        # TODO: maybe add other stuff later

    def get(self): return self

    def open(self, mode='r', **kwargs): return self.path.open(mode, **kwargs)

    def unzip(self, itest=None, checkzip=True): return openZip(self.path, itest, checkzip)

    def unpack(self): return loadFile(self.path)

    def openConfig(self): return Config(self.path)

    def openXML(self): return XML(self.path)

    def openSQL(self): return DataBase(self.path)


class Ressources(Directory):
    def __init__(self, path):
        super(Ressources, self).__init__('', '', None)
        self.path = Path(path)
        self.traverse(self, self.path)

    def traverse(self, obj, path):
        for root, subs, files, in walk(str(path)):
            for file in files: obj.__dict__[Path(file).stem] = File(file, root, obj)
            for sub in subs:
                obj.__dict__[sub] = Directory(sub, root, obj)
                self.traverse(obj.__dict__[sub], Path(root) / sub)
                obj.__dict__[sub].loadIgnore()
            break

    def remove(self): pass


if __name__ == '__main__': pass
