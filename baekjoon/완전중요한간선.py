import sys
from collections import deque

def dinic(adjacency_list, source, sink, any_flow=False):
    
    n_nodes = len(adjacency_list)
    level = [None] * n_nodes
    
    def build_level_graph_via_bfs(source, sink):
        
        for v in range(n_nodes):
            level[v] = -1
        
        level[source] = 0
        q = deque([source])
        while q:
            u = q.popleft()
            for edge in adjacency_list[u]: # edge: (node, flow, capacity, index of reverse node)
                if level[edge[0]] < 0 and edge[1] < edge[2]:
                    level[edge[0]] = level[u]+1
                    q.append(edge[0])
                     
        return False if level[sink] < 0 else True
    
    
    def send_flow(u, flow, sink, n_edges_explored):
        if u == sink:
            return flow
 
        while n_edges_explored[u] < len(adjacency_list[u]):
            # edge: [node, flow, capacity, index of reverse node]
            edge = adjacency_list[u][n_edges_explored[u]]
            if level[edge[0]] == level[u]+1 and edge[1] < edge[2]:
                avail_flow = min(flow, edge[2]-edge[1])
                flow_sent = send_flow(edge[0],avail_flow,sink,n_edges_explored)
                if flow_sent and flow_sent > 0:
                    edge[1] += flow_sent
                    adjacency_list[edge[0]][edge[3]][1] -= flow_sent
                    return flow_sent
            n_edges_explored[u] += 1
    
    if any_flow:
        assert source != sink
        return build_level_graph_via_bfs(source,sink)
    else:
        if source == sink:
            return -1
            
        max_flow = 0
        while build_level_graph_via_bfs(source,sink):
            n_edges_explored = [0 for _ in range(n_nodes)]
            while True:
                flow = send_flow(source, float('inf'), sink, n_edges_explored)
                if flow is None:
                    break
                else:
                    max_flow += flow
        return max_flow

K = int(sys.stdin.readline().rstrip())
for _ in range(K):
    N,M  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    
    # edge: (node, flow, capacity, index of reverse node)
    adj_list = [[] for i in range(N)]
    for _ in range(M):
        f, t, b = [int(d) for d in sys.stdin.readline().rstrip().split()]
        forward_edge = [t-1, 0, b, len(adj_list[t-1])]
        backward_edge = [f-1, 0, 0, len(adj_list[f-1])]
        adj_list[f-1].append(forward_edge)
        adj_list[t-1].append(backward_edge)
    
    dinic(adj_list, 0, N-1)
    
    ans = 0
    for i in range(len(adj_list)):
        for e in adj_list[i]:
            if e[1] == e[2] > 0:
                if not dinic(adj_list, i, e[0], True):
                    ans+=1

    print(ans)