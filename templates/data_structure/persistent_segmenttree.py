from collections import defaultdict

import sys
sys.path.append("..")
from custom_type import TREE, NAT


def just_bigger_power_2(val):
    i=0
    while 2**i < val:
        i+=1
    return 2**i

def generate_tree(tree_size:NAT) -> TREE:
    """
    Generate an empty tree with a node of [index_to_left_child, index_to_right_child, value]
    """
    return [[0,0,0]]+ [[i<<1, i<<1|1, 0] for i in range(1, tree_size // 2)] + [[0,0,0] for _ in range(tree_size // 2)]  # dummy first element

def update(tree:TREE, node, s, e, increment, index):
    """
    Increment a value at <index> while recursively updating a node value and a child node.
    [<s>,<e>] represents the range of <node> and <tree> is a list.
    A new node is appended with its values copied from the previous child node.
    Nodes are created only when update is required.

    Before calling this function, make sure new root is appended to tree.
    """
    tree[node][2] += increment
    if s != e: 
        mid = (s + e) // 2
        left_ch, right_ch, val = tree[node]
        if index <= mid: # update left child
            tree[node][0] = len(tree)
            tree.append([tree[left_ch][0], tree[left_ch][1], tree[left_ch][2]])
            update(tree, tree[node][0], s, mid, increment, index)
        else: # update right child
            tree[node][1] = len(tree)
            tree.append([tree[right_ch][0], tree[right_ch][1], tree[right_ch][2]])
            update(tree, tree[node][1], mid + 1, e, increment, index)

def query(tree:TREE, node, s, e, l, r):
    """
    Query a value for range [l,r] (inclusive)
    """
    if r < s or l > e:
        return 0
    elif l <= s and e <= r:
        return tree[node][2] # return value
    else:
        mid = (s + e) // 2
        left_ch, right_ch, val = tree[node]
        return query(tree, left_ch, s, mid, l, r) + query(tree, right_ch, mid + 1, e, l, r)

def get_kth(tree:TREE, next_node, prev_node, s, e, k):
    """
    Return index of <k>th value added between <prev_node> and <next_node>.
    [<s>,<e>] always includes index of <k>th value and the range is recursively narrowed down.
    Each node in tree is [index_to_left_child, index_to_right_child, total counts in [s,e] (inclusive)]
    """
    if s == e:
        return s
    else:
        left_size = tree[tree[next_node][0]][2] - tree[tree[prev_node][0]][2]
        mid = (s + e) // 2
        if k <= left_size:
            return get_kth(tree, tree[next_node][0], tree[prev_node][0], s, mid, k)
        else:
            return get_kth(tree, tree[next_node][1], tree[prev_node][1], mid+1, e, k-left_size)

def n_elements_leq_x(tree:TREE, next_node, prev_node, s, e, x):
    """
    Return the number of integers less than or equal to <x> among values added between <prev_node> and <next_node>.
    [<s>,<e>] always includes <x> and the range is recursively narrowed down.
    Each node in tree is [index_to_left_child, index_to_right_child, total counts in [s,e] (inclusive)]
    """
    if s == e:
        return tree[next_node][2] - tree[prev_node][2]
    else:
        left_size = tree[tree[next_node][0]][2] - tree[tree[prev_node][0]][2]
        mid = (s + e) // 2
        if x <= mid:
            return n_elements_leq_x(tree, tree[next_node][0], tree[prev_node][0], s, mid, x)
        else:
            return left_size + n_elements_leq_x(tree, tree[next_node][1], tree[prev_node][1], mid+1, e, x)

if __name__=="__main__":

    ##################################
    # count #points inside [1,2]x[1,3]
    ##################################
    # initialize tree
    MAX_N = 100_001
    L = just_bigger_power_2(MAX_N) # L should be power of 2
    n_tree_node = 2 * L
    tree = generate_tree(n_tree_node)
    # set points [(1,1), (2,3), (3,5)]
    x2y = defaultdict(list)
    x2y[1] = [1]
    x2y[2] = [3]
    x2y[3] = [5]
    # update tree with node (l,r,value)
    root = [1]
    for i in range(1, MAX_N+1):
        prev_root = root[-1]
        new_root = len(tree)
        root.append(new_root)
        tree.append([tree[prev_root][0], tree[prev_root][1], tree[prev_root][2]]) # initialize with prev root
        for y in x2y[i]:
            update(tree, new_root, 0, L-1, 1, y) # add log(len(tree)) nodes at best
    # answer query (# points inside [1,2]x[1,3])
    ans = 0
    l, r, b, t = 1,2,1,3 
    ans += (query(tree, root[r], 0, L-1, b, t) - query(tree, root[l-1], 0, L-1, b, t))
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
    
    L = just_bigger_power_2(L)  # L should be power of 2
    treesize = 2 * L
    tree = generate_tree(treesize)

    # update tree with node (l,r,value)
    root = [1]
    for i in range(len(arr)):
        prev_root = root[-1]
        new_root = len(tree)
        root.append(new_root)
        tree.append([tree[prev_root][0], tree[prev_root][1], tree[prev_root][2]])
        update(tree, new_root, 0, L-1, 1, shrinked_arr[i])

    # 2nd smallest element in [9,3,1] == 3
    l, r, k = 1, 3, 2
    index = get_kth(tree, root[r], root[l-1], 0, L-1, k)
    assert inverse_mapping[index] == 3

    # 1st smallest element in [1,2] == 1
    l, r, k = 3, 4, 1
    index = get_kth(tree, root[r], root[l-1], 0, L-1, k)
    assert inverse_mapping[index] == 1

    #######################################################
    # sum in [l,r] (tree is defined on coordinate and elements are updated)
    #######################################################
    arr = [1, 7, 8, 3, 2] # value in [0, inf]
    
    L = just_bigger_power_2(L)  # L should be power of 2
    treesize = 2 * L
    tree = generate_tree(treesize)

    # update tree with node (l,r,value)
    root = [1]
    for val in arr:
        prev_root = root[-1]
        new_root = len(tree)
        root.append(new_root)
        tree.append([tree[prev_root][0], tree[prev_root][1], tree[prev_root][2]])
        update(tree, new_root, 0, L-1, 1, val)

    # [1, 7, 8] -> [1, 7]
    l, r, x = 1, 3, 7
    ans = n_elements_leq_x(tree, root[r], root[l-1], 0, L-1, x)
    assert ans == 2
    
    # [1, 7, 8, 3, 2] -> [1, 7, 3, 2]
    l, r, x = 1, 5, 7
    ans = n_elements_leq_x(tree, root[r], root[l-1], 0, L-1, x)
    assert ans == 4
