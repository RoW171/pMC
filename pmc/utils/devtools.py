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
    def pack_release(version, notes='', directory=Path('../../release')):
        # update.create_version_file(version, notes)
        release_count = update.get_release_count(str(directory)) + 1
        zf = ZipFile(str(directory / 'release_{}'.format(release_count)), mode='w', compression=compression)

        for root, dirs, files, in walk(str(Path('../../'))):
            root = Path(root)
            try: third = root.parts[2]
            except (IndexError,): third = ''
            if third in ['pmc', 'res']:
                for file in files:
                    f = root / file
                    if f.suffix == '.pyc': continue
                    # print(f.resolve(), )
                    zf.write(str(f.resolve()), arcname=str(Path(*f.parts[2:])), compress_type=compression)

        include = [
            '../../core.py',
            '../../LICENSE',
            '../../README.md'
        ]

        for file in include:
            file = Path(file)
            zf.write(str(file.resolve()), str(str(Path(*file.parts[2:]))), compress_type=compression)

        zf.close()


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
        config.add_section('info')
        config.add_section('coords')
        config.add_section('on-top')
        config.add_section('fixed')
        config.add_section('lists')
        for key, value, in info.items(): config.set('info', key, str(value))
        for name, coords, in coorddata.items(): config.set('coords', name.upper(), ', '.join(list(map(str, coords))))
        for top, bottom, in ontop.items(): config.set('on-top', top.upper(), bottom.upper())
        for name, tex, in fixed.items(): config.set('fixed', name, tex.upper())
        for name, items, in lists.items():
            config.set('lists', name, ', '.join(list(map(lambda item: item.upper(), items))))
        with Path(target).open('w') as configfile: config.write(configfile)

        zfile = ZipFile(str(target), mode='w', compression=compression)
        try:
            zfile.write(str(image), 'texture.png', compress_type=compression)
            lines = list()
            for section in config.sections():
                lines.append('[{}]'.format(section))
                for option in config.options(section): lines.append('{} = {}'.format(option, config.get(section, option)))
                lines.append('')
            zfile.writestr('data', '\n'.join(lines), compress_type=compression)
        finally: zfile.close()


if __name__ == '__main__':
    textures.create_textureset('../../res/textures/set0',
                               r'C:\Users\User\Documents\python\PyMineCraft3\res\textures\set3~\texture.png',
                               {'creator': "Robin 'r0w' Weiland", 'tset-version': 0, 'size': 4, 'date': '2019-04-18'},
                               {
                                   'GRASS': (1, 0, 0, 1, 0, 0,),
                                   'DIRT': (0, 1, 0, 1, 0, 1,),
                                   'SAND': (1, 1, 1, 1, 1, 1,),
                                   'BRICK': (2, 0, 2, 0, 2, 0,),
                                   'STONE': (2, 1, 2, 1, 2, 1,),
                                   'LAVA': (3, 0, 3, 0, 3, 0,),
                                   'WOOD': (3, 2, 3, 2, 3, 1,),
                                   'CONCRETE': (2, 2, 2, 2, 2, 2,),
                                   'GLASS': (1, 2, 1, 2, 1, 2,)
                               },
                               {'GRASS': 'DIRT'},
                               {'edge': 'STONE', 'floor': 'GRASS'},
                               {'terraform': ['BRICK', 'GRASS', 'SAND', 'LAVA', 'CONCRETE'],
                                'inventory': ['BRICK', 'SAND', 'GRASS', 'DIRT', 'CONCRETE', 'WOOD', 'LAVA', 'GLASS'],
                                'hurt': ['LAVA'], 'transparent': ['GLASS']}
                               )


    # from timeit import Timer
    # timer = Timer(lambda: update.pack_release(0))
    # print(timer.timeit(1))

    # rng.create_new_pool(Path(r'C:\Users\User\Documents\python\pMC\res\data\rngpool'))
