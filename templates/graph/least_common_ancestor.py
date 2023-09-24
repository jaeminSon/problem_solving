import sys
sys.path.append("..")
import math
from custom_type import TREE


class LCA_SPRASE_TABLE:
    def __init__(self, adjacency_list: TREE):
        self.adjacency_list = adjacency_list
        self.n_nodes = len(adjacency_list)

    def preprocess(self, root):
        self.level = [None] * (2*self.n_nodes-1)
        self.visit = [None] * (2*self.n_nodes-1)
        self.appear = [None] * self.n_nodes
        self.depth = [None] * self.n_nodes

        self.step = 0

        self.dfs(root, 0)

        self.build_sparse_table()

    def dfs(self, node, l):
        self.appear[node] = self.step
        self.depth[node] = l
        self.visit[self.step] = node
        self.level[self.step] = l
        self.step += 1
        for ch in self.adjacency_list[node]:
            if self.appear[ch] is None:
                self.dfs(ch, l+1)
                self.visit[self.step] = node
                self.level[self.step] = l
                self.step += 1

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


class LCA_LOGARITHM:
    def __init__(self, adjacency_list: TREE):
        self.adjacency_list = adjacency_list
        self.n_nodes = len(adjacency_list)

    def preprocess(self, root, n_nodes, log_max_height):
        self.n_nodes = n_nodes
        self.log_max_height = log_max_height

        self.dp_parent = [[-1]*n_nodes for _ in range(log_max_height)]
        self.depth = [0]*n_nodes
        self.visit = [False]*n_nodes

        self.dfs(root, -1, 0)

        self.dp()

    def dfs(self, curr, parent, depth):
        self.visit[curr] = True
        self.dp_parent[0][curr] = parent
        self.depth[curr] = depth
        for ch in self.adjacency_list[curr]:
            if not self.visit[ch]:
                self.dfs(ch, curr, depth+1)

    def dp(self):
        for i in range(1, self.log_max_height):
            for j in range(self.n_nodes):
                self.dp_parent[i][j] = self.dp_parent[i-1][self.dp_parent[i-1][j]]

    def go_up(self, node, dist):
        for i in range(self.log_max_height):
            if (dist >> i) & 1:
                node = self.dp_parent[i][node]
        return node

    def lca_query(self, node1, node2):
        if self.depth[node1] > self.depth[node2]:
            node1, node2 = node2, node1
        node2 = self.go_up(node2, self.depth[node2]-self.depth[node1])
        if node1 == node2:
            return node1
        else:
            for i in range(self.log_max_height-1, -1, -1):
                if self.dp_parent[i][node1] != self.dp_parent[i][node2]:
                    node1 = self.dp_parent[i][node1]
                    node2 = self.dp_parent[i][node2]
            return self.dp_parent[0][node1]


if __name__ == "__main__":
    lca = LCA_SPRASE_TABLE([[1, 7], [2, 3, 6], [], [4, 5], [], [], [], [8, 9], [], []])  # directed representation of tree
    lca.preprocess(0)
    assert lca.lca_query(4, 6) == 1
    lca = LCA_LOGARITHM([[1, 7], [2, 3, 6], [], [4, 5], [], [], [], [8, 9], [], []])
    lca.preprocess(0, 10, 20)
    assert lca.lca_query(4, 6) == 1

    lca = LCA_SPRASE_TABLE([[1, 7], [0, 2, 3, 6], [1], [1, 4, 5], [3], [3], [1], [0, 8, 9], [7], [7]])  # undirected representation of tree
    lca.preprocess(0)
    assert lca.lca_query(4, 6) == 1
    assert lca.lca_query(5, 5) == 5
    assert lca.dist_query(1, 1) == 0
    assert lca.dist_query(0, 8) == 2

    lca = LCA_LOGARITHM([[1, 7], [0, 2, 3, 6], [1], [1, 4, 5], [3], [3], [1], [0, 8, 9], [7], [7]])  # undirected representation of tree
    lca.preprocess(0, 10, 20)
    assert lca.lca_query(4, 6) == 1
    assert lca.lca_query(5, 5) == 5
