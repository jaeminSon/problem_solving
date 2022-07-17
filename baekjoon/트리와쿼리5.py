import sys
from collections import defaultdict
from heapq import heappop, heappush

sys.setrecursionlimit(200000)

N = int(sys.stdin.readline().rstrip())

adj2 = defaultdict(set)
adj = defaultdict(set)
for _ in range(N-1):
    s,e  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[s-1].add(e-1)
    adj[e-1].add(s-1)
    adj2[s-1].add(e-1)
    adj2[e-1].add(s-1)

def centroid_decomposition(adjacency_list:dict):
    
    list_size = [0]*(max(adjacency_list.keys())+1)
    
    def get_size(node, parent):
        list_size[node] = 1
        for ne in adjacency_list[node]:
            if ne != parent:
                list_size[node] += get_size(ne, node)
        return list_size[node]

    def get_centroid(node, parent, n_nodes):
        for ne in adjacency_list[node]:
            if ne != parent and list_size[ne]*2 > n_nodes:
                return get_centroid(ne, node, n_nodes)
        return node

    def _recursive(node):
        if len(adjacency_list[node]) == 0:
            children[node] = set()
            return node
        else:
            n_nodes = get_size(node,-1)
            c = get_centroid(node, -1, n_nodes)
            
            neighbors = adjacency_list[c]
            
            for ne in adjacency_list[c]:
                adjacency_list[ne].remove(c)
            del adjacency_list[c]
            
            for ne in neighbors:
                next_c = _recursive(ne)
                children[c].add(next_c)
                parent[next_c] = c
                
            return c
    
    children = defaultdict(set)
    parent = defaultdict(int)
    
    root = _recursive(min(adjacency_list.keys()))
    parent[root] = -1
    
    return root, parent, children

root, parent, children = centroid_decomposition(adj)

import math

class LCA:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.n_nodes = len(adjacency_list)
    
    def preprocess(self, root):
        self.level = [None] * (2*self.n_nodes-1)
        self.visit = [None] * (2*self.n_nodes-1)
        self.appear = [None] * self.n_nodes
        self.depth = [None] * self.n_nodes
        
        self.step = 0
        
        self.dfs(root,0)
        
        self.build_sparse_table()
        
    def dfs(self, node, l):
        self.appear[node] = self.step
        self.depth[node] = l
        self.visit[self.step] = node
        self.level[self.step] = l
        self.step+=1
        for ch in self.adjacency_list[node]:
            if self.appear[ch] is None:
                self.dfs(ch, l+1)
                self.visit[self.step] = node
                self.level[self.step] = l
                self.step+=1
        
    def build_sparse_table(self):
        n = 2*self.n_nodes-1
        self.sparse_table = [[0]*int(math.log2(n)+1) for _ in range(n)]
        for i in range(n):
            self.sparse_table[i][0] = (self.level[i], i)
        
        j = 1
        while (1 << j) <= n:
            i = 0
            while i + (1 << j) - 1 < n:
                # min in [i, i+2^j-1] = min(min in [i,i+2^(j-1)-1], min in [i+2^(j-1), i+2^j-1])
                if self.sparse_table[i][j - 1][0] > self.sparse_table[i + (1 << (j - 1))][j - 1][0]:
                    self.sparse_table[i][j] = self.sparse_table[i + (1 << (j - 1))][j - 1]
                else:
                    self.sparse_table[i][j] = self.sparse_table[i][j - 1]
                i += 1
            j += 1    
        
    def lca_query(self, node1, node2):
        if node1 == node2:
            return node1
        elif self.appear[node1] <= self.appear[node2]:
            L, R = self.appear[node1], self.appear[node2]
        else:
            L, R = self.appear[node2], self.appear[node1]
        
        j = int(math.log2(R - L + 1))

        if self.sparse_table[L][j][0] > self.sparse_table[R - (1 << j) + 1][j][0]:
            return self.visit[self.sparse_table[R - (1 << j) + 1][j][1]]
        else:
            return self.visit[self.sparse_table[L][j][1]]

    def dist_query(self, node1, node2):
        if node1 == node2:
            return 0
        else:
            lca = self.lca_query(node1, node2)
            return (self.depth[node1]-self.depth[lca]) + (self.depth[node2]-self.depth[lca])
        
lca = LCA(adj2)
lca.preprocess(root)

def flip(v):
    is_white[v] = not is_white[v]
    u = v
    while u != -1:
        heappush(min_dist[u], (lca.dist_query(v, u), v))
        u = parent[u]

def query(v):
    ans = N
    u = v
    while u!=-1:
        while len(min_dist[u]) > 0:
            if not is_white[min_dist[u][0][1]]:
                heappop(min_dist[u])
            else:
                ans = min(ans, min_dist[u][0][0] + lca.dist_query(v, u))
                break
        u = parent[u]
    
    if ans == N:
        return -1
    else:
        return ans

is_white = [False] * N
min_dist = defaultdict(list)
M = int(sys.stdin.readline().rstrip())
Q = [[int(d) for d in sys.stdin.readline().rstrip().split()] for _ in range(M)]

for t, v in Q:
    if t==1:
        flip(v-1)
    else:
        print(query(v-1))
