import sys
import copy
from itertools import combinations, product
from collections import Counter
import time

st = time.time()

N, K = [int(el) for el in sys.stdin.readline().split()]

list_point = []
for _ in range(N):
    y, x, color = [int(el) for el in sys.stdin.readline().split()]
    list_point.append((y,x,color))

min_area = 4_000_000

def get_area(list_points):
    y_max = max([p[0] for p in list_points])
    y_min = min([p[0] for p in list_points])
    x_max = max([p[1] for p in list_points])
    x_min = min([p[1] for p in list_points])
    area = (y_max-y_min)*(x_max-x_min)
    return area

def loop(accum_points, list_color):
    global min_area
    current_color = list_color[0]
    for point in dict_point[current_color]:
        tmp_accum_points = copy.deepcopy(accum_points)
        tmp_accum_points.add(point)
        curr_size = get_area(tmp_accum_points)
        if min_area > curr_size:
            if len(list_color) == 1:
                min_area = curr_size
            else:
                loop(tmp_accum_points, list_color[1:])
        else:
            if min_area < curr_size:
                continue

dict_point = {p[2]:[] for p in list_point}
for p in list_point:
    dict_point[p[2]].append((p[0], p[1]))

list_n_elements = [len(dict_point[i]) for i in range(1, K+1)]
indices_sorted_by_n = sorted(range(len(list_n_elements)), key=list_n_elements.__getitem__)
colors_sorted_by_n = [el+1 for el in indices_sorted_by_n]
loop(set(), colors_sorted_by_n)
print(min_area)
