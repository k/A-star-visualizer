import types
import pqdict


# Fringe
class Fringe(pqdict.PQDict):
    def top(self):
        (s, c) = self.topitem()
        return (c, s)

    def pop(self):
        """Get the next element in the fringe"""
        (s, c) = self.popitem()
        return (c, s)

    def remove(self, s):
        super(Fringe, self).pop(s)
