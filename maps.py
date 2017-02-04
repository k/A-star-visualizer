from copy import deepcopy
from grid import borders, manhattan_distance
from highway import gen_highways
import numpy as np
from space import Space, Type
import time

# TODO use decorators for random seeds
# TODO use decorators for copying grids


def gen_rough(g):
    np.random.seed(int(time.time()*10**9 % 2**20))
    g = deepcopy(g)
    max_r = g.shape[0]
    max_c = g.shape[1]
    spaces = np.random.choice(g.flatten(), size=8, replace=False)
    for s in spaces:
        (r, c) = s.coords
        for x in range(max(0, r-15), min(max_r, r+15)):
            for y in range(max(0, c-15), min(max_c, c+15)):
                if np.random.choice([True, False], 1)[0]:
                    g[x, y].set_rough()

    return g


def gen_blocked(g):
    g = deepcopy(g)
    flat = filter(lambda x: not x.is_highway(), g.flatten())
    sample = np.random.choice(flat, size=g.size/5)
    for s in sample:
        s.set_blocked()
    return g


def gen_start_goal(g):
    np.random.seed(int(time.time()*10**9 % 2**20))
    g = deepcopy(g)
    start = None
    goal = None
    while start is None or manhattan_distance(start.coords, goal.coords) < 100:
        (start, goal) = np.random.choice(borders(g, 20), size=2)
    return (start, goal)


def output_file(g, start=None, goal=None):
    with open('map.txt', 'w') as f:
        if start:
            f.write(str(start.coords[0]) + ', ' + str(start.coords[1]) + '\n')
        if goal:
            f.write(str(goal.coords[0]) + ', ' + str(goal.coords[1]) + '\n')

        shape = g.shape
        for r in range(0, shape[0]):
            for c in range(0, shape[1]):
                s = g[r, c]
                f.write(s.type)
            f.write('\n')
