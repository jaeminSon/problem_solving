from heapq import merge

class MergSortTree:
    def __init__(self, arr):
        N = self.just_bigger_power_2(len(arr)) # N should be power of 2
        self.tree = [[] for _ in range(2*N)]
        self.len = N
        # arr = [1, 2, 3, 4]
        # tree = [0, [1, 2, 3, 4], [1,2], [3,4], [1], [2], [3], [4]]
        for i in range(len(arr)):
            self.tree[N+i] = [arr[i]]
        for i in range(N - 1, 0, -1):
            self.tree[i] = list(merge(self.tree[2*i], self.tree[2*i+1]))
        
    def just_bigger_power_2(self, val):
        i=0
        while 2**i < val:
            i+=1
        return 2**i

    def query(self, l, r):
        """
        Range query [l, r) with O(log N) time complexity.
        """
        
        N = self.len
        res = []
        
        l += N
        r += N
        while l < r: # stop if l==r
            if l % 2 ==1:# l is right child (include only l, not parent, move to parent of next node)
                res += self.tree[l] 
                l += 1
            if r % 2 == 1: # r is right child (include r-1, move to parent)
                r -= 1
                res += self.tree[r] 
            l //= 2
            r //= 2
        return res        
    

if __name__ == "__main__":
    a = [1, 2, 3, 4, 5, 6, 7]
    mergetree = MergSortTree(a)
    assert set(mergetree.query(1,3)) == set([2, 3]) # [a[1], a[2]] == [2, 3]
    assert set(mergetree.query(1,7)) == set([2, 3, 4, 5, 6, 7]) # [a[1], a[2]] == [2, 3]
    