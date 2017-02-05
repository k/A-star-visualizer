# grid.py Grid functions
import numpy as np
from space import Space


# returns a blank grid of all zeros
def grid(r=120, c=160):
    a = [Space((x, y)) for x in range(0, r) for y in range(0, c)]
    return np.array(a).reshape(r, c)


# returns a 1D array of all the border cells from a 2D ndarray
def borders(g, w=1):
    s = g.shape
    max_r = s[0]
    max_c = s[1]
    left = g[0:w, :].flatten()
    top = g[w:, 0:w].flatten()
    bottom = g[max_r - w:max_r, w:].flatten()
    right = g[w:(max_r - w), max_c - w:max_c].flatten()
    return np.concatenate([top, left, right, bottom]).flatten()


# returns a 1d array of all the corners from a 2d ndarray
def corners(g):
    s = g.shape
    return np.array([g[0, 0], g[0, s[1]-1], g[s[0]-1, 0], g[s[0]-1, s[1]-1]])


# Returns the cost to travel from s1 to s2. Returns inf if either is blocked
def cost(g, s1, s2):
    if s1.is_blocked() or s2.is_blocked():
        raise Exception('Calculating cost to blocked cell')
    if s2 in neighbors(g, s1):
        c = (s1.cost() + s2.cost())/2
        if s1.is_highway() and s2.is_highway():
            return c/4
        else:
            return c
    else:
        return float('inf')


# Returns the neighboring cells of Space s in grid g
def neighbors(g, s):
    (r, c) = s.coords
    max_r = g.shape[0]
    max_c = g.shape[1]
    n = []
    for x in range(max(0, r-1), min(max_r, r+2)):
        for y in range(max(0, c-1), min(max_c, c+2)):
            if not g[x, y].is_blocked():
                n.append(g[x, y])
    return n


# TODO Python Documentation
def unwrap_coords(func):
    def func_wrapper(s1, s2):
        (s1x, s1y) = s1.coords
        (s2x, s2y) = s2.coords
        return func(s1x, s1y, s2x, s2y)
    return func_wrapper


@unwrap_coords
def euclidian_distance(s1x, s1y, s2x, s2y):
    return ((s1x - s2x)**2 + (s1y - s2y)**2)**(1/2)


@unwrap_coords
def manhattan_distance(s1x, s1y, s2x, s2y):
    return abs(s1x - s2x) + abs(s1y - s2y)


@unwrap_coords
def diagonal_distance(s1x, s1y, s2x, s2y):
    d_x = abs(s1x - s2x)
    d_y = abs(s1y - s2y)
    return (2**(.5) - 1)*min(d_x, d_y) + max(d_x, d_y)
