from image_util import SpriteSheetWriter, SpriteSheetReader
from space import Space, Type
import numpy as np


def output_image(grid, fname, start, goal, path=[]):
    reader = SpriteSheetReader("tiles.png", 32)
    writer = SpriteSheetWriter(32, grid.shape[0], grid.shape[1])
    for index, s in np.ndenumerate(grid):
        (x, y) = index
        tile1 = get_tile(reader, s, start, goal, path)
        writer.addImage(tile1, x, y)
    writer.save(fname)


types = {Type.blocked: 3,
         Type.regular: 0.,
         Type.rough: 1,
         Type.highway_regular: 2,
         Type.highway_rough: 2}


def get_tile(reader, s, start, goal, path):
    x = types[s.type]
    if s is start:
        y = 3
    elif s is goal:
        y = 2
    elif s in path:
        y = 1
    else:
        y = 0
    tile = reader.getTile(x, y)
    return tile
