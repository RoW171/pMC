__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-02"
__version__ = "0.0.1"

from progressbar import ProgressBar
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from os import system, remove, walk
from sys import exit
from shutil import rmtree, copytree, copy2
from pathlib import Path
from pmc.resources.io.serializer import json
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
try:
    import zlib
    compression = ZIP_DEFLATED
except (ImportError,): compression = ZIP_STORED


VERSIONFILEPATH = Path('./res/data/version')


class UpdateError:
    def __init__(self): pass

    def cleanup(self): pass


def pause(): input('\nPress Return to continue...')  # system('pause')


def clear(): system('cls')


def replace(source, target):
    if not isinstance(source, Path): source = Path(source)
    if not isinstance(target, Path): target = Path(target)

    if not source.exists(): FileNotFoundError("path '{}' does not exist".format(source))
    if not target.exists(): FileNotFoundError("target '{}' does not exist".format(target))

    if not target.is_file(): rmtree(target)
    else: remove(target)

    if not source.is_file(): copytree(str(source), str(target))
    else: copy2(str(source), str(target))


def showprogress(block_num, block_size, total_size):
    global progress
    if progress is None: progress = ProgressBar(maxval=total_size).start()
    downloaded = block_num * block_size
    if downloaded < total_size: progress.update(downloaded)
    else: progress.finish()
    
    
def getVersionFile():
    try: return json.loadFile(VERSIONFILEPATH)
    except (Exception,): return None
    

def getLatestVersion():
    try: response = urlopen(VERSIONFILE['urls']['version']).read().decode('utf-8')
    except (URLError,): return -2
    except (ValueError,): return -1
    else:
        lv = json.loadObject(response)
        release = lv['version']['release']
        major, minor, patch, = lv['version']['version']
        date = lv['meta']['date']
        return release, major, minor, patch, date,


def getInstalledVersion():
    if VERSIONFILE is None: return -1
    release = VERSIONFILE['version']['release']
    major, minor, patch, = VERSIONFILE['version']['version']
    date = VERSIONFILE['meta']['date']
    return release, major, minor, patch, date,


def update():
    print('-' * 10, 'Updater', '-' * 10, sep='')
    print('Checking for available updates...')
    installed = getInstalledVersion()
    latest = getLatestVersion()
    print('\tInstalled on your system:', installed, '' if not isinstance(installed, int) else '[ERROR]')
    print('\tLatest release available:', latest, '' if not isinstance(latest, int) else '[ERROR]', '\n')
    if installed == -1:
        print('There seems to be a problem with your installation. It is recommended to update.')
        pause()
    elif latest == -2:
        print('Could not connect to the server. Consider checking your internet connection and try again.')
        pause()
    elif latest == -1:
        print('Release-specific data from the server was received but corrupted.')
        pause()
    else:
        if installed[0] < latest[0]:
            print('There is an update available.')
            if input('\tDo you want to update [Y/n]: ').lower() in ['yes', 'y', '']: runDownload(latest[0])
            else: exit(0)
        else:
            print('Your game is up-to-date. No updates needed for now.')
            pause()


def runDownload(release):
    clear()
    directory = Path('./download_{}'.format(release))
    releasefile = directory / 'version_{}'.format(release)
    print('create temporary directory')
    try: directory.mkdir()
    except (FileExistsError,): pass
    print('downloading latest release')
    urlretrieve(VERSIONFILE['url']['release'] + 'release_{}'.format(release), releasefile, showprogress)
    print('\nextracting updates')
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


VERSIONFILE = getVersionFile()
progress = None

if __name__ == '__main__': pass
