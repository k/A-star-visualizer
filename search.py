from fringe_heap import Fringe
from grid import neighbors, cost


def best_first_search(g, start, goal, f):
    if start is goal:
        return None

    fringe = Fringe()
    closed = {}
    parent = dict()
    parent[start] = start

    fringe.insert(start, 0)
    while len(fringe) > 0:
        (prev_cost, curr) = fringe.pop()
        if curr is goal:
            path = []
            while parent[curr] != curr:
                path.prepend(curr)
                curr = parent[curr]
            return (cost, path)  # TODO return path
        for n in neighbors(g, curr):
            if n not in closed:
                x = f(prev_cost, curr, n)
                if x not in fringe or x in fringe and x < fringe[n]:
                    parent[n] = curr
                    fringe[n] = x


def uniform_cost_search(g, start, goal):
    def f(prev_cost, curr, n):
        return prev_cost + cost(curr, n)

    return best_first_search(g, start, goal, f)


def a_star(g, start, goal, heuristic):
    def f(prev_cost, curr, n):
        return prev_cost + cost(curr, n) + heuristic(n)

    return best_first_search(g, start, goal, f)


def a_star_weighted(g, start, goal, heuristic, w):
    def f(prev_cost, curr, n):
        return prev_cost + cost(curr, n) + w * heuristic(n)
