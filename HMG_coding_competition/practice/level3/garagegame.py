import sys
import copy
import time

N = int(sys.stdin.readline().rstrip())

list_cars_init = [[0] * N for _ in range(3*N)]
set_coord_garage = set([(i,j) for i in range(2*N,3*N) for j in range(N)])
for i in range(3*N):
    for j, val in enumerate(sys.stdin.readline().split()):
        list_cars_init[i][j] = val

def fall(list_cars):
    set_move = set()
    for j in range(N):
        for i in range(3*N-1, 2*N-1, -1):
            if list_cars[i][j] == 0:
                inspect_i = i-1
                while list_cars[inspect_i][j] == 0 and inspect_i >= 0:
                    inspect_i -= 1
                if inspect_i >= 0:
                    set_move.add((inspect_i, j, list_cars[inspect_i][j]))
                    list_cars[i][j] = list_cars[inspect_i][j]
                    list_cars[inspect_i][j] = 0
                    
    return set_move


def get_neighbors(coord):
    list_neighbors = []
    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
        if 2*N <= coord[0]+dy and coord[0]+dy < 3*N and 0 <= coord[1]+dx and coord[1]+dx < N:
            list_neighbors.append((coord[0]+dy, coord[1]+dx))
    return list_neighbors


def erase(list_cars, coord):
    y, x = coord
    color = list_cars[y][x]
    set_neighbors = set([coord])
    set_visited = set([coord])
    min_x = x
    max_x = x
    min_y = y
    max_y = y
    while len(set_neighbors)!=0:
        coord = set_neighbors.pop()
        list_cars[coord[0]][coord[1]] = 0
        min_x = min(min_x, coord[1])
        max_x = max(max_x, coord[1])
        min_y = min(min_y, coord[0])
        max_y = max(max_y, coord[0])
        list_neighbors = get_neighbors(coord)
        for neighbor in list_neighbors:
            if list_cars[neighbor[0]][neighbor[1]] == color and neighbor not in set_visited:
                set_neighbors.add(neighbor)
                set_visited.add(neighbor)
    
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    min_rectangle = width * height

    score = len(set_visited) + min_rectangle
    
    return set_visited, score

def revert_list_cars(list_cars, set_erase, color_erased, set_move):
    for coord in set_erase:
        list_cars[coord[0]][coord[1]] = color_erased
    for coord_color in set_move:
        list_cars[coord_color[0]][coord_color[1]] = coord_color[2]

def run(list_cars, curr_score, n_steps):
    if n_steps==0:
        return curr_score
    else:
        st = time.time()
        best_score = curr_score
        set_garage = set_coord_garage.copy()
        while len(set_garage) > 0:
            coord = set_garage.pop()
            color_erased = list_cars[coord[0]][coord[1]]
            set_erase, score = erase(list_cars, coord)
            set_move = fall(list_cars)
            score_after_run = run(list_cars, curr_score + score, n_steps-1)
            revert_list_cars(list_cars, set_erase, color_erased, set_move)
            best_score = max(best_score, score_after_run)
            set_garage -= set_erase
        return best_score

best_score = run(list_cars_init, 0, 3)
print(best_score)