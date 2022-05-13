import sys
import time

st = time.time()

N, H, W = [int(el) for el in sys.stdin.readline().split()]

image = [[0]*W for _ in range(H)]

for i in range(H):
    row = [int(el) for el in sys.stdin.readline().split()]
    for j in range(W):
        image[i][j] = row[j]

dict_pt2group = {}
dict_group2color = {}
dict_group2pts = {}
dict_group2neighbors = {}

all_points = set([(i,j) for i in range(H) for j in range(W)])
group = 0
dict_group2neigobor_pts = {}
while len(all_points) > 0:
    p = all_points.pop()
    c = image[p[0]][p[1]]
    set_modif = set([p])
    set_children = set([p])
    set_visited = set([p])
    while len(set_children) > 0:
        new_set_children = set()
        for ch in set_children:
            for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                y_cand = ch[0] + dy
                x_cand = ch[1] + dx
                coord_cand = (y_cand, x_cand)
                if 0 <= y_cand and y_cand < H and 0 <= x_cand and x_cand < W and coord_cand not in set_visited:
                    set_visited.add(coord_cand)
                    if image[y_cand][x_cand] == c:
                        new_set_children.add(coord_cand)
                        set_modif.add(coord_cand)

        set_children = new_set_children
    for p_modif in set_modif:
        dict_pt2group[p_modif] = group
    dict_group2color[group] = c
    dict_group2pts[group] = set_modif
    dict_group2neigobor_pts[group] = set_visited - set_modif
    all_points -= set_modif
    group+=1
assert sum([len(val) for val in dict_group2pts.values()]) == H * W
for group, pts_neighbor in dict_group2neigobor_pts.items():
    dict_group2neighbors[group] = set()
    for pt_neighbor in pts_neighbor:
        dict_group2neighbors[group].add(dict_pt2group[pt_neighbor])

print("preprocess: ", time.time() - st)

for _ in range(N):
    h, w, c = [int(el) for el in sys.stdin.readline().split()]
    h -= 1
    w -= 1

    mc = image[h][w]
    group = dict_pt2group[(h,w)]
    for p in dict_group2pts[group]:
        image[p[0]][p[1]] = c
    dict_group2color[group] = c

    set_neighbors_removed_group = set()
    set_removed_group = set()
    for g in dict_group2neighbors[group]:
        g_c = dict_group2color[g]
        if g_c == c:
            for p in dict_group2pts[g]:
                dict_pt2group[p] = group
            dict_group2pts[group] = dict_group2pts[group].union(dict_group2pts[g])
            set_neighbors_removed_group = set_neighbors_removed_group.union(dict_group2neighbors[g] - set([group]))
            dict_group2pts.pop(g)
            dict_group2color.pop(g)
            dict_group2neighbors.pop(g)
            set_removed_group.add(g)
    for key in dict_group2neighbors:
        dict_group2neighbors[key] -= set_removed_group
    for g in set_neighbors_removed_group:
        dict_group2neighbors[g] = dict_group2neighbors[g].union(set([group]))
    dict_group2neighbors[group] = dict_group2neighbors[group].union(set_neighbors_removed_group)

for i in range(H):
    print(" ".join([str(el) for el in image[i]]))

print(time.time() - st)
