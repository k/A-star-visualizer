import unittest
from test import test_support
from space import Space
from grid import blank_grid, is_diagonal, neighbors, cost
from maps import gen_start_goal_pair
from search import *
import numpy as np


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = blank_grid(3, 3)
        pass

    def test_is_diagonal(self):
        assert is_diagonal(self.grid[1, 1], self.grid[0, 0]) is True
        assert is_diagonal(self.grid[1, 1], self.grid[0, 1]) is False
        assert is_diagonal(self.grid[1, 1], self.grid[1, 1]) is False
        assert is_diagonal(self.grid[1, 1], self.grid[1, 0]) is False
        assert is_diagonal(self.grid[1, 1], self.grid[0, 2]) is True
        assert is_diagonal(self.grid[1, 1], self.grid[1, 2]) is False
        assert is_diagonal(self.grid[1, 1], self.grid[2, 2]) is True
        assert is_diagonal(self.grid[1, 1], self.grid[2, 1]) is False
        assert is_diagonal(self.grid[1, 1], self.grid[2, 0]) is True

    def test_neighbors(self):
        n = [s for (i, s) in np.ndenumerate(self.grid) if i is not (1, 1)]
        computed_n = neighbors(self.grid, self.grid[1, 1])
        for s in n:
            assert s in computed_n

    def test_cost(self):
        def approx_equal(f1, f2): 
            return abs(f1 - f2) < .01
        assert approx_equal(cost(self.grid, self.grid[1, 1], self.grid[0, 0]), 2.**.5)
        assert approx_equal(cost(self.grid, self.grid[1, 1], self.grid[0, 1]), 1.)
        assert approx_equal(cost(self.grid, self.grid[1, 1], self.grid[1, 1]), 1.)
        assert approx_equal(cost(self.grid, self.grid[1, 1], self.grid[1, 0]), 1.)
        assert approx_equal(cost(self.grid, self.grid[1, 1], self.grid[0, 2]), 2.**.5)
        assert approx_equal(cost(self.grid, self.grid[1, 1], self.grid[1, 2]), 1.)
        assert approx_equal(cost(self.grid, self.grid[1, 1], self.grid[2, 2]), 2.**.5)
        assert approx_equal(cost(self.grid, self.grid[1, 1], self.grid[2, 1]), 1.)
        assert approx_equal(cost(self.grid, self.grid[1, 1], self.grid[2, 0]), 2.**.5)



def test_main():
    test_support.run_unittest(TestGrid)

if __name__ == '__main__':
    test_main()
