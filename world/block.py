__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-17"
__version__ = "0.0.1"


FACES = [
    (0, 1, 0,),  # top
    (0, -1, 0,),  # bottom
    (-1, 0, 0,),  # left
    (1, 0, 0,),  # right
    (0, 0, 1,),    # front
    (0, 0, -1,),  # back
]


FACESreference = [
    ((0, 1, 0,), 'top',),
    ((0, -1, 0,), 'bottom',),
    ((-1, 0, 0,), 'left',),
    ((1, 0, 0,), 'right',),
    ((0, 0, 1,), 'front',),
    ((0, 0, -1,), 'back',),
]


def cube_vertices(x, y, z, n):
    return [
        x - n, y + n, z - n, x - n, y + n, z + n, x + n, y + n, z + n, x + n, y + n, z - n,  # top
        x - n, y - n, z - n, x + n, y - n, z - n, x + n, y - n, z + n, x - n, y - n, z + n,  # bottom
        x - n, y - n, z - n, x - n, y - n, z + n, x - n, y + n, z + n, x - n, y + n, z - n,  # left
        x + n, y - n, z + n, x + n, y - n, z - n, x + n, y + n, z - n, x + n, y + n, z + n,  # right
        x - n, y - n, z + n, x + n, y - n, z + n, x + n, y + n, z + n, x - n, y + n, z + n,  # front
        x + n, y - n, z - n, x - n, y - n, z - n, x - n, y + n, z - n, x + n, y + n, z - n,  # back
    ]


def normalize(position): return tuple(map(lambda p: int(round(p)), position))


def sectorize(position, sector_size):
    x, _, z, = normalize(position)
    return x // sector_size, 0, z // sector_size,


if __name__ == '__main__': pass
