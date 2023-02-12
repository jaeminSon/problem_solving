import sys
from collections import defaultdict

MAX_N = 100_001

def just_bigger_power_2(val):
    i=0
    while 2**i < val:
        i+=1
    return 2**i

def generate_tree(tree_size):
    return [[0,0,0]]+ [[i<<1, i<<1|1, 0] for i in range(1, tree_size // 2)] + [[0,0,0] for i in range(tree_size // 2)] # dummy first element

def update(tree, node, s, e, increment, index):
    if s != e: 
        mid = (s + e) // 2
        left_ch = tree[node][0]
        right_ch = tree[node][1]
        if index <= mid: # update left child
            tree[node][0] = len(tree)
            tree.append([tree[left_ch][0], tree[left_ch][1], tree[left_ch][2] + increment])
            update(tree, tree[node][0], s, mid, increment, index)
        else: # update right child
            tree[node][1] = len(tree)
            tree.append([tree[right_ch][0], tree[right_ch][1], tree[right_ch][2] + increment])
            update(tree, tree[node][1], mid + 1, e, increment, index)

def query(tree, node, s, e, l, r):
    if r < s or l > e:
        return 0
    elif l <= s and e <= r:
        return tree[node][2] # return value
    else:
        mid = (s + e) // 2
        left_ch = tree[node][0]
        right_ch = tree[node][1]
        return query(tree, left_ch, s, mid, l, r) + query(tree, right_ch, mid + 1, e, l, r)

T = int(sys.stdin.readline().rstrip())
for _ in range(T):
    n,m  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    n_tree_node = 2*just_bigger_power_2(MAX_N)
    tree = generate_tree(n_tree_node)
    
    x2y = defaultdict(list)
    for _ in range(n):
        x,y = [int(d) for d in sys.stdin.readline().rstrip().split()]
        x2y[x+1].append(y+1)
    
    # update tree with node (l,r,value)
    root = [1]
    for i in range(1,MAX_N+1):
        prev_root = root[-1]
        new_root = len(tree)
        root.append(new_root)
        tree.append([tree[prev_root][0], tree[prev_root][1], tree[prev_root][2]]) # initialize with prev root
        for y in x2y[i]:
            tree[new_root][2] += 1 # increment value
            update(tree, new_root, 1, MAX_N, 1, y)

    # answer queries
    ans = 0
    for _ in range(m):
        l, r, b, t = [int(d) for d in sys.stdin.readline().rstrip().split()]
        ans += (query(tree, root[r+1], 1, MAX_N, b+1, t+1) - query(tree, root[l], 1, MAX_N, b+1, t+1))
    print(ans)