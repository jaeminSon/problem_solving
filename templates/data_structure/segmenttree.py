class SegmentTree:
    def __init__(self, arr):
        N = len(arr)
        self.tree = [0] * 2 * N
        self.len = N
        # arr = [1, 2, 3, 4, 5]
        # tree = [0, 4+5+1+2+3, 4+5+1, 2+3, 4+5, 1, 2, 3, 4, 5]
        for i in range(N):
            self.tree[N+i] = arr[i]
        for i in range(N - 1, 0, -1) :
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]
            # self.tree[i] = max(self.tree[2*i], self.tree[2*i+1]) # max query
        
    def query(self, l, r):
        # [l, r)
        N = self.len
        res = 0
        
        l += N
        r += N
        while l < r: # stop if l==r
            if l % 2 ==1 : # l is right child (include only l, not parent, move to parent of next node)
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
    
 
if __name__ == "__main__" :
    a = [1, 2, 3, 4, 5]
    segtree = SegmentTree(a)
    print(segtree.query(1,3))
    
    segtree.updateTreeNode(2, 1)
    print(segtree.query(1,3))