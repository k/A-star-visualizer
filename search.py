from fringe_heap import Fringe
from grid import cost, neighbors
from heuristic import (
        manhattan_distance,
        diagonal_distance,
        diagonal_distance_a,
        euclidian_distance,
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


# Implementation of Best First Search that uses a priority queue (implemented as a binary heap)
def best_first_search(grid, start, goal, cost, h=lambda n: 0):
    fringe = Fringe()
    visited = set()
    parent = dict()
    parent[start] = start
    g = dict()
    g[goal] = float('inf')
    g[start] = 0
    curr = None

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


def a_star(grid, start, goal, heuristic=diagonal_distance, w=1, w2=1):
    if isinstance(heuristic, list):  # Do iterative A*
        if len(heuristic) > 1:
            return a_star_sequential(grid, start, goal, heuristic, w, w2)
        else:
            return a_star(grid, start, goal, heuristic[0], w, w2)
    else:  # Do regular A*
        def h(n):
            return w*heuristic(n, goal)
        return best_first_search(grid, start, goal, cost, h)


def a_star_sequential(grid, start, goal,
                      heuristics=[diagonal_distance_a, euclidian_distance],
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
        to_yeild = None
        for i in inad:
            (a_top_c, a_top_s) = f[anchor].top()
            (i_top_c, i_top_s) = f[i].top()
            if a_top_c <= w2*i_top_c:
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
def a_star_integrated(grid, start, goal, heuristics=[], w1=1, w2=1):
    pass
