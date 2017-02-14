from space import Space
from grid import unwrap_coords, neighbors


def make_admissible(h):
    def h_admissable(s, goal):
        return h(s, goal)/4.
    return h_admissable


def favor_highways(h):
    def h_favor_highways(s, goal):
        h_v = h(s, goal)
        return h_v/4. if s.is_highway() else h_v
    return h_favor_highways


# TODO: Still need the grid for neighbors, maybe refactor heuristics to take a grid?
def favor_highways_smart(h):
    def h_favor_highways_smart(s, goal):
        # Only useful for searching for highways beyond manhattan distance
        # d_x = s.coords[0] - goal.coords[0]
        # d_y = s.coords[1] - goal.coords[1]
        m_d = manhattan_distance(s, goal)
        cost = h(s, goal)
        for n in neighbors(grid, s):
            if s1.parent is n:
                continue
            if s1.is_highway() and n.is_highway():
                m_d_n = manhattan_distance(s2, goal)
                if m_d < m_d_n:
                    cost = cost(s1, n)*m_d
                # In order to take into account searching for highways beyond the manhattan distance,
                # we would need to know the parent of s

        return cost
    return h_favor_highways_smart


@unwrap_coords
def chebychev_distance(s1x, s1y, s2x, s2y):
    return max(abs(s1x-s2x), abs(s1y-s2y))


@make_admissible
def chebychev_distance_a(s, goal):
    return chebychev_distance(s, goal)


@favor_highways
def chebychev_distance_f(s, goal):
    return chebychev_distance(s, goal)


@favor_highways_smart
def chebychev_distance_s(s, goal):
    return chebychev_distance(s, goal)


@unwrap_coords
def euclidian_distance(s1x, s1y, s2x, s2y):
    return ((s1x - s2x)**2. + (s1y - s2y)**2.)**(.5)


@make_admissible
def euclidian_distance_a(s1x, s1y, s2x, s2y):
    return ((s1x - s2x)**2. + (s1y - s2y)**2.)**(.5)


@favor_highways
def euclidian_distance_f(s1x, s1y, s2x, s2y):
    return ((s1x - s2x)**2. + (s1y - s2y)**2.)**(.5)


@favor_highways_smart
def euclidian_distance_s(s1x, s1y, s2x, s2y):
    return ((s1x - s2x)**2. + (s1y - s2y)**2.)**(.5)


@unwrap_coords
def manhattan_distance(s1x, s1y, s2x, s2y):
    return abs(s1x - s2x) + abs(s1y - s2y)


@make_admissible
def manhattan_distance_a(s, goal):
    return manhattan_distance(s, goal)


@favor_highways
def manhattan_distance_f(s, goal):
    return manhattan_distance(s, goal)


@favor_highways_smart
def manhattan_distance_s(s, goal):
    return manhattan_distance(s, goal)


@unwrap_coords
def diagonal_distance(s1x, s1y, s2x, s2y):
    d_x = abs(s1x - s2x)
    d_y = abs(s1y - s2y)
    return (2**(.5) - 1)*min(d_x, d_y) + max(d_x, d_y)


@make_admissible
def diagonal_distance_a(s, goal):
    return diagonal_distance(s, goal)


@favor_highways
def diagonal_distance_f(s, goal):
    return diagonal_distance(s, goal)


@favor_highways_smart
def diagonal_distance_s(s, goal):
    return diagonal_distance(s, goal)
