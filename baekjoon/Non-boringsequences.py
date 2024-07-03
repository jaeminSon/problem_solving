import sys

sys.setrecursionlimit(500_000)


def is_not_boring(l, r):
    if l > r:
        return True

    i = l
    j = r
    while i <= j:
        if prev_appear[i] < l and next_appear[i] > r:
            return is_not_boring(l, i-1) and is_not_boring(i+1, r)
        if prev_appear[j] < l and next_appear[j] > r:
            return is_not_boring(l, j-1) and is_not_boring(j+1, r)
        i += 1
        j -= 1

    return False


T = int(sys.stdin.readline().rstrip())

for _ in range(T):
    n = int(sys.stdin.readline().rstrip())
    v = [int(d) for d in sys.stdin.readline().rstrip().split()]
    value2index = {x: -1 for x in v}

    prev_appear = [-1] * n
    next_appear = [n+1] * n
    for i, x in enumerate(v):
        if value2index[x] != -1:
            prev_appear[i] = value2index[x]
            next_appear[value2index[x]] = i
        value2index[x] = i

    del v
    del value2index

    if is_not_boring(0, n-1):
        print("non-boring")
    else:
        print("boring")
