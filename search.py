from fringe_heap import Fringe
from grid import neighbors, cost
from heuristic import diagonal_distance

# TODO Add Node class to take advantage of dynamic programming
# - Store neighbors temporarily
# - Store cost temporarily
# - Store g values? -> already being done


# Returns a list dictating the path from curr to the start
def path(parent, curr):
    path = [curr]
    while parent[curr] != curr:
        curr = parent[curr]
        path = [curr] + path
    return path


def best_first_search(grid, start, goal, cost, h=lambda n: 0):
    if start is goal:
        yield None
        return

    fringe = Fringe()
    visited = set()
    parent = dict()
    parent[start] = start
    g = dict()
    g[start] = 0
    curr = None

    fringe[start] = 0
    while len(fringe) > 0:
        (p_cost, curr) = fringe.pop()
        if curr is goal:
            yield (g, h, parent, curr)
            return
        visited.add(curr)
        yield (g, h, parent, curr)
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


def a_star(grid, start, goal, heuristic=diagonal_distance, w=1):
    def h(n):
        return w*heuristic(n, goal)

    return best_first_search(grid, start, goal, cost, h)
