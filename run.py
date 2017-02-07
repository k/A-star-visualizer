import maps
from grid import blank_grid
from heuristic import make_admissibile, diagonal_distance, manhattan_distance, euclidian_distance
from search import uniform_cost_search, a_star, path
from gen_image import output_image

grid = blank_grid()

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

print('Testing start_goal')
(start, goal) = maps.gen_start_goal_pair(grid)

print('Writing to output file')
maps.output_file(grid, start, goal)

g = None
h = None
path = None

print('Running Uniform Cost Search')
ucs = uniform_cost_search(grid, start, goal)
for (g, h, parent, curr) in ucs:
    pass
print(g[goal])
output_image(grid, "ucs.png", start, goal, path[curr])


print('Running A* Search')
astar = a_star(grid, start, goal, make_admissible(manhattan_distance))
for (g, h, parent, curr) in astar:
    pass
print(g[goal])
output_image(grid, "a_star.png", start, goal, path[curr])

print('Running A* Weighted Search')
astar_w = a_star(grid, start, goal, diagonal_distance, w=2)
for (g, h, parent, curr) in astar_w:
    pass
print(g[goal])

print('Outputting map to map.txt')
output_image(grid, "a_star_w.png", start, goal, path[curr])
