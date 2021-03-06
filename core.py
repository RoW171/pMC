__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-23"
__version__ = "0.0.1"

from argparse import ArgumentParser
from pmc.utils.update import update
from pmc.utils.uninstall import uninstall
from pmc.utils.reset import reset

from pmc.game.offlinegame import OfflineGame


def main():
    parser = ArgumentParser(description='A puny minecraft clone running with python',
                            epilog='pMC v{} [{}] by {}'.format(__version__, __date__, __author__))
    parser.add_argument('--seed', dest='seed', nargs=1, default=None, type=str, help='seed for world creation')
    parser.add_argument('--savegame', dest='savegame', nargs=1, default=None, type=str, help='savefilepath to load the game from')
    parser.add_argument('--server', action='store_true',
                        help='start the game server, runs on console')
    parser.add_argument('--client', action='store_true',
                        help='start the game client to connect to the server')
    parser.add_argument('-fn', '--filename', default=None, type=str,
                        help='predetermine a savfile you want your game to save to;'
                             'NOT a file to open, rather to (over)write')
    parser.add_argument('-u', '--update', dest='update', action='store_true',
                        help='check for newer versions and prompt to install them')
    parser.add_argument('-r', '--reset', dest='reset', action='store_true',
                        help='reset the game entirely or in parts')
    parser.add_argument('-un', '--uninstall', dest='uninstall', action='store_true',
                        help='uninstall the game')

    args = parser.parse_args()

    if args.update: update()
    elif args.reset: reset()
    elif args.uninstall: uninstall()

    elif args.server: pass
    elif args.client: pass
    else: OfflineGame(seed=args.seed, savegame=args.savegame, name=args.filename)


if __name__ == '__main__': main()
