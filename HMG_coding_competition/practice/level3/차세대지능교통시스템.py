import sys

N, T = [int(el) for el in sys.stdin.readline().split()]

list_map = [[0]*N for _ in range(N)]

for i in range(N*N):
    list_map[i//N][i%N] = [int(el) - 1 for el in sys.stdin.readline().split()]

list_signal = [0]*12
list_signal[0] = [3, 0, 1, 2] # [start, dest1, dest2,...]
list_signal[1] = [2, 0, 1, 3]
list_signal[2] = [1, 0, 2, 3]
list_signal[3] = [0, 1, 2, 3]
list_signal[4] = [3, 0, 1]
list_signal[5] = [2, 0, 3]
list_signal[6] = [1, 2, 3]
list_signal[7] = [0, 1, 2]
list_signal[8] = [3, 1, 2]
list_signal[9] = [2, 0, 1]
list_signal[10] = [1, 0, 3]
list_signal[11] = [0, 2, 3]

def move(coord, direction):
    if direction == 0:
        # up
        return (coord[0]-1, coord[1], 2)
    elif direction == 1:
        # right
        return (coord[0], coord[1]+1, 3)
    elif direction == 2:
        # down
        return (coord[0]+1, coord[1], 0)
    elif direction == 3:
        # left
        return (coord[0], coord[1]-1, 1)
    

def inbound(coord, side):
    y, x = coord
    return 0 <= y and y < side and 0 <= x and x < side

set_leaf = set([(0,0,2)])
set_visited = set()
travel_time = 0
while travel_time <= T:
    new_set_leaf = set()
    for leaf in set_leaf:
        set_visited.add((leaf[0], leaf[1]))
        list_signal_at_intersection = list_map[leaf[0]][leaf[1]]
        current_signal = list_signal_at_intersection[travel_time % len(list_signal_at_intersection)]
        info_direction = list_signal[current_signal]
        if info_direction[0] == leaf[2]:
            for i in range(1, len(info_direction)):
                cand = move((leaf[0], leaf[1]), info_direction[i])
                if inbound((cand[0], cand[1]), N):
                    new_set_leaf.add(cand)
                    
    set_leaf = new_set_leaf
    travel_time += 1

print(len(set_visited))

