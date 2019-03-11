__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-02-24"
__version__ = "0.0.1"


class DataTypes:
    names = {
        'bool': bool,
        'int': int,
        'float': float,
        'str': str,
        'list': list,
        'tuple': tuple,
    }

    def __call__(self, arg):
        if type(arg) == str and len(arg) > 0: return self.names[arg]
        else: return arg.__name__


def writeLine(path, line):
    with path.open('a') as file: file.write(line + '\n')


if __name__ == '__main__': pass
