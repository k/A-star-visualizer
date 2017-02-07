# grid.py Grid functions
import numpy as np
from space import Space


# returns a blank grid of all zeros
def blank_grid(x=160, y=120):
    a = [Space((i, j)) for i in range(0, x) for j in range(0, y)]
    return np.array(a).reshape(x, y)


# returns a 1D array of all the border cells from a 2D ndarray
def borders(g, w=1):
    s = g.shape
    max_x = s[0]
    max_y = s[1]
    left = g[0:w, :].flatten()
    top = g[w:, 0:w].flatten()
    bottom = g[max_x - w:max_x, w:].flatten()
    right = g[w:(max_x - w), max_y - w:max_y].flatten()
    return np.concatenate([top, left, right, bottom]).flatten()


# returns a 1d array of all the corners from a 2d ndarray
def corners(g):
    s = g.shape
    return np.array([g[0, 0], g[0, s[1]-1], g[s[0]-1, 0], g[s[0]-1, s[1]-1]])


# Returns the cost to travel from s1 to s2. Returns inf if either is blocked
def cost(g, s1, s2):
    if s2 in neighbors(g, s1):
        y = (s1.cost() + s2.cost())/2.
        if is_diagonal(s1, s2):
            return (s1.cost() + s2.cost())/(2.**.5)
        elif s1.is_highway() and s2.is_highway():
            return y/4.
        else:
            return y
    else:
        return float('inf')


# Returns the neighboring cells of Space s in grid g
def neighbors(g, s):
    (x, y) = s.coords
    max_x = g.shape[0]
    max_y = g.shape[1]
    n = []
    for i in range(max(0, x-1), min(max_x, x+2)):
        for j in range(max(0, y-1), min(max_y, y+2)):
            if not g[i, j].is_blocked():
                n.append(g[i, j])
    return n


def unwrap_coords(func):
    def func_wrapper(s1, s2):
        (s1x, s1y) = s1.coords
        (s2x, s2y) = s2.coords
        return func(s1x, s1y, s2x, s2y)
    return func_wrapper


@unwrap_coords
def is_diagonal(s1x, s1y, s2x, s2y):
    return s1x != s2x and s1y != s2y
