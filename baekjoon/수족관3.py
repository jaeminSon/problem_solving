import sys
from heapq import heappush, heappop

sys.setrecursionlimit(100_000)
MAX = 1e+19

def init():
    for i in range(N):
        tree[N+i] = (ys[i], i)
    for i in range(N - 1, 0, -1):
        tree[i] = min(tree[2*i], tree[2*i+1])
    
def query(l, r):
    # [l, r)
    res = (MAX, MAX)
    
    l += N
    r += N
    while l < r: # stop if l==r
        if l % 2 ==1:# l is right child (include only l, not parent, move to parent of next node)
            res = min(res, tree[l]) # max query
            l += 1
        if r % 2 == 1: # r is right child (include r-1, move to parent)
            r -= 1
            res = min(res, tree[r]) # max query
        l //= 2
        r //= 2
    return res        


def best(s, e, h):
    if s >= e:
        return 0
    
    h_lowest, index = query(s, e)
    left = best(s, index, h_lowest)
    right = best(index+1, e, h_lowest)

    max_val = max(left, right) + (xs[e] - xs[s]) * (h_lowest-h)
    heappush(heap, -min(left, right))
    return max_val


N = int(input())
xs = []
ys = []
for _ in range(N//2):
    input()
    x, y = map(int, input().split())
    xs.append(x)
    ys.append(y)    

K = int(input())

N = len(ys)
tree = [0] * 2 * N
init()

heap = []
val = best(0, N-1, 0)
heappush(heap, -val)

ans = 0
for _ in range(K):
    if len(heap) > 0:
        val = heappop(heap)
        ans -= val
print(ans)

