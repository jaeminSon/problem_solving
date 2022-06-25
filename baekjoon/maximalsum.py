import sys

N = int(sys.stdin.readline().rstrip())
l = [int(d) for d in sys.stdin.readline().rstrip().split()]
T = int(sys.stdin.readline().rstrip())

K = 2**17
tree = [0]*(2*K)
for i in range(min(K, len(l))):
    tree[K+i] = sum(l[i::i+1])
for i in range(K - 1, 0, -1):
    tree[i] = max(tree[2*i], tree[2*i+1])

def update(p, s):

    for d in range(1, p+1):
        if p % d == 0:
            i = K + d - 1
            tree[i] += s
    
            while i > 1:
                if i % 2 == 0: # left child
                    tree[i//2] = max(tree[i], tree[i+1])
                else: # right child
                    tree[i//2] = max(tree[i-1], tree[i])
                i//=2

    return ans


ans = 0
for _ in range(T):
    p,s  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    update(p,s)
    ans += tree[1]
    update(p,-s)

print(ans)