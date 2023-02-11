import sys
from collections import defaultdict


def query(tree, l, r):
    # [l, r)
    N = len(tree) // 2
    res = -float("inf")

    l += N
    r += N
    while l < r:  # stop if l==r
        # l is right child (include only l, not parent, move to parent of next node)
        if l % 2 == 1:
            res = max(res, tree[l])  # max query
            l += 1
        if r % 2 == 1:  # r is right child (include r-1, move to parent)
            r -= 1
            res = max(res, tree[r])  # max query
        l //= 2
        r //= 2
    return res


def update(tree, p, value):
    N = len(tree) // 2
    i = p + N

    tree[i] = value
    while i > 1:
        if i % 2 == 0:  # left child
            tree[i//2] = max(tree[i], tree[i+1])  # max query
        else:  # right child
            tree[i//2] = max(tree[i-1], tree[i])  # max query
        i //= 2


def update_trees(p, v):
    global d, u
    update(downtree, p, v+d*p)
    update(uptree, p, v-u*p)


def get_best(p):
    global d, u
    return max(query(downtree, 0, p+1) - d*p, query(uptree, p, len(uptree)//2) + u*p)


def shop(list_lm):
    list_lm.sort(key=lambda x: x[0])
    down = []
    up = []
    for (l, _) in list_lm:
        best = get_best(l)
        down.append(best)
        up.append(best)

    for i in range(len(list_lm)):
        if i > 0:
            down[i] = max(down[i], down[i-1]
                          - (list_lm[i][0]-list_lm[i-1][0])*d)
        down[i] += list_lm[i][1]

    for i in range(len(list_lm)-1, -1, -1):
        if i < len(list_lm) - 1:
            up[i] = max(up[i], up[i+1] - (list_lm[i+1][0]-list_lm[i][0])*u)
        up[i] += list_lm[i][1]

    for i, (l, m) in enumerate(list_lm):
        update_trees(l, max(up[i], down[i]))



n, u, d, s = [int(d) for d in sys.stdin.readline().rstrip().split()]

t2lm = defaultdict(list)
for _ in range(n):
    t, l, m = [int(d) for d in sys.stdin.readline().rstrip().split()]
    t2lm[t].append((l, m))

treesize = 2**20
downtree = [-float("inf")] * treesize
uptree = [-float("inf")] * treesize

update_trees(s, 0)

t_sorted = sorted(t2lm.keys())
for t in t_sorted:
    shop(t2lm[t])

print(get_best(s))
