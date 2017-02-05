from copy import deepcopy
from grid import grid, borders, manhattan_distance
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
        for x in range(max(0, r-15), min(max_r, r+16)):
            for y in range(max(0, c-15), min(max_c, c+16)):
                if np.random.choice([True, False], 1)[0]:
                    g[x, y].set_rough()

    return g


def gen_blocked(g):
    g = deepcopy(g)
    size = g.size
    flat = filter(lambda x: not x.is_highway(), g.flatten())
    sample = np.random.choice(flat, size=size/5)
    for s in sample:
        s.set_blocked()
    return g


def gen_start_goal_pair(g):
    np.random.seed(int(time.time()*10**9 % 2**20))
    start = None
    goal = None
    while start is None or manhattan_distance(start, goal) < .8*min(g.shape[0], g.shape[1]):
        (start, goal) = np.random.choice(borders(g, 20), size=2)
    return (start, goal)


def output_file(g, start=None, goal=None):
    with open('map.txt', 'w') as f:
        if start:
            f.write(str(start.coords[0]) + ',' + str(start.coords[1]) + '\n')
        if goal:
            f.write(str(goal.coords[0]) + ',' + str(goal.coords[1]) + '\n')

        shape = g.shape
        for r in range(0, shape[0]):
            for c in range(0, shape[1]):
                s = g[r, c]
                f.write(s.type)
            if r < shape[0] - 1:
                f.write('\n')


def input_file(path):
    with open(path, 'r') as f:
        start = tuple([int(x) for x in f.readline().strip().split(',')])
        end = tuple([int(x) for x in f.readline().strip().split(',')])
        a = np.genfromtxt(f, delimiter=1)
        g = grid(a.shape[0], a.shape[1])
        for (i, s) in np.ndenumerate(g):
            (r, c) = i
            s.type = a[r, c]
        return g

