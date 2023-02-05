import sys
from collections import defaultdict


def find(parent: list, i: int):
    if parent[i] != i:
        parent[i] = find(parent, parent[i])
    return parent[i]


def union(parent, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)
    if xroot != yroot:
        parent[yroot] = xroot
        return True
    else:
        return False


m, n, q = [int(d) for d in sys.stdin.readline().rstrip().split()]

grid = [[0]*n for _ in range(m)]
for i in range(m):
    row = [int(d) for d in sys.stdin.readline().rstrip().split()]
    for j, v in enumerate(row):
        grid[i][j] = v
edges = []
for i in range(m):
    for j in range(n):
        if i < m-1:
            edges.append((n*i+j, n*(i+1)+j, max(grid[i+1][j], grid[i][j])))
        if j < n-1:
            edges.append((n*i+j, n*i+(j+1), max(grid[i][j+1], grid[i][j])))
edges.sort(key=lambda x: x[2])

ori_queries = [[int(d)-1 for d in sys.stdin.readline().rstrip().split()]
               for _ in range(q)]
queries_node = {i: [q[0]*n+q[1], q[2]*n+q[3]]
                for i, q in enumerate(ori_queries) if q[0] != q[2] or q[1] != q[3]}
ans = [grid[q[0]][q[1]] if i not in queries_node else 0 for i,
       q in enumerate(ori_queries)]

n_edges = len(edges)
l = {i:1 for i in queries_node}
r = {i:n_edges for i in queries_node}

while True:
    # group queries by mid point
    mid2query = defaultdict(list)
    finished = True
    for i in queries_node:
        if l[i] <= r[i]:  # binary search of [l,r]
            finished = False
            mid2query[(l[i] + r[i]) // 2].append(i)
    if finished:
        break

    # run algorithm and handle each query
    parent = [node for node in range(n_edges)]
    for i, (s, t, w) in enumerate(edges):
        op_count = i + 1
        union(parent, s, t)
        for index_query in mid2query[op_count]:
            if find(parent, queries_node[index_query][0]) == find(parent, queries_node[index_query][1]):
                ans[index_query] = w
                r[index_query] = op_count - 1
            else:
                l[index_query] = op_count + 1

for anw in ans:
    print(anw)
