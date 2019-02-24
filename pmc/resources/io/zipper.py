__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-24"
__version__ = "0.0.1"

from datetime import datetime
from atexit import register
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
try: import zlib
except (ImportError,): comression = ZIP_STORED
else: compression = ZIP_DEFLATED


class ZipFileDamagedError(Exception):
    def __init__(self, file, occurance):
        print('zipfile \'{}\' is damaged, first error at {}'.format(file, occurance))


class ZipFileIntegrityError(Exception):
    def __init__(self, file, test, found, length, names):
        print('zipfile integrity check failed')
        print('file: ', file)
        print('test: ', test)
        print('found: ', found)
        print('number of content identical:', length)
        print('content names identical:', names)


class ZipFileContents(dict):
    def __init__(self):
        super(ZipFileContents, self).__init__()
        register(self.close)

    def __delitem__(self, key): self[key].close()

    def close(self):
        for fileobject in self.values():
            try: fileobject.close()
            except (AttributeError,): continue


def print_info(archive):
    file = ZipFile(archive, 'r')
    print(file.comment)
    for info in file.infolist():
        print(info.filename)
        print('\tComment:\t', info.comment)
        print('\tModified:\t', datetime(*info.date_time))
        print('\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)')
        print('\tZIP version:\t', info.create_version)
        print('\tCompressed:\t', info.compress_size, 'bytes')
        print('\tUncompressed:\t', info.file_size, 'bytes')


def createZip(targetpath, contents, comment=''):
    zfile = ZipFile(str(targetpath), mode='w', compression=compression)
    zfile.comment = bytes(comment, 'utf-8')
    try:
        for name, file, in contents: zfile.writestr(name, file, compression)
    finally: zfile.close()


def openZip(file, itest=None, checkzip=True):
    zfile = ZipFile(str(file), mode='r')
    contents = ZipFileContents()
    names = zfile.namelist()
    if itest and len(names) != len(itest) and set(names) != set(itest):
        raise ZipFileIntegrityError(file, itest, names, len(names) == len(itest), set(names) == set(itest))
    elif checkzip:
        dtest = zfile.testzip()
        if dtest is not None: raise ZipFileDamagedError(file, dtest)
    for name in zfile.namelist(): contents[name] = zfile.open(name)
    return contents


if __name__ == '__main__': pass
