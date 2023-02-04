import sys
from collections import defaultdict
import heapq

n, b, s, r = [int(d) for d in sys.stdin.readline().rstrip().split()]

adj = defaultdict(dict)
reversed_adj = defaultdict(dict)
for i in range(r):
    u, v, w = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[u][v] = w
    reversed_adj[v][u] = w


def dijkstra(adjancy_list, s):
    distance = [float("inf")] * (n+1)
    distance[s] = 0
    visited = set([s])

    pq = [(0, s)]
    heapq.heapify(pq)
    while pq:
        cost, curr = heapq.heappop(pq)
        visited.add(curr)
        for next, cost in adjancy_list[curr].items():
            if next not in visited and distance[next] > distance[curr] + cost:
                distance[next] = distance[curr] + cost
                heapq.heappush(pq, (distance[next], next))

    return distance


branch2head = dijkstra(adj, b+1)
head2branch = dijkstra(reversed_adj, b+1)
dist = [branch2head[i] + head2branch[i] for i in range(1, b+1)]
dist = sorted(dist)
cum_sum = [0]
for i in range(len(dist)):
    cum_sum.append(cum_sum[-1]+dist[i])


def cost(k, j):
    return (j-k-1) * (cum_sum[j] - cum_sum[k])


def _recursive(i, m, n, l, r):
    if m > n:
        return
    else:
        mid = (m+n)//2
        opt_k = l
        for k in range(l, min(r+1, b)):
            c = (mid-k-1) * (cum_sum[mid] - cum_sum[k])
            if dp[i-1][k] + c < dp[i][mid]:
                dp[i][mid] = dp[i-1][k] + c
                opt_k = k

        _recursive(i, m, mid-1, l, opt_k)
        _recursive(i, mid+1, n, opt_k, r)


dp = [[float("inf")]*(b+1) for _ in range(s+1)]
for i in range(1, b+1):
    dp[1][i] = (i-1) * cum_sum[i]

for i in range(2, s+1):
    _recursive(i, 1, b, 1, b)

print(dp[s][b])
