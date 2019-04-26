__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-03-28"
__version__ = "0.0.1"


def basic_creator(world, seed):
        world.game.rng.setSeed(seed)
        world_size = world.game.data.game.world.world_size // 2
        stepsize = 1
        initYheight = 0
        for x in range(-world_size, world_size + 1, stepsize):
            for z in range(-world_size, world_size + 1, stepsize):
                for y in range(1, world.game.data.game.terrain.floor_depth + 1):
                    if world.game.data.game.terrain.floor_enabled:
                        world.addBlock((x, world.game.data.game.terrain.hill_base - y, z,),
                                       world.textures.floor, immediate=False)
                world.addBlock((x, world.game.data.game.terrain.hill_base -
                               world.game.data.game.terrain.floor_depth - 1, z,),
                               world.textures.edge, immediate=False)

                if x in (-world_size, world_size,) or z in (-world_size, world_size,):
                    for dy in range(world.game.data.game.terrain.hill_base -
                                    world.game.data.game.terrain.floor_depth, 3):
                        world.addBlock((x, initYheight + dy, z,), world.textures.edge, immediate=False)

        if world.game.data.game.terrain.hills_enabled:

            offset = world_size - world_size // 8  # 10
            for _ in range(world.game.data.game.terrain.hill_count):
                texture = world.textures.getRandom(world.game.rng.choice)
                xPos = world.game.rng.randint(-offset, offset)
                yPos = world.game.rng.randint(-offset, offset)
                height = world.game.rng.randint(1, world.game.data.game.terrain.hill_max_height)
                side = world.game.rng.randint(world.game.data.game.terrain.hill_min_side / 2,
                                              world.game.data.game.terrain.hill_max_side / 2)
                for y in range(world.game.data.game.terrain.hill_base,
                               world.game.data.game.terrain.hill_base + height):
                    for x in range(xPos - side, xPos + side + 1):
                        for z in range(yPos - side, yPos + side + 1):
                            if (x - xPos) ** 2 + (z - yPos) ** 2 > (side + 1) ** 2: continue
                            if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2: continue
                            world.addBlock((x, y, z,), texture, immediate=False)
                    side -= world.game.data.game.terrain.tappering


creators = {
    0: basic_creator
}


if __name__ == '__main__': pass
