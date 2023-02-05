import sys

MINUS_INF = -1001

N = int(sys.stdin.readline().rstrip())
l = [int(d) for d in sys.stdin.readline().rstrip().split()]
Q = int(sys.stdin.readline().rstrip())
q = [[int(d) for d in sys.stdin.readline().rstrip().split()] for _ in range(Q)]

class SegmentTree:
    # summation query
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
            return (MINUS_INF, MINUS_INF, 0, MINUS_INF)
        
    def query(self, s, e):
        # [s,e]
        return self.query_util(0, 0, self.len-1, s, e)

st = SegmentTree(l)
for s, e in q:
    print(st.query(s-1, e-1)[-1])
