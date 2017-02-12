import heapq
import types


# Fringe
class Fringe(list):
    def __init__(self):
        super(Fringe, self).__init__()
        self.costs = dict()

    def top(self):
        return iter(self).next()

    def pop(self):
        """Get the next element in the fringe"""
        (x, s) = heapq.heappop(self)
        self.costs.pop(s)
        return (x, s)

    def insert(self, s, x):
        self[s] = x

    def __contains__(self, s):
        return s in self.costs

    def __getitem__(self, s):
        if s in self:
            return (self.costs[s], s)
        else:
            raise KeyError('Key not found')

    # Update the cost of s in the fringe
    def __setitem__(self, s, x):
        if s in self:
            self.remove(s)
        self.costs[s] = x
        heapq.heappush(self, (x, s))

    # Remove s from the fringe
    def remove(self, s):
        x = self[s]
        super(Fringe, self).remove(x)
        self.costs.pop(s)
        heapq.heapify(self)
