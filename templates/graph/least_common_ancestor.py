import math

class LCA:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.n_nodes = len(adjacency_list)
    
    def preprocess(self,):
        self.level = [None] * (2*self.n_nodes-1)
        self.visit = [None] * (2*self.n_nodes-1)
        self.appear = [None] * self.n_nodes
        self.depth = [None] * self.n_nodes
        
        self.step = 0
        
        self.dfs(0,0)
        
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
            self.sparse_table[i][0] = self.level[i]
        
        j = 1
        while (1 << j) <= n:
            i = 0
            while i + (1 << j) - 1 < n:
                # min in [i, i+2^j-1] = min(min in [i,i+2^(j-1)-1], min in [i+2^(j-1), i+2^j-1])
                self.sparse_table[i][j] = min(self.sparse_table[i][j - 1], self.sparse_table[i + (1 << (j - 1))][j - 1])
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

        return self.visit[min(self.sparse_table[L][j], self.sparse_table[R - (1 << j) + 1][j])]

    def dist_query(self, node1, node2):
        if node1 == node2:
            return 0
        else:
            lca = self.lca_query(node1, node2)
            return (self.depth[node1]-self.depth[lca]) + (self.depth[node2]-self.depth[lca])
        


if __name__=="__main__":
    lca = LCA([[1,7],[2,3,6],[],[4,5],[],[],[],[8,9],[],[]]) # directed representation of tree
    lca.preprocess()
    assert lca.lca_query(4,6) == 1
    
    lca = LCA([[1,7],[0,2,3,6],[1],[1,4,5],[3],[3],[1],[0,8,9],[7],[7]]) # undirected representation of tree
    lca.preprocess()
    assert lca.lca_query(4,6) == 1
    assert lca.lca_query(5,5) == 5
    assert lca.dist_query(1,1) == 0
    assert lca.dist_query(0,8) == 2