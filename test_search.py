import unittest
from test import test_support
import grid
from maps import gen_start_goal_pair
from search import *


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.g = grid.grid(20, 20)

    def test_uniform_cost_search(self):
        (start, end) = gen_start_goal_pair(self.g)
        assert uniform_cost_search(self.g, start, end) is not None

    def test_a_star(self):
        (start, end) = gen_start_goal_pair(self.g)
        assert a_star(self.g, start, end) is not None

    def test_a_star_weighted(self):
        (start, end) = gen_start_goal_pair(self.g)
        assert a_star_weighted(self.g, start, end) is not None


def test_main():
    test_support.run_unittest(TestSearch)

if __name__ == '__main__':
    test_main()
