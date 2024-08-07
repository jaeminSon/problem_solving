class FenwickTree:
    def __init__(self, arr):
        N = len(arr)
        self.len = N
    
        self.tree = [0]*(N+1) # tree[0] is dummy
        for i in range(N):
            self.update(i, arr[i])
    
    def update(self, i ,delta):
        i+=1
        while i <= self.len:
            self.tree[i] += delta 
            # self.tree[i] = max(delta, self.tree[i]) # max query
            i += i & (-i) # right node (same depth) for update 

    def query(self, i):
        res = 0
        i = i+1
        while i > 0:
            res += self.tree[i]
            # res = max(res, self.tree[i])
            i -= i & (-i)
        return res
 

if __name__ == "__main__":
    # point update & range query
    freq = [2, 1, 1, 3, 2, 3, 4, 5, 6, 7, 8, 9]
    fwtree = FenwickTree(freq)
    assert fwtree.query(5)==12
    freq[3] += 6
    fwtree.update(3, 6)
    assert fwtree.query(5) - fwtree.query(2) == 14

    # range update (init array should be 0) & point query
    freq = [0] * 10
    fwtree = FenwickTree(freq)
    freq[3] += 2
    freq[4] += 2
    freq[5] += 2
    fwtree.update(3, 2)
    fwtree.update(6, -2)
    assert fwtree.query(5) == 2
