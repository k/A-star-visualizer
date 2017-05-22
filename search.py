from fringe_binheap import Fringe
from grid import cost, neighbors
from functools import partial
from heuristic import (
        manhattan_distance_n,
        diagonal_distance_n,
        diagonal_distance_a,
        euclidian_distance_n,
        )

# TODO Add Node class to take advantage of dynamic programming
# - Store cost temporarily
# - Store neighbors temporarily
# - Store g values? -> already being done


# Returns a list dictating the path from curr to the start
def path(parent, curr):
    path = [curr]
    while parent[curr] != curr:
        curr = parent[curr]
        path = [curr] + path
    return path


def path_cost(grid, parent, curr):
    p = path(parent, curr)
    c = 0
    prev = None
    for s in p:
        if prev:
            c = c + cost(grid, prev, s)
        prev = s
    return c


# Implementation of Best First Search that uses a priority queue (implemented as a binary heap)
def best_first_search(grid, start, goal, cost, h=lambda s: 0):
    fringe = Fringe()
    visited = set()
    parent = dict()
    parent[start] = start
    g = dict()
    g[goal] = float('inf')
    g[start] = 0
    curr = start

    fringe[start] = 0
    while len(fringe) > 0:
        yield (fringe, g, h, parent, curr)
        (p_cost, curr) = fringe.pop()
        if curr is goal:
            yield (fringe, g, h, parent, curr)
            return
        visited.add(curr)
        __expand_space(grid, fringe, visited, g, h, parent, curr)
    raise Exception("No path found")


def __expand_space(grid, fringe, visited, g, h, parent, curr):
    for n in neighbors(grid, curr):
        if n not in visited:
            if n not in fringe:
                g[n] = float('inf')
                parent[n] = None
            if g[curr] + cost(grid, curr, n) < g[n]:
                g[n] = g[curr] + cost(grid, curr, n)
                parent[n] = curr
                fringe[n] = g[n] + h(n)


def uniform_cost_search(grid, start, goal):
    return best_first_search(grid, start, goal, cost)


def a_star(grid, start, goal, heuristic=diagonal_distance_n, w=1, w2=1, integrated=True):
    if isinstance(heuristic, list):  # Do iterative A*
        if len(heuristic) > 1:
            if integrated:
                return a_star_integrated(grid, start, goal, heuristic, w, w2)
            else:
                return a_star_sequential(grid, start, goal, heuristic, w, w2)
        else:
            return a_star(grid, start, goal, heuristic[0], w, w2)
    else:  # Only one heuristic, do regular A*
        def new_h(s):
            return w*heuristic(grid, s, goal)
        return best_first_search(grid, start, goal, cost, new_h)


def a_star_sequential(grid, start, goal,
                      heuristics=[diagonal_distance_a, euclidian_distance_n],
                      w1=1, w2=1):
    """Create an A* sequential generator

    heuristics: List of heuristics to use, the first in the list is used as anchor
    """
    a_stars = [a_star(grid, start, goal, h, w1, w2) for h in heuristics]
    anchor = a_stars[0]
    inad = a_stars[1:]
    f, g, h, bp = dict(), dict(), dict(), dict()
    for a in a_stars:
        # Get first value for each heuristic so we can start the conditional loop
        f[a], g[a], h[a], bp[a], curr = next(a)
    while f[anchor].top()[0] < float('inf'):
        for i in inad:
            (a_top_c, a_top_s) = f[anchor].top()
            (i_top_c, i_top_s) = f[i].top()
            if i_top_c <= w2*a_top_c:
                if g[i][goal] <= i_top_c:
                    if g[i][goal] < float('inf'):
                        yield (f[i], g[i], h[i], bp[i], goal)
                        return
                else:
                    yield next(i)
            else:
                if g[anchor][goal] <= a_top_c:
                    if g[anchor][goal] < float('inf'):
                        yield (f[anchor], g[anchor], h[anchor], bp[anchor], goal)
                        return
                else:
                    yield next(anchor)
    raise Exception("No path found")


# The first heuristic in the huerisitcs parameter will be used as the admissible heuristic
def a_star_integrated(grid, start, goal,
                      heuristics=[diagonal_distance_a, euclidian_distance_n],
                      w1=1, w2=1):
    h_s = []

    def prep_h(f):
        def func_wrapper(n):
            return f(grid, n, goal)
        return func_wrapper

    for h1 in heuristics:  # Ran into a weird namespacing issue here when h1 was h
        h_s.append(prep_h(h1))

    heuristics = h_s
    g = dict()
    bp = dict()
    o = dict()
    g[start] = 0
    g[goal] = float('inf')
    bp[start] = start
    bp[goal] = None
    for h1 in heuristics:
        o[h1] = Fringe()
        o[h1][start] = key(g, h1, start, w1)
    anchor = heuristics[0]
    inad = heuristics[1:]
    c_a = set()
    c_i = set()
    expand_space = partial(__expand_space_integrated, grid, o, c_a, c_i, g,
                           anchor, inad, bp, w1, w2)
    while o[anchor].top()[0] < float('inf'):
        for i in inad:
            (a_top_c, a_top_s) = o[anchor].top()
            if len(o[i]) > 0:
                (i_top_c, i_top_s) = o[i].top()
            else:
                i_top_c = float('inf')
            if i_top_c <= w2*a_top_c:
                if g[goal] <= i_top_c:
                    if g[goal] < float('inf'):
                        yield (o[i], g, i, bp, goal)
                        return
                else:
                    (cst, curr) = o[i].pop()
                    expand_space(curr)
                    c_i.add(curr)
                    yield (o[i], g, i, bp, curr)
            else:
                if g[goal] <= a_top_c:
                    if g[goal] < float('inf'):
                        yield (o[anchor], g, anchor, bp, goal)
                        return
                else:
                    (cst, curr) = o[anchor].pop()
                    expand_space(curr)
                    c_a.add(curr)
                    yield (o[anchor], g, anchor, bp, curr)
    raise Exception("No path found")


def __expand_space_integrated(grid, o, c_a, c_i, g, anchor, inad, bp, w1, w2, curr):
    for k in o:
        if curr in o[k]:
            o[k].remove(curr)
    for n in neighbors(grid, curr):
        if n not in g:
            g[n] = float('inf')
            bp[n] = None
        g_new = g[curr] + cost(grid, curr, n)
        if g[n] > g[curr] + cost(grid, curr, n):
            g[n] = g_new
            bp[n] = curr
            if n not in c_a:
                o[anchor][n] = key(g, anchor, n, w1)
                if n not in c_i:
                    for i in inad:
                        if key(g, i, n, w1) <= w2*o[anchor][n]:
                            o[i][n] = key(g, i, n, w1)


def key(g, h, s, w1):
    return g[s] + w1*h(s)


# Options:
# 1. Put new shared data structures in a parameters for best_first_search and a_star
#   a. adds parameter value for each new data structure with default being None
#   b. introspection to determine which expand function to use
#
# 2. Make best_first_search into a class  <- I think this is the winner, but I won't have time
#   a. an instance of the class is iterable (it implements __iter__() and __next__())
#   b. methods can be overwritten (like expand)
#   c. state can be shared instead of requiring long parameter lists
#   d. initialization of the data structures can be handled in an encapsulated function
#       that can be overwritten
#
# 3. Write a separate function that does not use the a_star generaters
