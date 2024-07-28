from bisect import bisect_left
from heapq import merge


def just_bigger_power_2(val):
    i = 0
    while 2**i < val:
        i += 1
    return 2**i


def query(l, r, k):
    """
    Range query [l, r) with O(log N) time complexity.
    """

    res = 0

    l += N
    r += N
    while l < r:  # stop if l==r
        # l is right child (include only l, not parent, move to parent of next node)
        if l % 2 == 1:
            res += bisect_left(tree[l], k)
            l += 1
        if r % 2 == 1:  # r is right child (include r-1, move to parent)
            r -= 1
            res += bisect_left(tree[r], k)
        l //= 2
        r //= 2
    return res


def shrink_coord_1d(l, offset=0):
    l_unique_sorted = sorted(list(set(l)))
    mapping = {v: i+offset for i, v in enumerate(l_unique_sorted)}
    return [mapping[el] for el in l]


N = int(input())
arr = list(map(int, input().split()))
arr = shrink_coord_1d(arr)
Q = int(input())
questions = [list(map(int, input().split())) for _ in range(Q)]

prev = []
v2i = {}
for i, v in enumerate(arr):
    if v in v2i:
        prev.append(v2i[v])
    else:
        prev.append(-1)
    v2i[v] = i
        
N = just_bigger_power_2(len(prev))
tree = [[] for _ in range(2*N)]
for i in range(len(prev)):
    tree[N+i] = [prev[i]]
for i in range(N - 1, 0, -1):
    tree[i] = list(merge(tree[2*i], tree[2*i+1]))

answers = [0]
for i in range(Q):
    x, r = questions[i]
    l = answers[i] + x
    answers.append(query(l-1, r, l-1))

for i in range(1, len(answers)):
    print(answers[i])
