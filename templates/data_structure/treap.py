# https://gist.github.com/sabal202/2cda62c94c11c49434a84501ff4d3cc9
from random import uniform

class Node(object):

    def __init__(self, k):
        self.priority = uniform(0, 10 ** 9)
        self.key = k
        self.size = 1
        self.L = self.R = None


def merge(A, B):
    if A is None: return B
    if B is None: return A
    if A.priority > B.priority:
        A.R = merge(update_size(A.R), update_size(B))
        return update_size(A)
    else:
        B.L = merge(update_size(A), update_size(B.L))
        return update_size(B)


def split(T, k):
    # Left < k, k <= Right
    if T is None: return (T, T)
    if k <= T.key:
        L, R = split(T.L, k)
        T.L = update_size(R)
        return (update_size(L), T)
    else:
        L, R = split(T.R, k)
        T.R = update_size(L)
        return (T, update_size(R))


def insert(T, key):
    if T is None:
        return Node(key)
    else:
        L, R = split(T, key)
        return merge(merge(L, Node(key)), R)


def erase(T, key):
    # erase all nodes with a given key
    L, R = split(T, key)
    RL, RR = split(R, key + 1)
    return merge(L, RR)


def update_size(T):
    if T is None: 
        return T
    else:
        T.size = size(T.L) + size(T.R) + 1
        return T


def find(T, n):
    if T is None: return T
    root_n = size(T.R) # largest value in rightmost node
    if n == root_n:
        return T
    elif n > root_n:
        return find(T.L, n - (root_n + 1))
    else:
        return find(T.R, n)

def size(T):
    return 0 if T is None else T.size

def print_inorder(node):
    if node is None:
        return
    else:
        print_inorder(node.L)
        print(node.key)
        print_inorder(node.R)

if __name__=="__main__":
    # max Treap (or randomized cartesian tree with (key, (random) priority))
    #      28
    #    /   \
    #   10     30
    #  /         \
    # 5          40
 
    arr = [5, 10, 40, 30, 28]
    n = len(arr)
    t = None
    for el in arr:
        t = insert(t, el)
    
    print_inorder(t)
    for i in range(n):
        print("{}: {}".format(i, find(t, i).key))