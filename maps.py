from copy import deepcopy
from grid import blank_grid, borders
from heuristic import manhattan_distance
from highway import gen_highways
import numpy as np
from space import Space, Type
import time

# TODO use decorators for random seeds
# TODO use decorators for copying grids


def gen_rough(g):
    np.random.seed(int(time.time()*10**9 % 2**20))
    g = deepcopy(g)
    max_x = g.shape[0]
    max_y = g.shape[1]
    spaces = np.random.choice(g.flatten(), size=8, replace=False)
    for s in spaces:
        (x, y) = s.coords
        for i in range(max(0, x-15), min(max_x, x+16)):
            for j in range(max(0, y-15), min(max_y, y+16)):
                if np.random.choice([True, False], 1)[0]:
                    g[i, j].set_rough()

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


def output_file(g, start=None, goal=None, fname='map.txt'):
    with open(fname, 'w') as f:
        if start:
            f.write(str(start.coords[0]) + ',' + str(start.coords[1]) + '\n')
        if goal:
            f.write(str(goal.coords[0]) + ',' + str(goal.coords[1]) + '\n')

        shape = g.shape
        for x in range(0, shape[0]):
            for y in range(0, shape[1]):
                s = g[x, y]
                f.write(s.type)
            if x < shape[0] - 1:
                f.write('\n')


def input_file(path):
    with open(path, 'r') as f:
        start = tuple([int(x) for x in f.readline().strip().split(',')])
        end = tuple([int(x) for x in f.readline().strip().split(',')])
        a = np.genfromtxt(f, dtype='str', delimiter=1)
        grid = blank_grid(a.shape[0], a.shape[1])
        for (i, s) in np.ndenumerate(grid):
            (x, y) = i
            s.type = a[x, y]
        return (grid, start, end)
