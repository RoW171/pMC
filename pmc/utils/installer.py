__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-11"
__version__ = "0.0.1"

from progressbar import ProgressBar
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from os import system, remove, walk
from shutil import rmtree, copytree, copy2
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
try:
    import zlib
    compression = ZIP_DEFLATED
except (ImportError,): compression = ZIP_STORED
from json import loads


REPO = 'https://raw.github.com/RoW171/pMC/master/'


def clear(): system('cls')


def pause(): input('\nPress Return to continue...')


def replace(source, target):
    if not isinstance(source, Path): source = Path(source)
    if not isinstance(target, Path): target = Path(target)

    if not source.exists(): FileNotFoundError("path '{}' does not exist".format(source))
    if not target.exists(): FileNotFoundError("target '{}' does not exist".format(target))

    if not target.is_file(): rmtree(target)
    else: remove(target)

    if not source.is_file(): copytree(str(source), str(target))
    else: copy2(str(source), str(target))


def getLatestVersion():
    try: response = urlopen(REPO + 'res/data/version').read().decode('utf-8')
    except (URLError,): return -2
    except (ValueError,): return -1
    else:
        lv = loads(response)
        release = lv['version']['release']
        major, minor, patch, = lv['version']['version']
        date = lv['meta']['date']
        return release, major, minor, patch, date,


def showprogress(block_num, block_size, total_size):
    global progress
    if progress is None: progress = ProgressBar(maxval=total_size).start()
    downloaded = block_num * block_size
    if downloaded < total_size: progress.update(downloaded)
    else: progress.finish()


def runDownload(release):
    clear()
    directory = Path('./download_{}'.format(release))
    releasefile = directory / 'version_{}'.format(release)
    print('create temporary directory')
    try: directory.mkdir()
    except (FileExistsError,): pass
    print('downloading latest release')
    urlretrieve(REPO + 'release/release_{}'.format(release), releasefile, showprogress)
    print('\nextracting data')
    zf = ZipFile(str(releasefile), 'r')
    extProgress = ProgressBar()
    for file in extProgress(zf.namelist()): zf.extract(file)
    del zf
    print('extrated successfully')

    #

    print('installing')
    fileProgress, folderProgress, = ProgressBar(), ProgressBar()
    for dirpath, dirnames, filenames, in walk(directory):
        print('installing files')
        for file in fileProgress(filenames):
            if file == releasefile.name: continue
            replace(file.resolve(), Path(file).resolve())
        print('installing directories')
        break
    print('installed successfully')
    rmtree(str(directory))
    pause()


def update():
    print('-' * 10, 'Installer', '-' * 10, sep='')
    latest = getLatestVersion()
    print('\tLatest release available:', latest, '' if not isinstance(latest, int) else '[ERROR]', '\n')
    if latest == -2:
        print('Could not connect to the server. Consider checking your internet connection and try again.')
        pause()
    elif latest == -1:
        print('Release-specific data from the server was received but corrupted.')
        pause()
    else: runDownload(latest[0])


progress = None
update()


if __name__ == '__main__': pass
