from collections import defaultdict

MAX_N = 100_001

def just_bigger_power_2(val):
    i=0
    while 2**i < val:
        i+=1
    return 2**i

def generate_tree(tree_size):
    # node: [l, r, value]
    return [[0,0,0]]+ [[i<<1, i<<1|1, 0] for i in range(1, tree_size // 2)] + [[0,0,0] for _ in range(tree_size // 2)]  # dummy first element

def update(tree, node, s, e, increment, index):
    if s != e: 
        mid = (s + e) // 2
        left_ch, right_ch, val = tree[node]
        if index <= mid: # update left child
            tree[node][0] = len(tree)
            tree.append([tree[left_ch][0], tree[left_ch][1], tree[left_ch][2] + increment])
            update(tree, tree[node][0], s, mid, increment, index)
        else: # update right child
            tree[node][1] = len(tree)
            tree.append([tree[right_ch][0], tree[right_ch][1], tree[right_ch][2] + increment])
            update(tree, tree[node][1], mid + 1, e, increment, index)

def query(tree, node, s, e, l, r):
    # [l, r]
    if r < s or l > e:
        return 0
    elif l <= s and e <= r:
        return tree[node][2] # return value
    else:
        mid = (s + e) // 2
        left_ch, right_ch, val = tree[node]
        return query(tree, left_ch, s, mid, l, r) + query(tree, right_ch, mid + 1, e, l, r)

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

if __name__=="__main__":

    ##################################
    # count #points inside [1,2]x[1,3]
    ##################################
    # initialize tree
    n_tree_node = 2*just_bigger_power_2(MAX_N)
    tree = generate_tree(n_tree_node)
    # set points [(1,1), (2,3), (3,5)]
    x2y = defaultdict(list)
    x2y[1] = [1]
    x2y[2] = [3]
    x2y[3] = [5]
    # update tree with node (l,r,value)
    root = [1]
    for i in range(1,MAX_N+1):
        prev_root = root[-1]
        new_root = len(tree)
        root.append(new_root)
        tree.append([tree[prev_root][0], tree[prev_root][1], tree[prev_root][2]]) # initialize with prev root
        for y in x2y[i]:
            tree[new_root][2] += 1 # increment value
            update(tree, new_root, 0, MAX_N-1, 1, y) # add log(len(tree)) nodes at best
    # answer query (# points inside [1,2]x[1,3])
    ans = 0
    l, r, b, t = 1,2,1,3 
    ans += (query(tree, root[r], 0, MAX_N-1, b, t) - query(tree, root[l-1], 0, MAX_N-1, b, t))
    assert ans == 2

    ##########################
    # get kth element in [l,r]
    ##########################
    # shrink coordinate
    arr = [9, 3, 1, 2]
    sorted_arr = sorted(list(set(arr)))
    mapping = {v: i for i, v in enumerate(sorted_arr)}
    inverse_mapping = {i: v for i, v in enumerate(sorted_arr)}
    shrinked_arr = [mapping[el] for el in arr]
    
    L = len(arr)
    treesize = 2*just_bigger_power_2(L)
    tree = generate_tree(treesize)

    # update tree with node (l,r,value)
    root = [1]
    for i in range(L):
        prev_root = root[-1]
        new_root = len(tree)
        root.append(new_root)
        tree.append([tree[prev_root][0], tree[prev_root][1], tree[prev_root][2] + 1])
        update(tree, new_root, 0, L-1, 1, shrinked_arr[i])

    # 2nd smallest element in [1,3] == 3
    l, r, k = 1, 3, 2
    index = get_kth(tree, root[r], root[l-1], 0, L-1, k)
    assert inverse_mapping[index] == 3

    # 1st smallest element in [3,4] == 1
    l, r, k = 3, 4, 1
    index = get_kth(tree, root[r], root[l-1], 0, L-1, k)
    assert inverse_mapping[index] == 1
