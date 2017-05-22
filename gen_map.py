import maps
from grid import blank_grid
from heuristic import *
from search import uniform_cost_search, a_star, path
from gen_image import output_image
import argparse

parser = argparse.ArgumentParser(description='Creates a randomly generated map text file')
parser.add_argument('output_file', metavar='map', type=str, default='map.txt',
                    help='The filename to be used as the output file')
parser.add_argument('--width', '-x' , metavar='#', type=int, default=160,
                    help='The width of the map')
parser.add_argument('--height', '-y' , metavar='#', type=int, default=120,
                    help='The height of the map')
args = parser.parse_args()

grid = blank_grid(args.width, args.height)

print('Testing rough')
grid = maps.gen_rough(grid)

print('Testing gen_highways')
h = None
while h is None:
    try:
        h = maps.gen_highways(grid)
    except Exception as e:
        print(e)
        print('Retrying')
grid = h

print('Testing blocked')
grid = maps.gen_blocked(grid)
i = 0
while i < 10:
    print('Start/Goal Pair: ' + str(i))
    g = None
    h = None
    parent = None
    curr = None

    try:
        print('Testing start_goal')
        (start, goal) = maps.gen_start_goal_pair(grid)

        print('Testing Uniform Cost Search')
        ucs = uniform_cost_search(grid, start, goal)
        for (f, g, h, parent, curr) in ucs:
            pass
        print(g[goal])
# output_image(grid, "ucs.png", start, goal, path(parent, curr))

        print('Testing A* Search')
        astar = a_star(grid, start, goal, manhattan_distance_a)
        for (f, g, h, parent, curr) in astar:
            pass
        print(g[goal])
# output_image(grid, "a_star.png", start, goal, path(parent, curr))

        print('Testing A* Weighted Search')
        astar_w = a_star(grid, start, goal, diagonal_distance_n, w=2)
        for (f, g, h, parent, curr) in astar_w:
            pass
        print(g[goal])

# output_image(grid, "a_star_w.png", start, goal, path(parent, curr))
        print('Writing to output file')
        maps.output_file(grid, start, goal, args.output_file + '_' + str(i) + '.txt')
    except TypeError as e:
        raise
    except Exception as e:
        print e
        continue
    i = i+1
