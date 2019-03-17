__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-10"
__version__ = "0.0.1"

from json import dump as jdump
from dill import dump as ddump, HIGHEST_PROTOCOL
from pathlib import Path
from time import sleep
from datetime import datetime
from random import Random
from os import walk
from configparser import ConfigParser
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
try: import zlib
except (ImportError,): comression = ZIP_STORED
else: compression = ZIP_DEFLATED


class update:
    REPO = 'https://raw.github.com/RoW171/pMC/master/'
    VERSIONFILE = Path('../../res/data/version')

    @staticmethod
    def create_version_file(version, notes='', state='stable'):
        date = datetime.now().date()
        info = {
            'meta': {
                'author': __author__,
                'date': str(date.year) + '-' + str(date.month) + '-' + str(date.day)
            },
            'version': {
                'version': version,
                'release': update.get_release_count() + 1,
                'notes': notes,
                'state': state
            },
            'paths': {
                'installed-version': str(update.VERSIONFILE)
            },
            'urls': {
                'repo': update.REPO,
                'version': update.REPO + 'res/data/version',
                'release': update.REPO + 'release/'
            }

        }
        with update.VERSIONFILE.open('w+') as sfile: jdump(info, sfile, indent=4)

    @staticmethod
    def get_release_count(directory='../../release'):
        suffix = ''
        release_number = -1
        for root, subs, files, in walk(directory):
            for file in files:
                temp_rel_number = int(file.split('_')[-1].replace(suffix, ''))
                if temp_rel_number > release_number: release_number = temp_rel_number
            break
        return release_number

    @staticmethod
    def pack_release(): pass


class rng:
    @staticmethod
    def create_new_pool(file, size=10):
        if not isinstance(file, Path): file = Path(file)
        if file.exists():
            pass  # TODO: warn here
        r = Random()
        l = []
        for _ in range(size):
            r.seed(datetime.now())
            l.append(r.getstate())
            sleep(1)
        with file.open('wb+') as sfile: ddump(l, sfile, HIGHEST_PROTOCOL)


class textures:
    @staticmethod
    def create_textureset(target, image, info, coorddata, ontop, fixed, lists):
        if not isinstance(target, Path): target = Path(target)
        if not isinstance(image, Path): image = Path(image)
        config = ConfigParser()
        for key, value, in info.items(): config['info'] = {key: value}
        for name, coords, in coorddata.items():
            config['coords'] = {name.upper(): ', '.join(list(map(lambda item: item.upper(), coords)))}
        for top, bottom, in ontop: config['on-top'] = {top.upper(): bottom.upper()}
        for name, tex, in fixed: config['fixed'] = {name: tex.upper()}
        for name, items, in lists: config['lists'] = {name: ''.join(list(map(lambda item: item.upper(), items)))}
        with Path(target).open('w') as configfile: config.write(configfile)

        zfile = ZipFile(str(target), mode='w', compression=compression)
        try:
            zfile.write(str(image), compress_type=compression)
            zfile.writestr('data', config, compress_type=compression)
        finally: zfile.close()

if __name__ == '__main__': pass
