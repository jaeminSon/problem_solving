import sys

N = int(sys.stdin.readline().rstrip())

list_visited = [[False for _ in range(N)] for _ in range(N)]
list_obstacle = [[False for _ in range(N)] for _ in range(N)]

for i in range(N):
    list_obstacle[i] = [int(el) for el in sys.stdin.readline().rstrip()]

list_blobs = []
queue = []
for i in range(N):
    for j in range(N):
        if not list_visited[i][j] and list_obstacle[i][j]:
            queue.append((i,j))
            count = 0
            while queue:
                curr_i, curr_j = queue.pop()
                if not list_visited[curr_i][curr_j]: 
                    count+=1
                    list_visited[curr_i][curr_j]=True
                    neighbors = [(curr_i-1, curr_j), (curr_i+1, curr_j), (curr_i, curr_j-1), (curr_i, curr_j+1)]
                    for neighbor in neighbors:
                        check_i, check_j = neighbor
                        if check_i>=0 and check_i<N and check_j>=0 and check_j<N and (not list_visited[check_i][check_j]) and list_obstacle[check_i][check_j]:
                            queue.append((check_i, check_j))
            list_blobs.append(count)

list_blobs = sorted(list_blobs)
print(len(list_blobs))
for size in list_blobs:
    print(size)