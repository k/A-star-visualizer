import maps
from grid import grid

g = grid()

print 'Testing rough'
r = maps.gen_rough(g)

print 'Testing gen_highways'
h = None
while h is None:
    try:
        h = maps.gen_highways(r)
    except Exception as e:
        print e
        print 'Retrying'


print 'Testing blocked'
b = maps.gen_blocked(h)

print 'Testing start_goal'
(start, goal) = maps.gen_start_goal(g)

print 'Writing to output file'
maps.output_file(b, start, goal)
