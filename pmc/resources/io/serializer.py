__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-24"
__version__ = "0.0.1"

from dill import dump, load, dumps, loads, HIGHEST_PROTOCOL, PicklingError, UnpicklingError


class DumpError(Exception): pass


class LoadError(Exception): pass


def dumpFile(path, saveObj):
    try:
        with path.open('wb+') as sfile: dump(saveObj, sfile, HIGHEST_PROTOCOL)
    except (UnpicklingError,): raise DumpError("failed to dump into the file '{}'".format(path))


def loadFile(path):
    try:
        with path.open('rb') as lfile: return load(lfile)
    except (PicklingError,): raise LoadError("failed to load the file '{}'".format(path))


def dumpObject(obj):
    try: return dumps(obj, HIGHEST_PROTOCOL)
    except (PicklingError,): raise DumpError('failed to dump the object')


def loadObject(obj):
    try: return loads(obj)
    except (UnpicklingError,): raise LoadError('failed to load the object')


if __name__ == '__main__': pass
