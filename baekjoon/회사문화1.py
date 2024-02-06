import sys
from sys import stdin
input = stdin.readline

sys.setrecursionlimit(200_009)


def just_bigger_power_2(val):
    i = 0
    while 2**i < val:
        i += 1
    return 2**i


count = 0


def eulerian_technique(node):
    global count
    stack = [node]
    while stack:
        now = stack[-1]
        if start[now] == 0:
            count += 1
            start[now] = count
        check = False
        for nxt in adj[now]:
            if start[nxt] == 0:
                stack.append(nxt)
                check = True
                break
        if check == False:
            end[now] = count
            stack.pop()


n, m = map(int, input().split())

adj = [[] for _ in range(n)]
for i, p in enumerate(map(int, input().split())):
    if p != -1:
        adj[p-1].append(i)

queries = [map(int, input().split()) for _ in range(m)]

start = [0] * n
end = [0] * n
eulerian_technique(0)
start = [s-1 for s in start]
end = [e-1 for e in end]

tree = [0] * 2 * just_bigger_power_2(n)
lazy = [0] * 2 * just_bigger_power_2(n)


def initialize(tree, arr, s, e, index):
    if s <= e:
        if s == e:  # leaf node
            tree[index] = arr[s]
        else:
            mid = (s + e) // 2
            initialize(tree, arr, s, mid, index * 2 + 1)
            initialize(tree, arr, mid + 1, e, index * 2 + 2)


initialize(tree, [0]*n, 0, n-1, 0)


def update(tree, lazy, s, e, diff):
    update_util(tree, lazy, 0, 0, n - 1, s, e, diff)


def propagate(tree, lazy, node_index, node_s, node_e):
    if lazy[node_index] != 0:  # reflect lazy updates
        tree[node_index] += (node_e - node_s + 1) * lazy[node_index] 
        if node_s != node_e:  # intermediate node
            lazy[node_index * 2 + 1] += lazy[node_index]
            lazy[node_index * 2 + 2] += lazy[node_index]
        lazy[node_index] = 0


def update_util(tree, lazy, node_index, node_s, node_e, s, e, diff):
    propagate(tree, lazy, node_index, node_s, node_e)

    if node_s <= node_e and node_s <= e and node_e >= s:
        if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
            tree[node_index] += (node_e - node_s + 1) * diff 
            if node_s != node_e:  # intermediate node
                lazy[node_index * 2 + 1] += diff
                lazy[node_index * 2 + 2] += diff
        else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
            mid = (node_s + node_e) // 2
            update_util(tree, lazy, node_index * 2 +
                        1, node_s, mid, s, e, diff)
            update_util(tree, lazy, node_index * 2 + 2, mid +
                        1, node_e, s, e, diff)
            tree[node_index] = tree[node_index * 2 + 1] + tree[node_index * 2 + 2] 


def query_util(tree, lazy, node_index, node_s, node_e, s, e):
    propagate(tree, lazy, node_index, node_s, node_e)

    if node_s <= node_e and node_s <= e and node_e >= s:
        if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
            return tree[node_index]
        else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
            mid = (node_s + node_e) // 2
            return query_util(tree, lazy, 2 * node_index + 1, node_s, mid, s, e) + query_util(tree, lazy, 2 * node_index + 2, mid + 1, node_e, s, e)
    else:
        return 0


def query(tree, lazy, s, e):
    # [s,e]
    return query_util(tree, lazy, 0, 0, n-1, s, e)


for node, w  in queries:
    node -= 1
    update(tree, lazy, start[node], end[node], w)

print(" ".join([str(query(tree, lazy, start[i], start[i])) for i in range(n)]))
