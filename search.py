from fringe_heap import Fringe
from grid import neighbors, cost, euclidian_distance

# TODO Add Node class to take advantage of dynamic programming
# - Store neighbors temporarily
# - Store cost temporarily
# - Store g values?
# - Store grid in Node so neighbors can be called from it?


def best_first_search(grid, start, goal, cost, h=lambda n: 0):
    if start is goal:
        return None

    fringe = Fringe()
    visited = set()
    parent = dict()
    parent[start] = start
    g = dict()
    g[start] = 0

    fringe[start] = 0
    while len(fringe) > 0:
        (p_cost, curr) = fringe.pop()
        if curr is goal:
            path = [curr]
            while parent[curr] != curr:
                curr = parent[curr]
                path = [curr] + path
            return (g[goal], path)
        visited.add(curr)
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


def a_star(grid, start, goal, heuristic=euclidian_distance):
    def h(n):
        return heuristic(n, goal)

    return best_first_search(grid, start, goal, cost, h)


def a_star_weighted(grid, start, goal, heuristic=euclidian_distance, w=1):
    def h(n):
        return w * heuristic(n, goal)

    return best_first_search(grid, start, goal, cost, h)
