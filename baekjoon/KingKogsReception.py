
def just_bigger_power_2(val):
    i = 0
    while 2**i < val:
        i += 1
    return 2**i


N = 1_001_000
ans = [0]
tree = [[0, 0] for _ in range(2 * just_bigger_power_2(N))]


def merge(left, right):
    end = max(right[1], left[1] + right[0])
    return [left[0] + right[0], end]


def initialize(s, e, index):
    if s <= e:
        if s == e:  # leaf node
            tree[index][1] = s
        else:
            mid = (s + e) // 2
            initialize(s, mid, index * 2 + 1)
            initialize(mid + 1, e, index * 2 + 2)
            tree[index] = merge(tree[index * 2 + 1], tree[index * 2 + 2])


initialize(0, N-1, 0)


def update_util(node_index, node_s, node_e, p, diff):

    if node_s <= p <= node_e:
        if node_s == node_e:
            tree[node_index][0] += diff
            tree[node_index][1] += diff
        else:
            mid = (node_s + node_e) // 2
            if p <= mid:
                update_util(node_index * 2 + 1, node_s, mid, p, diff)
            else:
                update_util(node_index * 2 + 2, mid + 1, node_e, p, diff)
            tree[node_index] = merge(
                tree[node_index * 2 + 1], tree[node_index * 2 + 2])


def update(p, diff):
    update_util(0, 0, N - 1, p, diff)


def query_util(node_index, node_s, node_e, p):

    if node_s <= node_e:
        if node_e <= p:
            ans[0] = max(ans[0]+tree[node_index][0], tree[node_index][1])
        else:
            mid = (node_s + node_e) // 2
            query_util(2 * node_index + 1, node_s, mid, p)
            if mid < p:
                query_util(2 * node_index + 2, mid + 1, node_e, p)


def query(p):
    return query_util(0, 0, N-1, p)


Q = int(input())
queries = [input().split() for _ in range(Q)]

dict_query = {}
for i, q in enumerate(queries):

    if q[0] == "+":
        t, d = int(q[1]), int(q[2])
        t -= 1
        update(t, d)
        dict_query[i+1] = (t, d)
    elif q[0] == "-":
        k = int(q[1])
        update(dict_query[k][0], -dict_query[k][1])
    elif q[0] == "?":
        t = int(q[1])
        t -= 1
        ans[0] = 0
        query(t)
        print(ans[0]-t)
