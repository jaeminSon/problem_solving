import sys

N, M, K = [int(d) for d in sys.stdin.readline().rstrip().split()]

l = [int(sys.stdin.readline().rstrip()) for _ in range(N)]
l_q = [[int(d) for d in sys.stdin.readline().rstrip().split()] for _ in range(M+K)]


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

s = SegmentTreeLazyPropagation(l)

for q in l_q:
    if q[0]==1:
        s.update(q[1]-1, q[2]-1, q[3])
    else:
        print(s.query(q[1]-1, q[2]-1))