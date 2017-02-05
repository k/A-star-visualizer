from copy import deepcopy
from grid import borders, corners
from itertools import count
import numpy as np
from space import Space
import time


def gen_highways(g):
    highways = []
    fails = 0
    g = deepcopy(g)
    while len(highways) < 4:
        try:
            highway = gen_highway(g)
            highways.append(highway)
            for s in highway:
                s.set_highway()
        except:
            fails = fails + 1
            if fails is 50:
                raise Exception('Highway generation failed 50 times')

    return g


def gen_highway(g):
    np.random.seed(int(time.time()*10**9 % 2**20))
    edges = np.setdiff1d(borders(g), corners(g))
    all_directions = {-1, 1, -1j, 1j}
    start = None
    while start is None or start.is_highway():
        start = np.random.choice(edges)
    coords = start.coords
    if coords[0] is 0:  # On the left border
        direction = 1  # right
    if coords[0] is g.shape[0]-1:  # On the bottom border
        direction = -1j  # up
    if coords[1] is 0:  # On the top border
        direction = 1j  # down
    if coords[1] is g.shape[1]-1:  # On the right border
        direction = -1  # left
    highway = []
    curr = start

    for i in count(1):
        if i % 20 is 0:
            directions = [direction]
            sideways = set.difference(all_directions,
                                      {direction, -1*direction})
            for d in sideways:
                directions.append(d)
            direction = np.random.choice(np.array(directions), p=[.6, .2, .2])

        if curr.is_highway() or curr in highway:  # Redo path on highway
            raise Exception('Ran into existing highway')
        else:
            highway.append(curr)

        # Stop on border an evaluate length
        if curr in edges and curr is not start:
            if len(highway) < .8*min(g.shape[0], g.shape[1]):
                raise Exception('Highway not long enough')
            break

        (r, c) = curr.coords
        curr = g[r + direction.real, c + direction.imag]

    return highway
