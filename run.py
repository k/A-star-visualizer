import maps
from grid import grid
from search import UniformCostSearch, AStar, AStarWeighted

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
(start, goal) = maps.gen_start_goal(g)

print('Writing to output file')
maps.output_file(g, start, goal)

print('Running Uniform Cost Search')
print(UniformCostSearch.search(g, start, goal))

