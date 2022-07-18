import sys
from collections import defaultdict, OrderedDict
from heapq import heappop, heappush

sys.setrecursionlimit(200000)

N = int(sys.stdin.readline().rstrip())

adj2 = defaultdict(dict)
adj = defaultdict(set)
for _ in range(N-1):
    s,e, l  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[s-1].add(e-1)
    adj[e-1].add(s-1)
    adj2[s-1][e-1] = -l
    adj2[e-1][s-1] = -l
    
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
        self.dist = [None] * self.n_nodes
        
        self.step = 0
        
        self.dfs(root,0,0)
        
        self.build_sparse_table()
        
    def dfs(self, node, l, d):
        self.appear[node] = self.step
        self.dist[node] = d
        self.visit[self.step] = node
        self.level[self.step] = l
        self.step+=1
        for ch in self.adjacency_list[node]:
            if self.appear[ch] is None:
                self.dfs(ch, l+1, d+self.adjacency_list[node][ch])
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
            return (self.dist[node1]-self.dist[lca]) + (self.dist[node2]-self.dist[lca])
        
lca = LCA(adj2)
lca.preprocess(root)

def add_to_min_dist(elem):
    if elem not in set_global:
        heappush(min_dist_global, elem)
        set_global.add(elem)

def update_subtree(node):
    if len(best2[node]) > 0:
        add_to_min_dist(best2[node][0])

def update_other_subtrees(v):
    if len(best2[v]) == 2:
        smallest = best2[v][0]
        second_small = best2[v][1]
        new_elem = (smallest[0]+second_small[0], smallest[1], second_small[1])
        new_elem_eq = (smallest[0]+second_small[0], second_small[1], smallest[1])
        if new_elem_eq not in set_global:                
            add_to_min_dist(new_elem)

def update_dist_branch(p, ch, new_elem):
    if new_elem not in set_dist_branch:
        heappush(min_dist_branch[p][ch], new_elem) # O(log N)
        set_dist_branch.add(new_elem)

def update_best2(p, new_elem):
    if len(best2[p]) == 0:
        best2[p].append(new_elem)
    elif len(best2[p]) == 1:
        if best2[p][0][0] <= new_elem[0]:
            best2[p].append(new_elem)
        else:
            best2[p].insert(0, new_elem)
    elif len(best2[p]) == 2:
        if best2[p][0][0] <= new_elem[0] and best2[p][1][0] > new_elem[0]:
            best2[p][1] = new_elem
        else:
            best2[p][1] = best2[p][0]
            best2[p][0] = new_elem

def flip(v):
    is_white[v] = not is_white[v]
    if is_white[v]:
        n_white[0] += 1
        
        update_subtree(v) #O(1)

        ch = v
        p = parent[v]
        while p != -1:
            
            new_elem = (lca.dist_query(v, p), v, p)
            update_dist_branch(p, ch, new_elem)
            update_best2(p, new_elem)
            
            if is_white[p]:
                add_to_min_dist(new_elem) # O(log N)
            
            update_other_subtrees(p) #O(1)
            
            ch = p
            p = parent[p]
    else:
        n_white[0] -= 1
        
        ch = v
        p = parent[v]
        while p != -1:
            while min_dist_branch[p][ch] and not is_white[min_dist_branch[p][ch][0][1]]:
                set_dist_branch.remove(min_dist_branch[p][ch][0])
                heappop(min_dist_branch[p][ch])
            ch = p
            p = parent[p]

def query():
    if n_white[0] == 0:
        return -1
    elif n_white[0] == 1:
        return 0
    else:
        while min_dist_global:
            dist, u, v = min_dist_global[0]
            if is_white[u] and is_white[v]:
                return max(-dist, 0)
            else:
                set_global.remove((dist, u, v))
                heappop(min_dist_global)

is_white = [False] * N
n_white = [0]
min_dist_branch = defaultdict(dict)
best2 = defaultdict(list)
def initialize(node):
    for ch in children[node]:
        min_dist_branch[node][ch] = []
        initialize(ch)
initialize(root)

min_dist_global = []
set_global = set()
set_dist_branch = set()

for i in range(N):
    flip(i)

M = int(sys.stdin.readline().rstrip())
Q = [[int(d) for d in sys.stdin.readline().rstrip().split()] for _ in range(M)]

for q in Q:
    if q[0]==1:
        flip(q[1]-1)
    else:
        print(query())

