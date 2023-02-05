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
        self.tree = [0] * 2 * self.just_bigger_power_2(N)
        self.lazy = [0] * 2 * self.just_bigger_power_2(N)
        self.len = N
        self.initialize(arr, 0, N-1, 0)
        
    def just_bigger_power_2(self, val):
        i=0
        while 2**i < val:
            i+=1
        return 2**i

    def initialize(self, arr, s, e, index) : 
        # arr = [1, 2, 3, 4, 5]
        # tree = [15, 6, 9, 3, 3, 4, 5, 1, 2, 0]
        if s <= e:
            if s == e: # leaf node
                self.tree[index] = arr[s]
            else:
                mid = (s + e) // 2 
                self.initialize(arr, s, mid, index * 2 + 1) 
                self.initialize(arr, mid + 1, e, index * 2 + 2) 
                self.tree[index] = self.tree[index * 2 + 1] + self.tree[index * 2 + 2] 
            
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

class SummationQuerySegmentTree:
    def __init__(self, arr):
        N = len(arr)
        self.tree = [0] * 2 * self.just_bigger_power_2(N)
        self.len = N
        self.initialize(arr, 0, N-1, 0)
        
    def just_bigger_power_2(self, val):
        i=0
        while 2**i < val:
            i+=1
        return 2**i
    
    def initialize(self, arr, s, e, index) : 
        # arr = [1, 2, 3, 4, 5]
        # tree = [15, 6, 9, 3, 3, 4, 5, 1, 2, 0]
        if s <= e:
            if s == e: # leaf node
                self.tree[index] = (arr[s], arr[s], arr[s], arr[s]) # best left, best right, total, best
            else:
                mid = (s + e) // 2; 
                self.initialize(arr, s, mid, index * 2 + 1); 
                self.initialize(arr, mid + 1, e, index * 2 + 2); 
                l_best_left, l_best_right, l_total, l_best = self.tree[index * 2 + 1]
                r_best_left, r_best_right, r_total, r_best = self.tree[index * 2 + 2]
                best_left = max(l_best_left,  l_total + r_best_left)
                best_right = max(r_best_right, r_total + l_best_right)
                total = l_total + r_total
                best = max([l_best, r_best, l_best_right+r_best_left, best_left, best_right])
                self.tree[index] = (best_left, best_right, total, best)
            
    def query_util(self, node_index, node_s, node_e, s, e): 

        if node_s <= node_e and node_s <= e and node_e >= s:        
            if node_s >= s and node_e <= e: # [node_s, node_e] in [s,e]
                return self.tree[node_index]
            else: # non-overlapping node
                mid = (node_s + node_e) // 2 
                l_best_left, l_best_right, l_total, l_best = self.query_util(2 * node_index + 1, node_s, mid, s, e)
                r_best_left, r_best_right, r_total, r_best = self.query_util(2 * node_index + 2, mid + 1, node_e, s, e)
                best_left = max(l_best_left,  l_total + r_best_left)
                best_right = max(r_best_right, r_total + l_best_right)
                total = l_total + r_total
                best = max([l_best, r_best, l_best_right+r_best_left, best_left, best_right])
                return (best_left, best_right, total, best)
        else:
            import math
            return (-math.inf, -math.inf, 0, -math.inf)
        
    def query(self, s, e):
        # [s,e]
        return self.query_util(0, 0, self.len-1, s, e)

class Node:
    def __init__(self, s, l, r, b):  # sum, left-sum, right-sum, best
        self.s = s
        self.l = l
        self.r = r
        self.b = b

class BestPrefixSumSegmentTree:

    def __init__(self, bias):
        # bias should be power of 2 and greater than max number of elements
        self.bias = bias
        self.n_trees = 2*bias
        self.tree = [Node(0, 0, 0, 0) for _ in range(self.n_trees)]  # 0th tree empty

    def clear(self):
        for i in range(self.n_trees):
            self.replace(i, 0)

    def merge(self, a, b):
        # t <- a + b
        s = a.s + b.s
        return Node(s, max(a.l, a.s + b.l), max(b.r, a.r + b.s), max(a.r + b.l, a.b, b.b, s))

    def increment(self, i, v):
        self.tree[i].s += v
        self.tree[i].l += v
        self.tree[i].r += v
        self.tree[i].b += v

    def replace(self, i, v):
        self.tree[i].s = v
        self.tree[i].l = v
        self.tree[i].r = v
        self.tree[i].b = v

    def update(self, i, v):
        i += self.bias
        self.increment(i, v)
        # self.replace(x, v)
        while i > 1:
            if i % 2 == 0:  # left child
                self.tree[i//2] = self.merge(self.tree[i], self.tree[i+1])
            else:  # right child
                self.tree[i//2] = self.merge(self.tree[i-1], self.tree[i])
            i //= 2

    def query(self, l, r):
        # [l, r]
        l += self.bias
        r += self.bias
        ret = Node(0, 0, 0, 0)
        while l <= r:
            if l % 2 == 1:
                ret = self.merge(self.tree[l], ret)
                l += 1
            if r % 2 == 1:
                ret = self.merge(ret, self.tree[r])
                r -= 1
            l //= 2
            r //= 2
        return ret

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