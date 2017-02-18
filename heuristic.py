from space import Space
from grid import unwrap_coords, neighbors, is_horizontal, is_vertical, cost


def grid_arg(h):
    def h_grid(grid, *args, **kwargs):
        return h(*args, **kwargs)
    return h_grid


def make_admissible(h):
    def h_admissable(*args, **kwargs):
        return h(*args, **kwargs)/4.
    return h_admissable


def favor_highways(h):
    def h_favor_highways(*args, **kwargs):
        s = args[1]
        h_v = h(*args, **kwargs)
        return h_v/4. if s.is_highway() else h_v
    return h_favor_highways


# Takes a grid so cannot be used a decorator here
def favor_highways_smart(h):
    def h_favor_highways_smart(grid, s, goal, *args, **kwargs):
        # Only useful for searching for highways beyond manhattan distance bc we only need to compare manhattan distance
        # d_x = s.coords[0] - goal.coords[0]
        # d_y = s.coords[1] - goal.coords[1]
        m_d = manhattan_distance(s, goal)
        c = h(grid, s, goal, *args, **kwargs)
        for n in neighbors(grid, s):
            if is_horizontal(s, n) or is_vertical(s, n):
                if s.is_highway() and n.is_highway():
                    m_d_n = manhattan_distance(n, goal)
                    if m_d < m_d_n:
                        c = cost(grid, s, n)*m_d
            # In order to take into account searching for highways beyond the manhattan distance,
            # we would need to know the parent of s
            # if s.parent is n:
            #    continue

        return c
    return h_favor_highways_smart


@unwrap_coords
def chebychev_distance(s1x, s1y, s2x, s2y):
    return max(abs(s1x-s2x), abs(s1y-s2y))


@grid_arg
def chebychev_distance_n(s, goal):
    return chebychev_distance(s, goal)


@grid_arg
@make_admissible
def chebychev_distance_a(s, goal):
    return chebychev_distance(s, goal)


@favor_highways
@grid_arg
def chebychev_distance_f(s, goal):
    return chebychev_distance(s, goal)


@favor_highways_smart
@grid_arg
def chebychev_distance_s(s, goal):
    return chebychev_distance(s, goal)


@unwrap_coords
def euclidian_distance(s1x, s1y, s2x, s2y):
    return ((s1x - s2x)**2. + (s1y - s2y)**2.)**(.5)


@grid_arg
def euclidian_distance_n(s, goal):
    return euclidian_distance(s, goal)


@grid_arg
@make_admissible
def euclidian_distance_a(s, goal):
    return euclidian_distance(s, goal)


@favor_highways
@grid_arg
def euclidian_distance_f(s, goal):
    return euclidian_distance(s, goal)


@favor_highways_smart
@grid_arg
def euclidian_distance_s(s, goal):
    return euclidian_distance(s, goal)


@unwrap_coords
def manhattan_distance(s1x, s1y, s2x, s2y):
    return abs(s1x - s2x) + abs(s1y - s2y)


@grid_arg
def manhattan_distance_n(s, goal):
    return manhattan_distance(s, goal)


@grid_arg
@make_admissible
def manhattan_distance_a(s, goal):
    return manhattan_distance(s, goal)


@grid_arg
@favor_highways
def manhattan_distance_f(s, goal):
    return manhattan_distance(s, goal)


@favor_highways_smart
@grid_arg
def manhattan_distance_s(s, goal):
    return manhattan_distance(s, goal)


@unwrap_coords
def diagonal_distance(s1x, s1y, s2x, s2y):
    d_x = abs(s1x - s2x)
    d_y = abs(s1y - s2y)
    return (2**(.5) - 1)*min(d_x, d_y) + max(d_x, d_y)


@grid_arg
def diagonal_distance_n(s, goal):
    return diagonal_distance(s, goal)


@make_admissible
@grid_arg
def diagonal_distance_a(s, goal):
    return diagonal_distance(s, goal)


@favor_highways
@grid_arg
def diagonal_distance_f(s, goal):
    return diagonal_distance(s, goal)


@favor_highways_smart
@grid_arg
def diagonal_distance_s(s, goal):
    return diagonal_distance(s, goal)
