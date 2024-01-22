from sys import stdin
input = stdin.readline


def just_bigger_power_2(val):
    i = 0
    while 2**i < val:
        i += 1
    return 2**i


def generate_tree(tree_size):
    # node: [l, r, value]
    # dummy first element
    return [[0, 0, 0]] + [[i << 1, i << 1 | 1, 0] for i in range(1, tree_size // 2)] + [[0, 0, 0] for _ in range(tree_size // 2)]


def update(tree, node, s, e, increment, index):
    tree[node][2] += increment
    if s != e:
        mid = (s + e) // 2
        left_ch, right_ch, val = tree[node]
        if index <= mid:  # update left child
            tree[node][0] = len(tree)
            tree.append([tree[left_ch][0], tree[left_ch][1], tree[left_ch][2]])
            update(tree, tree[node][0], s, mid, increment, index)
        else:  # update right child
            tree[node][1] = len(tree)
            tree.append(
                [tree[right_ch][0], tree[right_ch][1], tree[right_ch][2]])
            update(tree, tree[node][1], mid + 1, e, increment, index)


def get_kth(tree, next_node, prev_node, s, e, k):
    if s == e:
        return s
    else:
        left_size = tree[tree[next_node][0]][2] - tree[tree[prev_node][0]][2]
        mid = (s + e) // 2
        if k <= left_size:
            return get_kth(tree, tree[next_node][0], tree[prev_node][0], s, mid, k)
        else:
            return get_kth(tree, tree[next_node][1], tree[prev_node][1], mid+1, e, k-left_size)


def n_elements_leq_x(tree, next_node, prev_node, s, e, x):
    if s == e:
        return tree[next_node][2] - tree[prev_node][2]
    else:
        left_size = tree[tree[next_node][0]][2] - tree[tree[prev_node][0]][2]
        mid = (s + e) // 2
        if x <= mid:
            return n_elements_leq_x(tree, tree[next_node][0], tree[prev_node][0], s, mid, x)
        else:
            return left_size + n_elements_leq_x(tree, tree[next_node][1], tree[prev_node][1], mid+1, e, x)


def xor(tree, next_node, prev_node, s, e, x, shift):
    if s == e:
        return s
    else:
        left_size = tree[tree[next_node][0]][2] - tree[tree[prev_node][0]][2]
        right_size = tree[tree[next_node][1]][2] - tree[tree[prev_node][1]][2]
        mid = (s + e) // 2
        if ((x >> shift) & 1) == 1:
            if left_size > 0:
                return xor(tree, tree[next_node][0], tree[prev_node][0], s, mid, x, shift-1)
            else:
                return xor(tree, tree[next_node][1], tree[prev_node][1], mid+1, e, x, shift-1)
        else:
            if right_size > 0:
                return xor(tree, tree[next_node][1], tree[prev_node][1], mid+1, e, x, shift-1)
            else:
                return xor(tree, tree[next_node][0], tree[prev_node][0], s, mid, x, shift-1)


n_tree_node = 2**20
L = 2**19
tree = generate_tree(n_tree_node)
root = [1] * L
curr_n_root = 0

M = int(input())

questions = []
for _ in range(M):
    questions.append(input().split())

for l in questions:
    
    if l[0] == "1":
        curr_n_root += 1
        root[curr_n_root] = len(tree)
        prev_root = root[curr_n_root-1]
        tree.append([tree[prev_root][0], tree[prev_root]
                    [1], tree[prev_root][2]])
        update(tree, root[curr_n_root], 0, L-1, 1, int(l[1]))
    elif l[0] == "2":
        ans = xor(tree, root[int(l[2])],
                  root[int(l[1])-1], 0, L-1, int(l[3]), 18)
        print(ans)
    elif l[0] == "3":
        curr_n_root -= int(l[1])
    elif l[0] == "4":
        ans = n_elements_leq_x(
            tree, root[int(l[2])], root[int(l[1])-1], 0, L-1, int(l[3]))
        print(ans)
    elif l[0] == "5":
        ans = get_kth(tree, root[int(l[2])],
                      root[int(l[1])-1], 0, L-1, int(l[3]))
        print(ans)
