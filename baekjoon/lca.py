import sys 
import math
from collections import defaultdict

sys.setrecursionlimit(100000)

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
        
        # index_visit = min(range(L, R+1), key=lambda i:self.level[i]) # can be O(nlogn) preprocess and O(1) query with sparse table
        # return self.visit[index_visit]
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
        
N = int(sys.stdin.readline().rstrip())

adj = defaultdict(set)
for _ in range(N-1):
    s,e  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[s-1].add(e-1)
    adj[e-1].add(s-1)

lca = LCA(adj)
lca.preprocess(0)
    
M = int(sys.stdin.readline().rstrip())
Q = [[int(d) for d in sys.stdin.readline().rstrip().split()] for _ in range(M)]

for q in Q:
    print(lca.lca_query(q[0]-1, q[1]-1)+1)
    
