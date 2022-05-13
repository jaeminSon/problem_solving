import sys

H, W = [int(el) for el in sys.stdin.readline().split()]

list_map = [[False]*W for _ in range(H)]

for i in range(H):
    for j, ch in enumerate(sys.stdin.readline().rstrip()):
        list_map[i][j] = (ch =="#")

def get_init_coord(l):
    for i in range(H):
        for j in range(W):
            if l[i][j]:
                return (i,j)

def get_neighbor(l, coord):
    list_neighbors = []
    y, x = coord
    if y > 0 and l[y-1][x]:
        list_neighbors.append((y-1,x))
    if x > 0 and l[y][x-1]:
        list_neighbors.append((y,x-1))
    if y < len(l)-1 and l[y+1][x]:
        list_neighbors.append((y+1,x))
    if x < len(l[0])-1 and l[y][x+1]:
        list_neighbors.append((y,x+1))

    return list_neighbors

def get_direction_from_points(coord, new_coord):
    if new_coord[0]==coord[0]-1:
        return "up"
    elif new_coord[0]==coord[0]+1:
        return "down"
    elif new_coord[1]==coord[1]-1:
        return "left"
    elif new_coord[1]==coord[1]+1:
        return "right"

def move(coord, orientation, list_checked, step=2):
    if orientation=="down":
        for k in range(step+1):
            list_checked[coord[0]+k][coord[1]] = True
        return (coord[0]+step, coord[1])
    elif orientation=="up":
        for k in range(step+1):
            list_checked[coord[0]-k][coord[1]] = True
        return (coord[0]-step, coord[1])
    elif orientation=="left":
        for k in range(step+1):
            list_checked[coord[0]][coord[1]-k] = True
        return (coord[0], coord[1]-step)
    elif orientation=="right":
        for k in range(step+1):
            list_checked[coord[0]][coord[1]+k] = True
        return (coord[0], coord[1]+step)

def turn(curr_orientation, target_orientation):
    dict_ori = {"up":0, "right":1, "down":2, "left":3}
    rotation = (dict_ori[curr_orientation] - dict_ori[target_orientation]) % 4
    if rotation==1:
        return "L"
    elif rotation==3:
        return "R"
    else:
        return None

def find_starting_point(list_map):
    list_checked = [[False]*W for _ in range(H)]
    coord = get_init_coord(list_map)
    while True:
        neighbors = get_neighbor(list_map, coord)
        if len(neighbors) == 1:
            return coord
        elif len(neighbors) == 2:
            if all([not list_checked[ne[0]][ne[1]] for ne in neighbors]):
                next_coord = neighbors[0]
            else:
                next_coord = [ne for ne in neighbors if not list_checked[ne[0]][ne[1]]][0]
            
            orientation = get_direction_from_points(coord, next_coord)
            move(coord, orientation, list_checked, step=1)
            coord = next_coord
        else:
            raise ValueError("neighbors should be one or two")

def find_starting_orientation(list_map, starting_point):
    neighbors = get_neighbor(list_map, starting_point)
    if len(neighbors)==0:
        return "right", len(neighbors)
    elif len(neighbors)==1:
        next_coord = neighbors[0]
        return get_direction_from_points(starting_point, next_coord), len(neighbors)
    else:
        raise ValueError("neighbors should be 0 or 1 at the starting point")

def navigate(list_map, starting_point, starting_orientation):
    list_checked = [[False]*W for _ in range(H)]
    coord = starting_point
    orientation = starting_orientation
    list_checked[coord[0]][coord[1]] = True
    list_navigation = []
    while True:
        neighbors = get_neighbor(list_map, coord)
        if len(neighbors) == 1 and (coord!=starting_point):
            return list_navigation
        else:
            next_coord = [ne for ne in neighbors if not list_checked[ne[0]][ne[1]]][0]
            new_orientation = get_direction_from_points(coord, next_coord)
            if orientation != new_orientation:
                turning_ori = turn(orientation, new_orientation)
                list_navigation.append(turning_ori)
                orientation = new_orientation
            list_navigation.append("A")
            coord = move(coord, orientation, list_checked, step=2)

starting_point = find_starting_point(list_map)
print("{} {}".format(starting_point[0]+1, starting_point[1]+1))

dict_starting_orientation = {"up":"^", "down":"v", "right":">", "left":"<"}
starting_orientation, n_neighbors = find_starting_orientation(list_map, starting_point)
print(dict_starting_orientation[starting_orientation])
if n_neighbors==0:
    print("")
else:
    list_navigation = navigate(list_map, starting_point, starting_orientation)
    print("".join(list_navigation))
