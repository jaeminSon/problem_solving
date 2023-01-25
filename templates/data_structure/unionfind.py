class UnionFind:
    parent_node = {}
    rank = {}

    def make_set(self, u):
        for i in u:
            self.parent_node[i] = i
            self.rank[i] = 0

    def op_find(self, k):
        if self.parent_node[k] != k:
            self.parent_node[k] = self.op_find(self.parent_node[k])
        return self.parent_node[k]

    def op_union(self, a, b):
        x = self.op_find(a)
        y = self.op_find(b)
        
        if self.rank[x] > self.rank[y]:
            self.parent_node[y] = x
        elif self.rank[x] < self.rank[y]:
            self.parent_node[x] = y
        else:
            self.parent_node[y] = x
            self.rank[x] += 1

class Arpa:
    # range-min-query in [L,R]
    def __init__(self, arr):
        self.arr = arr
        self.N = len(arr)
        self.dsu = list(range(self.N))
        
    def run(self, queries):
        Q = len(queries)
        qu = [[] for _ in range(self.N)]
        for i,(L,R) in enumerate(queries):
            qu[R].append(i)
        
        ans = [None]*Q
        stack = [] # stack maintains a strictly increasing sequence
        for i in range(self.N):
            while stack and self.arr[stack[-1]] >= self.arr[i]:
                self.dsu[stack.pop()] = i # x -> i where arr[x] >= arr[i] and x < i
            stack.append(i) # all elements in stack < arr[i]
            for j in qu[i]:
                idx = self.root(queries[j][0]) # root of L
                ans[j] = [idx, self.arr[idx]] # [index, val]
        
        return ans
        
    def root(self, k):
        if self.dsu[k] == k:
            return k
        self.dsu[k] = self.root(self.dsu[k])
        return self.dsu[k]

if __name__ == "__main__":
    arpa = Arpa([3928,   53, 3093, 4657, 2209, 1823, 3613, 1018,  129,   32,  # 10
        3585,  903, 1538, 2462, 2092, 2093, 2230, 3209, 2800, 1689,  # 20
        4938, 3443,  386, 2725, 3363, 2351, 2696, 1641, 3931, 1073,  # 30
        3121, 2160, 1132, 2829, 2447, 2411,  381, 3528, 3309, 1496,  # 40
        4439, 4848, 4050, 2572,  158, 1076, 4222,  662, 3294, 4084,  # 50
        4312, 2752, 4420,  210, 4073, 1403,  800,  766, 2433, 1255,  # 60
        4260, 1391,  215, 1826,  488, 4379, 2582, 4896, 1245, 1328,  # 70
        1093, 2146, 1081,   48, 4918, 1037, 2653, 2201, 2080,  656,  # 80
        1124, 2575, 2037,  183, 2912, 2952, 2409, 1323, 1764, 2647,  # 90
        2035, 1950, 4997,  844, 2437, 2825, 4001, 3263, 3897, 2227])  # 100
    
    ans = arpa.run([[61, 78], [53, 74], [14, 26], [15, 96], [63, 80],
            [ 3, 62], [ 1, 49], [ 2, 57], [ 9, 33], [16, 83],
            [69, 80], [62, 84], [25, 58], [29, 75], [28, 55],
            [12, 53], [52, 97], [11, 96], [66, 98], [ 9, 27],
            [39, 86], [23, 88], [22, 96], [66, 68], [56, 83],
            [ 3,  7], [31, 44], [ 9, 88], [ 5, 60], [18, 71]])
    
    assert ans == [[73,  48], [73,  48], [22, 386], [73,  48], [73,  48],
                    [ 9,  32], [ 9,  32], [ 9,  32], [ 9,  32], [73,  48],
                    [73,  48], [73,  48], [44, 158], [73,  48], [44, 158],
                    [44, 158], [73,  48], [73,  48], [73,  48], [ 9,  32],
                    [73,  48], [73,  48], [73,  48], [68,1245], [73,  48],
                    [ 7,1018], [44, 158], [ 9,  32], [ 9,  32], [44, 158]]