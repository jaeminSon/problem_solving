from collections import deque, defaultdict
from typing import List, Dict

import sys
sys.path.append("..")
from custom_type import GRAPH, TREE, NODE, LIST1D


def dfs_preorder(adjacency_list: GRAPH, root: NODE, neighbor_func) -> LIST1D:
    # returns valid preorder sequence
    stack = [root]
    marked = set([root])
    preorder = []
    while stack:
        node = stack.pop()
        preorder.append(node)
        for ne in neighbor_func(adjacency_list, node):
            if ne not in marked:
                stack.append(ne)
                marked.add(ne)
    return preorder


def dfs_postorder(adjacency_list: GRAPH, root: NODE, neighbor_func) -> LIST1D:
    # returns valid postorder sequence
    stack = [root]
    marked = set([root])
    postorder = []
    while stack:
        node = stack.pop()
        list_neighbors = [ne for ne in neighbor_func(adjacency_list, node) if ne not in marked]
        if len(list_neighbors) == 0:  # add leaf node or intermediate node
            postorder.append(node)
        else:
            stack.append(node)  # push node at first visit of the intermediate node
            # push neighbors
            for ne in list_neighbors:
                if ne not in marked:
                    stack.append(ne)
                    marked.add(ne)

    return postorder


def retrieve_connected_trees(adjacency_list: GRAPH, neighbor_func) -> List[LIST1D]:
    list_trees = []
    not_marked = set(range(len(adjacency_list)))
    while len(not_marked) > 0:
        root = not_marked.pop()
        nodes = dfs_preorder(adjacency_list, root, neighbor_func)
        list_trees.append(nodes)
        not_marked -= set(nodes)
    return list_trees


def bfs(adjacency_list: GRAPH, root, neighbor_func) -> LIST1D:
    # returns valid bfs sequence
    q = deque([root])
    marked = set([root])
    order = []
    while q:
        node = q.popleft()  # visit node
        order.append(node)
        for ne in neighbor_func(adjacency_list, node):
            if ne not in marked:
                marked.add(ne)
                q.append(ne)
    return order

# binary tree (one-liner)


class Node:
    def __init__(self, val, parent=None):
        self.left = None
        self.right = None
        self.val = val
        if parent is not None:
            if parent.left is None:
                parent.left = self
            elif parent.right is None:
                parent.right = self


def preorder(root: NODE):
    return [root.val] + preorder(root.left) + preorder(root.right) if root else []


def inorder(root: NODE):
    return inorder(root.left) + [root.val] + inorder(root.right) if root else []


def postorder(root: NODE):
    return postorder(root.left) + postorder(root.right) + [root.val] if root else []


def mark_depth(adjacency_list: GRAPH, root: NODE) -> Dict[NODE, int]:
    depth = defaultdict(int)
    stack = [(root, 0)]
    marked = set([root])
    while stack:
        node, d = stack.pop()
        depth[node] = d
        for ne in adjacency_list[node]:
            if ne not in marked:
                stack.append((ne, d+1))
                marked.add(ne)
    return depth


def node_status(adjacency_list: TREE, root: NODE):
    """
    Assume connected tree
    """
    def dfs(curr, par, dep):
        size[curr] = 1
        parent[curr] = par
        depth[curr] = dep
        for ch in adjacency_list[curr]:
            if ch != par:
                size[curr] += dfs(ch, curr, dep+1)
        return size[curr]

    n_nodes = len(adjacency_list)
    size = [0] * n_nodes
    depth = [0] * n_nodes
    parent = [-1] * n_nodes

    dfs(root, -1, 0)

    return size, depth, parent


def dfs_recursive(adjacency_list: TREE, curr, n_nodes: int):
    def dfs(node):
        visited[curr] = True
        for ch in adjacency_list[curr]:
            if not visited[ch]:
                pass
                # <returned_value_from_child> = dfs(ch)
                # <do some operations>
    
    # to avoid visiting multiple nodes when dealing with a multiple trees
    # reference visited when checking 'visited'
    # ========================
    # visited = [False]*(N+1)
    # for i in range(N+1):
    #     if not visited[i]:
    #         dfs(i)
    # ========================
    visited = [False] * n_nodes
    return None  # <something>


if __name__ == "__main__":

    ###################
    # graph structure #
    ######   0   ######
    ####  1     2 #####
    # 3 4 - 5 6 #### (node 4-5 are connected)
    ###################
    adjacency_list = [[1, 2], [0, 3, 4], [0, 5, 6], [1], [1, 5], [2, 4], [2]]
    def neighbor_func(x, y): return x[y]
    assert dfs_preorder(adjacency_list, 0, neighbor_func) == [0, 2, 6, 5, 4, 1, 3]
    assert dfs_postorder(adjacency_list, 0, neighbor_func) == [6, 4, 5, 2, 3, 1, 0]
    assert bfs(adjacency_list, 0, neighbor_func) == [0, 1, 2, 3, 4, 5, 6]

    ###################
    # graph structure #
    ######   0   ######
    ####  1     2 #####
    # 3 4 - 5 6 #### (node 4-5 and 3-6 are connected)
    ##   |_______|   ##
    ###################
    assert dfs_postorder([[1, 2], [0, 3, 4], [0, 5, 6], [1, 6], [1, 5], [2, 4], [2, 3]], 0, neighbor_func) == [3, 6, 4, 5, 2, 1, 0]

    ##################
    # tree structure #
    ######   0   #####
    ####  1     2 ####
    ###  3 4   5 6 ###
    ##################
    node0 = Node(0)
    node1 = Node(1, node0)
    node2 = Node(2, node0)
    node3 = Node(3, node1)
    node4 = Node(4, node1)
    node5 = Node(5, node2)
    node6 = Node(6, node2)
    assert preorder(node0) == [0, 1, 3, 4, 2, 5, 6]
    assert inorder(node0) == [3, 1, 4, 0, 5, 2, 6]
    assert postorder(node0) == [3, 4, 1, 5, 6, 2, 0]

    assert mark_depth([[1, 2], [0, 3, 4], [0, 5, 6], [1], [1], [2], [2]], 0) == {0: 0, 2: 1, 6: 2, 5: 2, 1: 1, 4: 2, 3: 2}

    assert node_status([[], [5, 2], [1], [4, 5], [3], [1, 3]], 1) == ([0, 5, 1, 2, 1, 3], [0, 0, 1, 2, 3, 1], [-1, -1, 1, 5, 3, 1])
