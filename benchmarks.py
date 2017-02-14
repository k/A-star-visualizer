import csv
import resource
import os
from functools import partial
import numpy as np

from heuristic import *
from maps import input_file
from search import path, a_star, a_star_sequential, a_star_integrated, uniform_cost_search


bases = [chebychev_distance, manhattan_distance, diagonal_distance, euclidian_distance]
modifiers = [make_admissible, favor_highways]  # TODO: Fix and add favor_highways_smart


def heuristics():
    for b in bases:
        yield b
        for m in modifiers:
            yield m(b)


def heuristics_a():
    for b in bases:
        if b is not euclidian_distance:
            yield make_admissible(b)


def heuristics_f():
    for b in bases:
        yield favor_highways(b)


def heuristics_s():  # Favor_highways_smart needs fixing
    for b in bases:
        yield favor_highways_smart(b)


def algorithms():
    """Generator that generates all algorithms to be tested.

    Uses currying to return different configurations of the algorithms.
    """
# Uniform Cost Search
    yield uniform_cost_search.__name__, [], None, None, uniform_cost_search

# A*
    for h in heuristics():
        yield a_star.__name__, [h], 1, None, partial(a_star, heuristic=h)

# Weighted A*
    for h in heuristics():
        for w in [1.25, 2, 3, 4]:
            yield a_star.__name__, [h], w, None, partial(a_star, heuristic=h, w=w)

# Sequential A*
    for anchor in heuristics_a():
        for i in [bases, heuristics_f()]:
            other = [h for h in i]
            hs = [anchor] + other
            for w1 in [1.25, 2, 3, 4]:
                for w2 in [1.25, 2, 3, 4]:
                    yield a_star_sequential.__name__, hs, w1, w2, partial(a_star_sequential, heuristics=hs, w1=w1, w2=w2)
# Integrated A*
    for anchor in heuristics_a():
        for i in [bases, heuristics_f()]:
            other = [h for h in i]
            hs = [anchor] + others
            for w1 in [1.25, 2, 3, 4]:
                for w2 in [1.25, 2, 3, 4]:
                    yield a_star_integrated.__name__, hs, w1, w2, partial(a_star_integrated, heuristics=hs, w1=w1, w2=w2)


def map_path(map_num, sg_pair):
    return "maps/map{0}_{1}.txt".format(map_num, sg_pair)


def run_algo(algo):
    """Run an algorithm, return benchmarks"""
    expanded = 0
    for f, g, h, bp, s in algo():
        expanded = expanded+1
        pass
    p = path(bp, s)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    f_string = "-------------\n\
                Process {0}:\n\
                -------------\n\
                Run Time {1}\n\
                Path Length {2}\n\
                Expanded {3}\n\
                Memory {4}\n\
                -------------\n\
                "
    benchmarks = b = (os.getpid(), usage.ru_utime, len(p), expanded, usage.ru_maxrss)
    print(f_string.format(b[0], b[1], b[2], b[3], b[4]))
    return benchmarks


def main():
    os.mkdir('./csv')
    fname = "benchmarks.csv"  # CSV with the averages
    with open('csv/' + fname, 'w+') as csvwritefile:
        writer = csv.writer(csvwritefile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Algorithm', 'Heuristics', 'w1', 'w2', 'Average Run Time',
                        'Average Path Length', 'Average Nodes Expanded', 'Memory Used'])

    for name, hs, w1, w2, a in algorithms():
        for map_num in range(1, 6):
            for sg_pair in range(0, 10):
                (grid, start, goal) = input_file(map_path(map_num, sg_pair))
                algo = partial(a, grid, grid[start], grid[goal])
                print("Forking to run {0}".format(name))
                newpid = os.fork()  # Fork the process so we get a separate memory footprint
                if newpid is 0:
                    benchmarks = run_algo(algo)
                    with open('csv/' + name + str(hs) + str(w1) + str(w2) + '.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(list(benchmarks))
                    os._exit(0)
                else:
                    os.wait4(newpid, 0)
        with open('csv/' + fname, 'a') as csvwritefile:
            with open('csv/' + name + str(hs) + str(w1) + str(w2) + '.csv', 'r') as csvreadfile:
                # reader = csv.reader(csvreadfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer = csv.writer(csvwritefile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                m = np.genfromtxt(csvreadfile, dtype='float', delimiter=' ')
                # m = np.array([r for r in reader])
                row = [name, hs, w1, w2]
                for c in m.T:
                    row.append(np.mean(c))
                writer.writerow(row)

if __name__ == '__main__':
    main()
