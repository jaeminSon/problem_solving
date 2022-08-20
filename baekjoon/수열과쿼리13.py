import sys

MOD = 10**9+7

N = int(sys.stdin.readline().rstrip())

l = [int(d) for d in sys.stdin.readline().rstrip().split()]

Q = int(sys.stdin.readline().rstrip())
l_q = [[int(d) for d in sys.stdin.readline().rstrip().split()] for _ in range(Q)]

class SegmentTreeLazyPropagation:
    # summation query
    def __init__(self, arr):
        N = len(arr)
        self.tree = [0] * 4 * N
        self.lazy_mul = [1] * 4 * N
        self.lazy_add = [0] * 4 * N
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
                self.tree[index] = (self.tree[index * 2 + 1] + self.tree[index * 2 + 2]) % MOD 
    
    def propagate(self, node_index, node_s, node_e):
        if not (self.lazy_mul[node_index] == 1 and self.lazy_add[node_index] == 0):
            self.tree[node_index] = (self.tree[node_index] * self.lazy_mul[node_index] + (node_e-node_s+1)*self.lazy_add[node_index]) % MOD
            if node_s != node_e: # intermediate node
                self.lazy_mul[node_index * 2 + 1] = (self.lazy_mul[node_index * 2 + 1]*self.lazy_mul[node_index]) % MOD
                self.lazy_mul[node_index * 2 + 2] = (self.lazy_mul[node_index * 2 + 2]*self.lazy_mul[node_index]) % MOD
                self.lazy_add[node_index * 2 + 1] = (self.lazy_add[node_index * 2 + 1]*self.lazy_mul[node_index] + self.lazy_add[node_index]) % MOD
                self.lazy_add[node_index * 2 + 2] = (self.lazy_add[node_index * 2 + 2]*self.lazy_mul[node_index] + self.lazy_add[node_index]) % MOD
            self.lazy_mul[node_index] = 1
            self.lazy_add[node_index] = 0 
    
    def update(self, op, s, e, val):
        self.update_util(0, 0, self.len - 1, s, e, op, val)
    
    def update_util(self, node_index, node_s, node_e, s, e, op, val): 
        self.propagate(node_index, node_s, node_e)
        
        if node_s <= node_e and node_s <= e and node_e >= s:
            if node_s >= s and node_e <= e: # [node_s, node_e] in [s,e]
                if op==1:
                    self.lazy_mul[node_index] = 1
                    self.lazy_add[node_index] = val
                elif op==2:
                    self.lazy_mul[node_index] = val
                    self.lazy_add[node_index] = 0
                else:
                    self.lazy_mul[node_index] = 0
                    self.lazy_add[node_index] = val
                self.propagate(node_index, node_s, node_e)
            else: # non-overlapping node
                mid = (node_s + node_e) // 2 
                self.update_util(node_index * 2 + 1, node_s, mid, s, e, op, val) 
                self.update_util(node_index * 2 + 2, mid + 1, node_e, s, e, op, val) 
                self.tree[node_index] = self.tree[node_index * 2 + 1] + self.tree[node_index * 2 + 2] 
            
    def query_util(self, node_index, node_s, node_e, s, e): 
        self.propagate(node_index, node_s, node_e)

        if node_s <= node_e and node_s <= e and node_e >= s:        
            if node_s >= s and node_e <= e: # [node_s, node_e] in [s,e]
                return self.tree[node_index] 
            else: # non-overlapping node
                mid = (node_s + node_e) // 2 
                return (self.query_util(2 * node_index + 1, node_s, mid, s, e) + self.query_util(2 * node_index + 2, mid + 1, node_e, s, e)) % MOD
        else:
            return 0 # null value for summation query
        
    def query(self, s, e):
        # [s,e]
        return self.query_util(0, 0, self.len-1, s, e)

segtree = SegmentTreeLazyPropagation(l)
for q in l_q:
    if q[0]==4:
        print(segtree.query(q[1]-1,q[2]-1))
    else:
        segtree.update(q[0],q[1]-1,q[2]-1,q[3])
