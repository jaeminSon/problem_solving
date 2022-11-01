import sys

MINUS_INF = -100_001

N = int(sys.stdin.readline().rstrip())
l = [int(d) for d in sys.stdin.readline().rstrip().split()]
Q = int(sys.stdin.readline().rstrip())
q = [[int(d)-1 for d in sys.stdin.readline().rstrip().split()] for _ in range(Q)]

class SegmentTree:
    # summation query
    def __init__(self, arr):
        N = len(arr)
        self.tree = [0] * 4 * N
        self.lazy = [0] * 4 * N
        self.len = N
        self.initialize(arr, 0, N-1, 0)
        
    def initialize(self, arr, s, e, index) : 
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
                llsum, lrsum, lsum, lbest = self.query_util(2 * node_index + 1, node_s, mid, s, e)
                rlsum, rrsum, rsum, rbest = self.query_util(2 * node_index + 2, mid + 1, node_e, s, e)
                best_left = max(llsum,  lsum + rlsum)
                best_right = max(rrsum, rsum + lrsum)
                total = lsum + rsum
                best = max([lbest, rbest, lrsum+rlsum, best_left, best_right])
                return (best_left, best_right, total, best)
        else:
            return MINUS_INF, MINUS_INF, 0, MINUS_INF
        
    def query(self, s, e):
        # [s,e]
        if s <= e:
            return self.query_util(0, 0, self.len-1, s, e)
        else:
            return 0, 0, 0, 0

st = SegmentTree(l)
for x1, y1, x2, y2 in q:
    if y1 >= x2: # overlap
        lbest_left, lbest_right, ltotal, lbest = st.query(x1,x2-1)
        mbest_left, mbest_right, mtotal, mbest = st.query(x2,y1)
        rbest_left, rbest_right, rtotal, rbest = st.query(y1+1,y2)
        ans = max(lbest_right+mbest_left, lbest_right+mtotal+rbest_left, mbest, mbest_right+rbest_left)
        print(ans)
    else: # best_left, best_right, total, best
        print(st.query(x1, y1)[1]+st.query(y1+1, x2-1)[2]+st.query(x2, y2)[0])