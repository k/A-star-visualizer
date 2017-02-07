from space import Space
from grid import unwrap_coords


@unwrap_coords
def euclidian_distance(s1x, s1y, s2x, s2y):
    return ((s1x - s2x)**2. + (s1y - s2y)**2.)**(.5)


@unwrap_coords
def manhattan_distance(s1x, s1y, s2x, s2y):
    return abs(s1x - s2x) + abs(s1y - s2y)


@unwrap_coords
def diagonal_distance(s1x, s1y, s2x, s2y):
    d_x = abs(s1x - s2x)
    d_y = abs(s1y - s2y)
    return (2**(.5) - 1)*min(d_x, d_y) + max(d_x, d_y)


def make_admissible(h):
    def h_admissable(s, goal):
        return h(s, goal)/4.
    return h_admissable


def favor_highways(h):
    def h_favor_highway(s, goal):
        h_v = h(s, goal)
        return h_v/4. if s.is_highway() else h_v
    return h_favor_highway
