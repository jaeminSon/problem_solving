import sys
import gc

N, M = [int(el) for el in sys.stdin.readline().split()]

set_ice = set()

for i in range(N):
    row = [int(el) for el in sys.stdin.readline().split()]
    for j, val in enumerate(row):
        if val == 1:
            set_ice.add((i+1, j+1))

def get_outside(set_ice, H, W):
    set_visited = set()
    set_outside = set([(0,0)])
    set_leaf = set([(0,0)])
    while len(set_leaf) > 0:
        new_set_leaf = set()
        set_visited = set_visited.union(set_leaf)
        for leaf in set_leaf:
            neighbors = get_neighbors(leaf, H, W)
            for neighbor in neighbors:
                if neighbor not in set_ice and neighbor not in set_visited:
                    new_set_leaf.add(neighbor)

        set_leaf = new_set_leaf
        set_outside = set_outside.union(set_leaf)

    return set_outside

def is_connected(chunk, coord, H, W):
    neighbors = get_neighbors(coord, H, W)
    for neighbor in neighbors:
        if neighbor in chunk:
            return True
    return False

def update_outside(set_outside, set_inner, H, W):
    for coord_melt in set_inner:
        if is_connected(set_outside, coord_melt, H, W):
            set_outside.add(coord_melt)

def inbound(coord, H, W):
    y, x = coord
    return 0 <= y and y < H and 0 <= x and x < W

def get_neighbors(coord, H, W):
    y, x = coord
    list_neighbors = []
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if abs(dx) + abs(dy) == 1:
                cand = (y+dy, x+dx)
                if inbound(cand, H, W):
                    list_neighbors.append(cand)
    return list_neighbors

def get_n_touches(set_outside, coord, H, W):
    n_touches = 0
    list_neighbors = get_neighbors(coord, H, W)
    for neighbor in list_neighbors:
        if neighbor in set_outside:
            n_touches += 1
                
    return n_touches

H = N + 1
W = M + 1
set_all = set()
for i in range(H):
    for j in range(W):
        set_all.add((i,j))
set_outside = get_outside(set_ice, H, W)

duration = 0
while len(set_ice) > 0:
    set_melt = set()
    for coord_ice in set_ice:
        n_touches = get_n_touches(set_outside, coord_ice, H, W)
        if n_touches >= 2:
            set_melt.add(coord_ice)            
    
    set_ice = set_ice - set_melt
    set_outside = get_outside(set_ice, H, W)
    duration += 1
    gc.collect()

print(duration)
