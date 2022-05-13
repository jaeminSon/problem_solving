import sys
from queue import PriorityQueue

R, C = [int(el) for el in sys.stdin.readline().split()]

set_coord_rain = set()
set_coord_river = set()
for i in range(R):
    for j, ch in enumerate(sys.stdin.readline().rstrip()):
        if j <= C:
            if ch == "H":
                home = (i,j)
            elif ch == "W":
                work = (i,j)
            elif ch == "*":
                set_coord_rain.add((i,j))
            elif ch == "X":
                set_coord_river.add((i,j))

def inbound(coord, R, C):
    y, x = coord
    return 0 <= y and y < R and 0 <= x and x < C

def get_neighbors(coord, R, C):
    list_neighbors = []
    for delta_i in [-1,0,1]:
        for delta_j in [-1,0,1]:
            if abs(delta_i)+abs(delta_j) == 1:
                cand = (coord[0] + delta_i, coord[1] + delta_j)
                if inbound(cand, R, C):
                    list_neighbors.append(cand)
    return list_neighbors

def update_rain(set_coord_rain, set_forbidden, R, C):
    new_set_coord_rain = set_coord_rain.copy()
    for coord in set_coord_rain:
        list_neighbors = get_neighbors(coord, R, C)
        for neighbor in list_neighbors:
            if neighbor not in set_forbidden:
                new_set_coord_rain.add(neighbor)
    return new_set_coord_rain

answer = "FAIL"
set_visited = set()
set_visited.add(work)
set_leaf = set([work])
travel_time = 0
found_answer = False
while not found_answer and len(set_leaf)!=0:
    travel_time += 1
    set_coord_rain = update_rain(set_coord_rain, set_coord_river.union(set([home])), R, C)
    set_new_leaf = set()
    for coord in set_leaf:
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = (coord[0]+dy, coord[1]+dx) 
            if inbound(neighbor, R, C) and neighbor not in set_visited:
                set_visited.add(neighbor)
                if neighbor == home:
                    answer = travel_time
                    found_answer = True
                elif (neighbor not in set_coord_rain) and (neighbor not in set_coord_river):
                    set_new_leaf.add(neighbor)
    
    set_leaf = set_new_leaf

print(answer)

