import unittest
from test import test_support
import imports
from grid import blank_grid
from maps import gen_start_goal_pair
from search import *


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.g = blank_grid(20, 20)
        (start, end) = gen_start_goal_pair(self.g)
        self.start = start
        self.end = end

    def test_uniform_cost_search(self):
        assert uniform_cost_search(self.g, self.start, self.end) is not None

    def test_a_star(self):
        assert a_star(self.g, self.start, self.end) is not None
        assert a_star(self.g, self.start, self.end, w=2) is not None
        assert a_star_sequential(self.g, self.start, self.end) is not None


def test_main():
    test_support.run_unittest(TestSearch)

if __name__ == '__main__':
    test_main()
