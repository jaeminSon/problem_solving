import sys

n, m = [int(d) for d in sys.stdin.readline().rstrip().split()]

edges = []
for _ in range(m):
    s, t, w = [int(d) for d in sys.stdin.readline().rstrip().split()]
    edges.append((s-1, t-1, w))
edges.sort(key=lambda x: x[2])

Q = int(sys.stdin.readline().rstrip())
queries = [[int(d)-1 for d in sys.stdin.readline().rstrip().split()]
           for _ in range(Q)]


def find(parent: list, i: int):
    if parent[i] != i:
        parent[i] = find(parent, parent[i])
    return parent[i]


def union(parent, n_nodes, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)
    if xroot != yroot:
        n_nodes[xroot] += n_nodes[yroot]
        parent[yroot] = xroot


l = [1] * Q
r = [m] * Q
ans = [[-1, -1]] * Q

while True:
    # group queries by mid point
    mid2query = {v:[] for v in range(1, m+1)}
    finished = True
    for i in range(len(queries)):
        if l[i] <= r[i]:  # binary search of [l,r]
            finished = False
            mid2query[(l[i] + r[i]) // 2].append(i)
    if finished:
        break

    # run algorithm and handle each query
    parent = [node for node in range(n)]
    n_nodes = [1] * n
    for i, (s, t, w) in enumerate(edges):
        op_count = i + 1
        union(parent, n_nodes, s, t)
        for index_query in mid2query[op_count]:
            if find(parent, queries[index_query][0]) == find(parent, queries[index_query][1]):
                ans[index_query] = [w, n_nodes[parent[s]]]
                r[index_query] = op_count - 1
            else:
                l[index_query] = op_count + 1

for i in range(Q):
    print(" ".join([str(el) for el in ans[i]]) if ans[i][0] != -1 else -1)
