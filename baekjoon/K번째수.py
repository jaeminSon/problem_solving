import sys


def just_bigger_power_2(val):
    i = 0
    while 2**i < val:
        i += 1
    return 2**i


def generate_tree(tree_size):
    return [[0, 0, 0]] + [[i << 1, i << 1 | 1, 0] for i in range(1, tree_size // 2)] + [[0,0,0] for i in range(tree_size // 2)]


def update(tree, node, s, e, increment, index):
    if s != e:
        mid = (s + e) // 2
        left_ch, right_ch, val = tree[node]
        if index <= mid:  # update left child
            tree[node][0] = len(tree)
            tree.append([tree[left_ch][0], tree[left_ch][1], tree[left_ch][2] + increment])
            update(tree, tree[node][0], s, mid, increment, index)
        else:  # update right child
            tree[node][1] = len(tree)
            tree.append([tree[right_ch][0], tree[right_ch][1], tree[right_ch][2] + increment])
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


n, m = [int(d) for d in sys.stdin.readline().rstrip().split()]

l_val = [int(d) for d in sys.stdin.readline().rstrip().split()]

queries = [[int(d) for d in sys.stdin.readline().rstrip().split()]
           for _ in range(m)]

l_unique_sorted = sorted(list(set(l_val)))
mapping = {v: i for i, v in enumerate(l_unique_sorted)}
inverse_mapping = {i: v for i, v in enumerate(l_unique_sorted)}
shrinked_coord = [mapping[el] for el in l_val]

L = len(shrinked_coord)
treesize = 2*just_bigger_power_2(L)
tree = generate_tree(treesize)

# update tree with node (l,r,value)
root = [1]
for i in range(L):
    prev_root = root[-1]
    new_root = len(tree)
    root.append(new_root)
    # initialize with prev root
    tree.append([tree[prev_root][0], tree[prev_root][1], tree[prev_root][2]+1])
    update(tree, new_root, 0, L-1, 1, shrinked_coord[i])

for q in queries:
    l, r, k = q
    index = get_kth(tree, root[r], root[l-1], 0, L-1, k)
    print(inverse_mapping[index])
