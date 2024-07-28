import bisect
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
            res += len(tree[l]) - bisect.bisect_right(tree[l], k)
            l += 1
        if r % 2 == 1:  # r is right child (include r-1, move to parent)
            r -= 1
            res += len(tree[r]) - bisect.bisect_right(tree[r], k)
        l //= 2
        r //= 2
    return res


N = int(input())
arr = list(map(int, input().split()))
Q = int(input())
questions = [list(map(int, input().split())) for _ in range(Q)]

N = just_bigger_power_2(len(arr))
tree = [[] for _ in range(2*N)]
for i in range(len(arr)):
    tree[N+i] = [arr[i]]
for i in range(N - 1, 0, -1):
    tree[i] = list(merge(tree[2*i], tree[2*i+1]))

answers = [0]
for t, (a, b, c) in enumerate(questions):
    i = answers[t] ^ a
    j = answers[t] ^ b
    k = answers[t] ^ c
    answers.append(query(i-1, j, k))

for i in range(1, len(answers)):
    print(answers[i])
