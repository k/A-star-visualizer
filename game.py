import sys
import logging

from rx.subjects import Subject
from rx.concurrency import PyGameScheduler
from space import Space, Type
from maps import input_file
from grid import blank_grid
from search import uniform_cost_search, a_star
import numpy as np

import pygame as pg

# FORMAT = '%(asctime)-15s %(threadName)s %(message)s'
# logging.basicConfig(format=FORMAT, level=logging.DEBUG)
# log = logging.getLogger('Rx')

TILE_SIZE = 8
FRAMES_PER_SECOND = 10

types = {Type.blocked: 3,
         Type.regular: 0.,
         Type.rough: 1,
         Type.highway_regular: 2,
         Type.highway_rough: 2}


def main():

    pg.init()

    clock = pg.time.Clock()

    (grid, start, goal) = input_file('map.txt')
    (g, h, path) = a_star(grid, grid[start[0], start[1]], grid[goal[0], goal[1]])

    size = (grid.shape[0] * TILE_SIZE, grid.shape[1] * TILE_SIZE)
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Search Visualizer")

    black = 0, 0, 0
    background = pg.Surface(screen.get_size())
    background.fill(black)             # fill the background black
    background = background.convert()  # prepare for faster blitting

    scheduler = PyGameScheduler()
    mousemove = Subject()

    files = [
        "tiles.png"
        ]
    tile_keys = {(i,j): "img/tile" + str(i) + str(j) + ".png" for i in range(0,4) for j in range(0,4)}
    images = [pg.image.load(image).convert_alpha() for image in files]
    tile_images = [pg.image.load(tile_keys[k]).convert_alpha() for k in tile_keys]
    tile_images = np.array(tile_images).reshape(4, 4)

    old = [None] * len(images)
    draw = []
    erase = []

    def get_tile_for_space(s, start, goal, path):
        i = types[s.type]
        j = 0
        if s is start:
            j = 3
        elif s is goal:
            j = 2
        elif s in path:
            j = 1
        else:
            j = 0
        tile = tile_images[i, j]
        return tile

    for (index, s) in np.ndenumerate(grid):
        (x, y) = index
        tile = get_tile_for_space(s, start, goal, path)
        draw.append((tile, pg.Rect(x*TILE_SIZE, y*TILE_SIZE,(x+1)*TILE_SIZE,(y+1)*TILE_SIZE)))

    def handle_image(i, image):
        imagerect = image.get_rect()

        def on_next(ev):
            imagerect.top = ev[1]
            imagerect.left = ev[0] + i * 30

            if old[i]:
                erase.append(old[i])
            old[i] = imagerect.copy()
            # draw.append((image, imagerect.copy()))

        def on_error(err):
            print("Got error: %s" % err)
            sys.exit()

        mousemove.delay(i * i * 50, scheduler=scheduler).subscribe(on_next, on_error=on_error)

    for i, image in enumerate(images):
        handle_image(i, image)

    while True:
        clock.tick(FRAMES_PER_SECOND)
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                print('Mousemotion')
                pos = event.pos
                mousemove.on_next(pos)
            elif event.type == pg.QUIT:
                sys.exit()

        if len(draw):
            update = []
            for rect in erase:
                screen.blit(background, (rect.x, rect.y), rect)
                update.append(rect)

            for image, rect in draw:
                screen.blit(image, rect)
                update.append(rect)

            pg.display.update(update)
            pg.display.flip()
            draw = []
            erase = []

        scheduler.run()

if __name__ == '__main__':
    main()
