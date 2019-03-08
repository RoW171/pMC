__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-24"
__version__ = "0.0.1"

from dill import dump as ddump, load as dload, dumps as ddumps, loads as dloads, HIGHEST_PROTOCOL, PicklingError, UnpicklingError
from json import dump as jdump, load as jload, dumps as jdumps, loads as jloads


class DumpError(Exception): pass


class LoadError(Exception): pass


class pickle:
    @staticmethod
    def dumpFile(path, saveObj):
        try:
            with path.open('wb+') as sfile: ddump(saveObj, sfile, HIGHEST_PROTOCOL)
        except (UnpicklingError,): raise DumpError("failed to dump into the file '{}'".format(path))

    @staticmethod
    def loadFile(path):
        try:
            with path.open('rb') as lfile: return dload(lfile)
        except (PicklingError,): raise LoadError("failed to load the file '{}'".format(path))

    @staticmethod
    def dumpObject(obj):
        try: return ddumps(obj, HIGHEST_PROTOCOL)
        except (PicklingError,): raise DumpError('failed to dump the object')

    @staticmethod
    def loadObject(obj):
        try: return dloads(obj)
        except (UnpicklingError,): raise LoadError('failed to load the object')


class json:
    @staticmethod
    def dumpFile(path, saveObj, **kwargs):
        try:
            with path.open('w+') as sfile: jdump(saveObj, sfile, **kwargs)
        except (UnpicklingError,): raise DumpError("failed to dump into the file '{}'".format(path))

    @staticmethod
    def loadFile(path, **kwargs):
        try:
            with path.open('r') as lfile: return jload(lfile, **kwargs)
        except (PicklingError,): raise LoadError("failed to load the file '{}'".format(path))

    @staticmethod
    def dumpObject(obj, **kwargs):
        try: return jdumps(obj, **kwargs)
        except (PicklingError,): raise DumpError('failed to dump the object')

    @staticmethod
    def loadObject(obj, **kwargs):
        try: return jloads(obj, **kwargs)
        except (UnpicklingError,): raise LoadError('failed to load the object')


if __name__ == '__main__': pass
