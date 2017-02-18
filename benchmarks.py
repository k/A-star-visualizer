import csv
import resource
import os
from functools import partial
from itertools import chain
import numpy as np

from heuristic import *
from maps import input_file
from search import path, path_cost, a_star, a_star_sequential, a_star_integrated, uniform_cost_search


bases = [chebychev_distance_n, manhattan_distance_n, diagonal_distance_n, euclidian_distance_n]
base_names = ['c', 'm', 'd', 'e']
base_dict = dict(zip(bases, base_names))
modifiers = [make_admissible, favor_highways, favor_highways_smart]  # TODO: Fix and add favor_highways_smart
modifier_names = dict(zip(modifiers, ['a', 'f', 's']))


def heuristics():
    for b in bases:
        yield (base_dict[b], b)
        for m in modifiers:
            yield (base_dict[b]+modifier_names[m], m(b))


def heuristics_b():
    for b in bases:
        yield (base_dict[b], b)


def heuristics_a():
    for b in bases:
        if b is not euclidian_distance:
            yield (base_dict[b]+modifier_names[make_admissible], make_admissible(b))


def heuristics_f():
    for b in bases:
        yield (base_dict[b]+modifier_names[favor_highways], favor_highways(b))


def heuristics_s():
    for b in bases:
        yield (base_dict[b]+modifier_names[favor_highways_smart], favor_highways_smart(b))


def heuristic_all_inad(b):
    name = base_dict[b]
    yield (name, b)
    for m in modifiers:
        if m is not make_admissible:
            yield (name+modifier_names[m], m(b))


def algorithms():
    """Generator that generates all algorithms to be tested.

    Uses currying to return different configurations of the algorithms.
    """
# Uniform Cost Search
    yield uniform_cost_search.__name__, None, None, None, uniform_cost_search

# A*
    for name, h in heuristics():
        yield a_star.__name__, name, 1, None, partial(a_star, heuristic=h)

# Weighted A*
    for name, h in heuristics():
        for w in [1.25, 2, 3, 4, 10]:
            yield a_star.__name__, name, w, None, partial(a_star, heuristic=h, w=w)

# Sequential A*
# TODO: Use some smaller sets heuristics (2 or 3) and mix them up
    for b_name, base in heuristics_b():
        anchor = make_admissible(base)
        a_name = b_name+modifier_names[make_admissible]
        for i in [heuristics_b(), heuristics_f(), heuristics_s(),
                  heuristic_all_inad(base), chain(heuristics_b(), heuristics_s())]:
            others = []
            names = a_name
            for name, h in i:
                others.append(h)
                names = names + '-' + name
            hs = [anchor] + others
            for w1 in [1, 1.25, 2, 3, 4, 10]:
                for w2 in [1, 1.25, 2, 3, 4, 10]:
                    yield (a_star_sequential.__name__, names, w1, w2,
                           partial(a_star_sequential, heuristics=hs, w1=w1, w2=w2))

# Integrated A*
    for b_name, base in heuristics_b():
        anchor = make_admissible(base)
        a_name = b_name+modifier_names[make_admissible]
        for i in [heuristics_b(), heuristics_f(), heuristics_s(),
                  heuristic_all_inad(base), chain(heuristics_b(), heuristics_s())]:
            others = []
            names = a_name
            for name, h in i:
                others.append(h)
                names = names + '-' + name
            hs = [anchor] + others
            for w1 in [1, 1.25, 2, 3, 4, 10]:
                for w2 in [1, 1.25, 2, 3, 4, 10]:
                    yield (a_star_integrated.__name__, names, w1, w2,
                           partial(a_star_integrated, heuristics=hs, w1=w1, w2=w2))


def map_path(map_num, sg_pair):
    return "maps/map{0}_{1}.txt".format(map_num, sg_pair)


def run_algo(algo, grid, s_path):
    """Run an algorithm, return benchmarks"""
    expanded = 0
    usage_b = resource.getrusage(resource.RUSAGE_SELF)
    for f, g, h, bp, s in algo():
        expanded = expanded+1
        pass
    p = path(bp, s)
    p_cost = path_cost(grid, bp, s)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    f_string = "-------------\n\
                Process {0}:\n\
                -------------\n\
                Run Time {1}\n\
                Path Length {2}\n\
                Path Cost {3}\n\
                Expanded {4}\n\
                Memory {5}\n\
                -------------\n\
                "
    benchmarks = b = (os.getpid(), usage.ru_utime - usage_b.ru_utime, len(p),
                      p_cost/s_path, expanded, usage.ru_maxrss - usage_b.ru_maxrss)
    print(f_string.format(b[0], b[1], b[2], b[3], b[4], b[5]))
    return benchmarks


def main():
    os.mkdir('./csv')
    fname = "benchmarks.csv"  # CSV with the averages
    with open('csv/' + fname, 'w+') as csvwritefile:
        writer = csv.writer(csvwritefile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Algorithm', 'Heuristics', 'w1', 'w2', 'Average Run Time',
                        'Average Path Length', 'Average Path Cost/Optimal', 'Average Nodes Expanded', 'Memory Used'])

    s_paths = np.zeros([5, 10])
    a_star_admissible = partial(a_star, heuristic=manhattan_distance_a)
    for name, hs, w1, w2, a in algorithms():
        for map_num in range(1, 6):
            for sg_pair in range(0, 10):
                (grid, start, goal) = input_file(map_path(map_num, sg_pair))
                s_path = s_paths[map_num-1, sg_pair]
                if s_path == 0:  # Lazily create shortest paths
                    for f, g, h, bp, s in uniform_cost_search(grid, grid[start], grid[goal]):
                        pass
                    s_paths[map_num-1, sg_pair] = s_path = path_cost(grid, bp, s)
                algo = partial(a, grid, grid[start], grid[goal])
                print("Forking to run {0}".format(name))
                newpid = os.fork()  # Fork the process so we get a separate memory footprint
                if newpid is 0:
                    benchmarks = run_algo(algo, grid, s_path)
                    with open('csv/' + name + str(hs) + str(w1) + str(w2) + '.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(list(benchmarks))
                    os._exit(0)
                else:
                    os.wait4(newpid, 0)

        with open('csv/' + fname, 'a') as csvwritefile:
            with open('csv/' + name + str(hs) + str(w1) + str(w2) + '.csv', 'r') as csvreadfile:
                # reader = csv.reader(csvreadfile, quoting=csv.QUOTE_MINIMAL)
                writer = csv.writer(csvwritefile, quoting=csv.QUOTE_MINIMAL)
                m = np.genfromtxt(csvreadfile, dtype='float', delimiter=' ')
                # m = np.array([r for r in reader])
                row = [name, hs, w1, w2]
                for c in m.T:
                    row.append(np.mean(c))
                writer.writerow(row)

if __name__ == '__main__':
    main()
