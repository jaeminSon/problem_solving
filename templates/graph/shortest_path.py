import heapq
from collections import deque


def dijkstra(adjacency_list, s, t):
    
    n_nodes = len(adjacency_list)
    distance = [float("Inf")] * n_nodes
    distance[s] = 0
    visited = set([s])
    prev = {}
    
    pq = [(0, s)]
    heapq.heapify(pq)
    while pq:
        cost, curr = heapq.heappop(pq)
        if curr == t:
            break
        visited.add(curr)
        for next, cost in adjacency_list[curr]:
            if next not in visited and distance[next] > distance[curr] + cost: 
                distance[next] = distance[curr] + cost
                heapq.heappush(pq, (distance[next], next))
                prev[next] = curr

    def get_trajectory(node:int):
        if node != s:
            return get_trajectory(prev[node]) + [node]
        else:
            return [node]
    
    return get_trajectory(t), distance[t]
 
def bellman_ford(adjacency_list, s):
     
    n_nodes = len(adjacency_list)
    dist = [float("Inf")] * n_nodes
    dist[s] = 0

    for _ in range(n_nodes - 1):
        for u in range(n_nodes):
            for v, w in adjacency_list[u]:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w

    # check negative cycle
    for u in range(n_nodes):
        for v, w in adjacency_list[u]:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                return None # distance has no meaning with negative cycle
    
    return dist

def bellman_ford_fast(adjacency_list, s):
     
    n_nodes = len(adjacency_list)
    dist = [float("Inf")] * n_nodes
    dist[s] = 0
    push_count = [0] * n_nodes
    
    in_queue = [False] * n_nodes
    q = deque([s])
    while q:
        u = q.popleft()
        in_queue[u] = False
        if push_count[u] < n_nodes:
            for v, w in adjacency_list[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    if not in_queue[v]:
                        q.append(v)
                        in_queue[v] = True
                        push_count[v] += 1
        else:
            return None # negative cycle
            

    return dist


def floyd_warshall(adjacency_list):
   
    n_nodes = len(adjacency_list)

    dist = [[float("Inf")]*n_nodes for _ in range(n_nodes)]
    for i in range(n_nodes):
        dist[i][i]=0
    for s in range(n_nodes):
        for t, w in adjacency_list[s]:
            dist[s][t] = w
 
    for k in range(n_nodes):
        for i in range(n_nodes):
            for j in range(n_nodes):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
 
    return dist
    
if __name__ == "__main__":
    for t in range(9):
        print(dijkstra([[(1,4),(7,8)], [(0,4),(2,8),(7,11)], [(1,8),(3,7),(5,4),(8,2)], [(2,7),(4,9),(5,14)], [(3,9),(5,10)], [(2,4),(3,14),(4,10),(6,2)], [(5,2),(7,1),(8,6)], [(0,8),(1,11),(6,1),(8,7)], [(2,2),(6,6),(7,7)]], 0, t))
    """
    ([0], 0)
    ([0, 1], 4)
    ([0, 1, 2], 12)
    ([0, 1, 2, 3], 19)
    ([0, 7, 6, 5, 4], 21)
    ([0, 7, 6, 5], 11)
    ([0, 7, 6], 9)
    ([0, 7], 8)
    ([0, 1, 2, 8], 14)
    """ 
    
    print(bellman_ford([[(1,-1),(2,4)],[(2,3),(3,2),(4,2)], [], [(2,5),(1,1)],[(3,-3)]], 0)) # [0, -1, 2, -2, 1]
    print(bellman_ford_fast([[(1,-1),(2,4)],[(2,3),(3,2),(4,2)], [], [(2,5),(1,1)],[(3,-3)]], 0)) # [0, -1, 2, -2, 1]
    print(bellman_ford_fast([[(1,-1)],[(0,-1)]], 0)) # None (negative cycle)
    print(floyd_warshall([[(1,5),(3,10)], [(2,3)], [(3,1)], []])) # [[0, 5, 8, 9], [inf, 0, 3, 4], [inf, inf, 0, 1], [inf, inf, inf, 0]]
    