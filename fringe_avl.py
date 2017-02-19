import types
from bintrees import FastAVLTree


# TODO: Switch this to be bisect for faster reads and allow it to set a sort function (for A* tiebreakers)
class Fringe(FastAVLTree):
    def __init__(self):
        super(Fringe, self).__init__()
        self.costs = dict()

    def top(self):
        return self.min_item()

    def pop(self):
        """Get the next element in the fringe"""
        return self.pop_min()
