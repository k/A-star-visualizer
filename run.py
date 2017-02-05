import maps
from grid import grid, diagonal_distance
from search import uniform_cost_search, a_star, a_star_weighted
from heuristic import make_admissible

g = grid()

print('Testing rough')
g = maps.gen_rough(g)

print('Testing gen_highways')
h = None
while h is None:
    try:
        h = maps.gen_highways(g)
    except Exception as e:
        print(e)
        print('Retrying')
g = h

print('Testing blocked')
g = maps.gen_blocked(g)

print('Testing start_goal')
(start, goal) = maps.gen_start_goal_pair(g)

print('Writing to output file')
maps.output_file(g, start, goal)

print('Running Uniform Cost Search')
print(uniform_cost_search(g, start, goal))

print('Running A* Search')
print(a_star(g, start, goal, make_admissible(diagonal_distance)))

print('Running A* Weighted Search')
print(a_star_weighted(g, start, goal))
