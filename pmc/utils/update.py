__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-02"
__version__ = "0.0.1"

from progressbar import ProgressBar
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from os import system, remove, walk
from shutil import rmtree, copytree, copy2
from pathlib import Path
from pmc.resources.io.serializer import json
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
try:
    import zlib
    compression = ZIP_DEFLATED
except (ImportError,): compression = ZIP_STORED


VERSIONFILE = Path('./res/data/version')
REPO = 'https://raw.github.com/RoW171/pMC/master/'


class UpdateError:
    def __init__(self): pass

    def cleanup(self): pass


def pause(): system('pause')


def clear(): system('cls')


def replace(path, target):
    if not isinstance(path, Path): path = Path(path)
    if not isinstance(target, Path): target = Path(target)

    if not path.exists(): FileNotFoundError("path '{}' does not exist".format(path))
    if not target.exists(): FileNotFoundError("target '{}' does not exist".format(target))

    if not target.is_file(): rmtree(target)
    else: remove(target)

    if not path.is_file(): copytree(str(path), str(target))
    else: copy2(str(path), str(target))


def showprogress(block_num, block_size, total_size):
    global progress
    if progress is None: progress = ProgressBar(maxval=total_size).start()
    downloaded = block_num * block_size
    if downloaded < total_size: progress.update(downloaded)
    else: progress.finish()
    
    
def getVersionFile():
    try: return json.loadFile(VERSIONFILE)
    except (Exception,): return None
    

def getLatestVersion():
    try: response = urlopen(REPO + 'res/data/version').read().decode('utf-8')
    except (URLError,): return -2
    except (ValueError,): return -1
    else:
        lv = json.loadObject(response)
        release = lv['version']['release']
        major, minor, patch, = lv['version']['version']
        date = lv['meta']['date']
        return release, major, minor, patch, date,


def getInstalledVersion():
    if versionfile is None: return -1
    release = versionfile['version']['release']
    major, minor, patch, = versionfile['version']['version']
    date = versionfile['meta']['date']
    return release, major, minor, patch, date,


def check():
    installed = getInstalledVersion()
    latest = getLatestVersion()

    if isinstance(installed, int):
        pass  #  error
    if isinstance(latest, int):
        if latest == -2:
            pass  # error: network
        elif latest == -1:
            pass  # error

    if installed[0] < latest[0]: return latest, installed
    else: return


def update():
    print(getLatestVersion())
    print(getInstalledVersion())


def download(release):
    clear()
    directory = Path('./download_{}'.format(release))
    releasefile = directory / 'version_{}'.format(release)
    #
    try: directory.mkdir()
    except (FileExistsError,): pass
    #
    urlretrieve(versionfile['url']['release'] + 'release_{}'.format(release), releasefile, showprogress)
    #
    zf = ZipFile(str(releasefile), 'r')
    extProgress = ProgressBar()
    for file in extProgress(zf.namelist()): zf.extract(file)
    del zf
    #
    return release, directory, releasefile


def install(release, dir, rfile):
        print('installing')
        fileProgress, folderProgress, = ProgressBar(), ProgressBar()
        for dirpath, dirnames, filenames, in walk(dir):
            print('installing files')
            for file in fileProgress(filenames):
                if file == rfile.name: continue
                replace(file.resolve(), Path(file).resolve())
            print('installing directories')
            # for directory in folderProgress(dirnames):
                # print(directory)
                # replace(abspath(join(folder, directory)), abspath(directory))
            break
        print('installed successfully')
        rmtree(dir)
        pause()


def create_version_file(version, release, notes='', state='stable'):
    from datetime import datetime
    date = datetime.now().date()
    info = {
        'meta': {
            'author': 'Robin \'r0w\' Weiland',
            'date': str(date.year) + '-' + str(date.month) + '-' + str(date.day)
        },
        'version': {
            'version': version,
            'release': release,
            'notes': notes,
            'state': state
        },
        'paths': {
            'installed-version': str(VERSIONFILE)
        },
        'urls': {
            'repo': REPO,
            'version': REPO + 'res/data/version',
            'release': REPO + 'release/'
        }

    }
    json.dumpFile(Path('../../res/data/version'), info, indent=4)


if __name__ == '__main__':
    versionfile = getVersionFile()
    # create_version_file((0, 0, 1,), 0, 'development - unstable')
    progress = None
    update()

