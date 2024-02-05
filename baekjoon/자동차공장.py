from sys import stdin
input = stdin.readline

def just_bigger_power_2(val):
    i = 0
    while 2**i < val:
        i += 1
    return 2**i

count = 0
def eulerian_technique(node):
    global count
    stack=[node]
    while stack:
        now=stack[-1]
        if start[now]==0:
            count+=1
            start[now]=count
        check=False
        for nxt in adj[now]:
            if start[nxt]==0:
                stack.append(nxt)
                check=True
                break
        if check==False:
            end[now]=count
            stack.pop()


N, M = map(int, input().split())

list_pay = [int(input())]

adj = [[] for _ in range(N)]
for i in range(N-1):
    w, p = map(int, input().split())
    adj[p-1].append(i+1)
    list_pay.append(w)

queries = []
for _ in range(M):
    queries.append(input().split())

start = [0] * N
end = [0] * N
eulerian_technique(0)
start = [s-1 for s in start]
end = [e-1 for e in end]

tree = [0] * 2 * just_bigger_power_2(N)
lazy = [0] * 2 * just_bigger_power_2(N)


def merge(left, right):
    return left + right


def initialize(arr, s, e, index):
    if s <= e:
        if s == e:  # leaf node
            tree[index] = arr[s]
        else:
            mid = (s + e) // 2
            initialize(arr, s, mid, index * 2 + 1)
            initialize(arr, mid + 1, e, index * 2 + 2)

inv_start = {v:i for i, v in enumerate(start)}
initialize([list_pay[inv_start[i]] for i in range(N)], 0, N-1, 0)


def update(s, e, diff):
    update_util(0, 0, N - 1, s, e, diff)


def propagate(node_index, node_s, node_e):
    if lazy[node_index] != 0:  # reflect lazy updates
        if node_s != node_e:  # intermediate node
            lazy[node_index * 2 + 1] += lazy[node_index]
            lazy[node_index * 2 + 2] += lazy[node_index]
        else:
            tree[node_index] += lazy[node_index]
        lazy[node_index] = 0


def update_util(node_index, node_s, node_e, s, e, diff):
    propagate(node_index, node_s, node_e)

    if node_s <= node_e and node_s <= e and node_e >= s:
        if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
            if node_s != node_e:  # intermediate node
                lazy[node_index * 2 + 1] += diff
                lazy[node_index * 2 + 2] += diff
            else:
                tree[node_index] += diff
        else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
            mid = (node_s + node_e) // 2
            update_util(node_index * 2 + 1, node_s, mid, s, e, diff)
            update_util(node_index * 2 + 2, mid +
                        1, node_e, s, e, diff)


def query_util(node_index, node_s, node_e, s, e):
    propagate(node_index, node_s, node_e)

    if node_s <= node_e and node_s <= e and node_e >= s:
        if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
            return tree[node_index]
        else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
            mid = (node_s + node_e) // 2
            return merge(query_util(2 * node_index + 1, node_s, mid, s, e), query_util(2 * node_index + 2, mid + 1, node_e, s, e))
    else:
        return 0  # null value for summation query


def query(s, e):
    # [s,e]
    return query_util(0, 0, N-1, s, e)


for q in queries:
    if q[0] == "p":
        node = int(q[1])-1
        update(start[node]+1, end[node], int(q[2]))
    else:
        node = int(q[1])-1
        print(query(start[node], start[node]))
