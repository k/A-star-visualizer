from random import sample, uniform
from numpy import ndenumerate, random
import numpy as np

# Terrain
# 0 - blocked
# 1 - clear
# 2 - rough
# a - highway 
# b - rough highway

# returns a blank grid of all zeros
def blank_grid(r, c):
    return np.ones([r, c])

# returns a 1D array of all the border cells from a 2D array
def borders(g):
    s = g.shape
    return np.concatenate([g[0,:],g[1:,0],g[s[0]-1,1:],g[1:(s[0]-1),s[1]-1]])

def rough(g):
    s = g.shape
    coords = np.random.choice(ndenumerate(g).flat, size=8, replace=False)
    for (r, c, v) in coords:
        for (r, c, v) in ndenumerage(g)[r-15:(r+15)%s[0],c-15:(c+15)%s[1]]:
            g[r, c] = np.random.choice([0, 1], 1)[0]

def gen_highways(g):
    highways = []
    fails = 0
    while len(highways) < 8:
        if fails is 5:
            # TODO: clear all highways
        edges = borders(ndenumerate(g))
        b = random.choice(edges)
        directions = set([(-1,0), (1,0), (0,-1), (0,1)])
        if b[0] is 0:
            directions.remove((0,-1))
        if b[0] is b.shape[0]-1:
            directions.remove((0,1))
        if b[1] is 0:
            directions.remove((-1,0))
        if b[1] is b.shape[1]-1:
            directions.remove((1,0))
        direction = random.choice(list(directions))
        current_highway = []

        for i in count(1):
            if i % 20 is 0:
                # TODO: chance to change directions

            (r, c) = b
            if g[r,c] is in ['a', 'b']: # Redo path on highway
                fails += 1
                continue;
            else:
                g[r,c] = 'a' # TODO: Make this update correctly for rough tiles
                current_highway.append((r,c))

            b = (r + direction[0], c + direction[1])

            #TODO: Stop on border and evaluate length

        highways.append(highway)


def blocked(g):


