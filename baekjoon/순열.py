import sys

N = int(sys.stdin.readline().rstrip())

A = [int(sys.stdin.readline().rstrip()) for _ in range(N)]

K = 2**17
tree = [0]*(2*K)
for i in range(K):
    tree[K+i] = 1
for i in range(K - 1, 0, -1):
    tree[i] = tree[2*i] + tree[2*i+1]

def pos(a):

    def _recursive_search(root, target):
        if root >= K:
            return root - K
        elif tree[2*root] > target: # left child
            return _recursive_search(2*root, target)
        else: # right child
            return _recursive_search(2*root+1, target-tree[2*root])

    ans = _recursive_search(1, a)

    # update
    i = K + ans
    tree[i] = 0
    while i > 1:
        if i % 2 == 0: # left child
            tree[i//2] = tree[i] + tree[i+1]
        else: # right child
            tree[i//2] = tree[i-1] + tree[i]
        i//=2

    return ans

res = [0] * N
for i, a in enumerate(A):
    res[pos(a)] = i+1
for r in res:
    print(r)