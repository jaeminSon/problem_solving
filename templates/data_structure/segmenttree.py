class SegmentTree:
    def __init__(self, arr):
        N = len(arr) # N should be power of 2
        self.tree = [0] * 2 * N
        self.len = N
        # arr = [1, 2, 3, 4]
        # tree = [0, 1+2+3+4, 1+2, 3+4, 1, 2, 3, 4]
        for i in range(N):
            self.tree[N+i] = arr[i]
        for i in range(N - 1, 0, -1):
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]
            # self.tree[i] = max(self.tree[2*i], self.tree[2*i+1]) # max query
        
    def query(self, l, r):
        # [l, r)
        N = self.len
        res = 0
        
        l += N
        r += N
        while l < r: # stop if l==r
            if l % 2 ==1:# l is right child (include only l, not parent, move to parent of next node)
                res += self.tree[l] 
                # res = max(res, self.tree[l]) # max query
                l += 1
            if r % 2 == 1: # r is right child (include r-1, move to parent)
                r -= 1
                res += self.tree[r] 
                # res = max(res, self.tree[r]) # max query
            l //= 2
            r //= 2
        return res        
    
    def updateTreeNode(self, p, value):
        N = self.len
        i = p + N
        
        self.tree[i] = value
        while i > 1:
            if i % 2 == 0: # left child
                self.tree[i//2] = self.tree[i] + self.tree[i+1]
                # self.tree[i//2] = max(self.tree[i], self.tree[i+1]) # max query
            else: # right child
                self.tree[i//2] = self.tree[i-1] + self.tree[i]
                # self.tree[i//2] = max(self.tree[i-1], self.tree[i]) # max query
            i//=2
    
class SegmentTreeLazyPropagation:
    # summation query
    def __init__(self, arr):
        N = len(arr)
        self.tree = [0] * 4 * N
        self.lazy = [0] * 4 * N
        self.len = N
        self.initialize(arr, 0, N-1, 0)
        
    def initialize(self, arr, s, e, index) : 
        # arr = [1, 2, 3, 4, 5]
        # tree = [15, 6, 9, 3, 3, 4, 5, 1, 2, 0]
        if s <= e:
            if s == e: # leaf node
                self.tree[index] = arr[s]
            else:
                mid = (s + e) // 2; 
                self.initialize(arr, s, mid, index * 2 + 1); 
                self.initialize(arr, mid + 1, e, index * 2 + 2); 
                self.tree[index] = self.tree[index * 2 + 1] + self.tree[index * 2 + 2]; 
            
    def update(self, s, e, diff):
        self.update_util(0, 0, self.len - 1, s, e, diff)
    
    def propagate(self, node_index, node_s, node_e):
        if self.lazy[node_index] != 0: # reflect lazy updates
            self.tree[node_index] += (node_e - node_s + 1) * self.lazy[node_index] 
            if node_s != node_e: # intermediate node
                self.lazy[node_index * 2 + 1] += self.lazy[node_index] 
                self.lazy[node_index * 2 + 2] += self.lazy[node_index] 
            self.lazy[node_index] = 0 
        
    
    def update_util(self, node_index, node_s, node_e, s, e, diff): 
        self.propagate(node_index, node_s, node_e)
        
        if node_s <= node_e and node_s <= e and node_e >= s:
            if node_s >= s and node_e <= e: # [node_s, node_e] in [s,e]
                self.tree[node_index] += (node_e - node_s + 1) * diff 
                if node_s != node_e: # intermediate node
                    self.lazy[node_index * 2 + 1] += diff 
                    self.lazy[node_index * 2 + 2] += diff 
            else: # non-overlapping node
                mid = (node_s + node_e) // 2 
                self.update_util(node_index * 2 + 1, node_s, mid, s, e, diff) 
                self.update_util(node_index * 2 + 2, mid + 1, node_e, s, e, diff) 
                self.tree[node_index] = self.tree[node_index * 2 + 1] + self.tree[node_index * 2 + 2] 
            
    def query_util(self, node_index, node_s, node_e, s, e): 
        self.propagate(node_index, node_s, node_e)

        if node_s <= node_e and node_s <= e and node_e >= s:        
            if node_s >= s and node_e <= e: # [node_s, node_e] in [s,e]
                return self.tree[node_index] 
            else: # non-overlapping node
                mid = (node_s + node_e) // 2 
                return self.query_util(2 * node_index + 1, node_s, mid, s, e) + self.query_util(2 * node_index + 2, mid + 1, node_e, s, e)
        else:
            return 0 # null value for summation query
        
    def query(self, s, e):
        # [s,e]
        return self.query_util(0, 0, self.len-1, s, e)

            
if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    segtree = SegmentTree(a)
    assert segtree.query(1,3) == 5 # a[1]+a[2]=2+3
    segtree.updateTreeNode(2, 1)
    assert segtree.query(1,3) == 3 # a[1]+a[2]=2+1
    
    segtree_lazy = SegmentTreeLazyPropagation(a)
    assert segtree_lazy.query(1,2) == 5 # a[1]+a[2]=2+3
    segtree_lazy.update(2, 4, 1)
    assert segtree_lazy.query(1,4) == 17 # a[1]+a[2]+a[3]+a[4]=2+4+5+6