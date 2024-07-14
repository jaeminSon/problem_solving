N_MAX = 300_010
tree = [0] * (N_MAX+1)

def update(i, delta):
    i += 1
    while i <= N_MAX:
        tree[i] += delta
        i += i & (-i)  # right node (same depth) for update


def query(i):
    res = 0
    i = i+1
    while i > 0:
        res += tree[i]
        i -= i & (-i)
    return res


def update_values(l, r, a):
    if l <= r:
        update(l, a)
        update(r+1, -a)
    else:
        update(0, a)
        update(r+1, -a)
        update(l, a)


N, M = map(int, input().split())
O = list(map(int, input().split()))
nation2planets = {i: [] for i in range(N)}
for i, v in enumerate(O):
    nation2planets[v-1].append(i)
P = list(map(int, input().split()))
Q = int(input())
questions = [list(map(int, input().split())) for _ in range(Q)]
questions = [(l-1, r-1, a) for l, r, a in questions]

l = [1] * N
r = [Q] * N
ans = [None] * N

while True:
    # group queries by mid point
    mid2query = {i: [] for i in range(1, Q+1)}
    finished = True
    for i in range(N):
        if l[i] <= r[i]:  # binary search of [l,r]
            finished = False
            mid2query[(l[i] + r[i]) // 2].append(i)
    if finished:
        break

    # run algorithm and handle each query
    tree = [0] * (N_MAX+1)
    for op_count in range(1, Q+1):
        update_values(*questions[op_count-1])
        for i_nation in mid2query[op_count]:
            if sum(query(i) for i in nation2planets[i_nation]) >= P[i_nation]:
                ans[i_nation] = op_count
                r[i_nation] = op_count - 1  # binary search of [l,r]
            else:
                l[i_nation] = op_count + 1


for s in ans:
    print("NIE" if s is None else s)
