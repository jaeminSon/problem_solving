import sys
import time
from collections import defaultdict

st = time.time()

N, H, W = [int(el) for el in sys.stdin.readline().split()]

image = [[0]*W for _ in range(H)]

for i in range(H):
    row = [int(el) for el in sys.stdin.readline().split()]
    for j in range(W):
        image[i][j] = row[j]


for _ in range(N):
    h, w, c = [int(el) for el in sys.stdin.readline().split()]
    h -= 1
    w -= 1

    mc = image[h][w]
    qu = set([(h, w)])
    # visited = defaultdict(lambda: False)
    visited = set()  # OK
    set_modif = set([(h,w)]) # takes long time
    while qu:
        i, j = qu.pop()
        image[i][j] = c
        # visited[(i, j)] = True
        visited.add((i,j))
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            y_cand = i + dy
            x_cand = j + dx
            coord_cand = (y_cand, x_cand)
            if 0 <= y_cand and y_cand < H and 0 <= x_cand and x_cand < W and not coord_cand in visited: #visited[coord_cand]:
                visited.add(coord_cand) # OK
                # visited[coord_cand] = True
                if image[y_cand][x_cand] == mc:
                    # qu.append(coord_cand)
                    qu.add(coord_cand)
                    set_modif.add(coord_cand) # takes long time

    # h, w, c = [int(el) for el in sys.stdin.readline().split()]
    # h -= 1
    # w -= 1
    #
    # mc = image[h][w]
    # set_modif = set([(h,w)])
    # set_children = set([(h,w)])
    # set_visited = set([(h,w)])
    # while len(set_children) > 0:
    #     new_set_children = set()
    #     for ch in set_children:
    #         for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
    #             y_cand = ch[0] + dy
    #             x_cand = ch[1] + dx
    #             coord_cand = (y_cand, x_cand)
    #             if 0 <= y_cand and y_cand < H and 0 <= x_cand and x_cand < W and coord_cand not in set_visited:
    #                 set_visited.add(coord_cand)
    #                 if image[y_cand][x_cand] == mc:
    #                     new_set_children.add(coord_cand)
    #                     set_modif.add(coord_cand)
    #
    #     set_children = new_set_children
    #
    # for el in set_modif: # takes long time
    #     y, x = el
    #     image[y][x] = c

for i in range(H):
    print(" ".join([str(el) for el in image[i]]))

print(time.time() - st)
