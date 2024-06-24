import sys
import heapq
from collections import defaultdict


def dijkstra():
    queue = []
    distances = [1e9] * (N + 1)
    for i in range(K):
        heapq.heappush(queue, (0, festival[i]))
        distances[festival[i]] = 0
    while queue:
        current_distance, now_node = heapq.heappop(queue)
        if distances[now_node] < current_distance:
            continue
        for new_node, new_distance in adj[now_node]:
            total_distance = current_distance + new_distance
            if total_distance < distances[new_node]:
                distances[new_node] = total_distance
                heapq.heappush(queue, (total_distance, new_node))
    return distances


def make_set(n):
    for i in range(n):
        parent_node[i] = i
        rank[i] = i


def op_find(k):
    if parent_node[k] != k:
        parent_node[k] = op_find(parent_node[k])
    return parent_node[k]


def op_union(a, b):
    x = op_find(a)
    y = op_find(b)

    if rank[x] > rank[y]:
        parent_node[y] = x
    elif rank[x] < rank[y]:
        parent_node[x] = y
    else:
        parent_node[y] = x
        rank[x] += 1


N, M, K, Q = map(int, sys.stdin.readline().split())
adj = [[] for _ in range(N + 1)]
edges = []
distances = []
for _ in range(M):
    start, end, dist = map(int, sys.stdin.readline().split())
    adj[start].append((end, dist))
    adj[end].append((start, dist))
    if start < end:
        edges.append((start, end))
    else:
        edges.append((end, start))
festival = [int(sys.stdin.readline()) for _ in range(K)]

distances = dijkstra()

edges_by_distance = []
for s, e in edges:
    edges_by_distance.append((min(distances[s], distances[e]), s, e))

result = [0] * Q
node2qs = defaultdict(set)
for q in range(Q):
    start, end = map(int, sys.stdin.readline().split())
    node2qs[start].add(q)
    node2qs[end].add(q)

parent_node = [0] * (N+1)
rank = [0] * (N+1)
make_set(N+1)

edges_by_distance = sorted(edges_by_distance, reverse=True, key=lambda x: x[0])
for dist, s, e in edges_by_distance:
    low = op_find(s)
    high = op_find(e)
    if low == high:
        continue

    if low > high:
        low, high = high, low

    for q in node2qs[low]:
        if q in node2qs[high]:
            result[q] = dist
            node2qs[low].remove(q)
        else:
            node2qs[high].add(q)

    op_union(high, low)

for q in range(Q):
    print(result[q])
