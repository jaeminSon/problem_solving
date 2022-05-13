class UnionFind:
    parent_node = {}

    def make_set(self, u):
        for i in u:
            self.parent_node[i] = i

    def op_find(self, k):
        if self.parent_node[k] == k:
            return k
        return self.op_find(self.parent_node[k])

    def op_union(self, a, b):
        x = self.op_find(a)
        y = self.op_find(b)
        self.parent_node[x] = y