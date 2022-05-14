# general tree
from collections import deque


def dfs_preorder(adjacency_list, root, neighbor_func):
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

def dfs_postorder(adjacency_list, root, neighbor_func):
    # returns valid postorder sequence
    stack = [root]
    second_visit = set()
    marked = set([root])
    postorder = []
    while stack:
        node = stack.pop()
        list_neighbors = [ne for ne in neighbor_func(adjacency_list, node) if ne not in marked]
        if len(list_neighbors)==0: # add leaf node
            postorder.append(node)
        else:
            if node in second_visit: # add second visit of the intermediate node
                postorder.append(node)
            else:
                stack.append(node) # push node at first visit of the intermediate node
                # push neighbors
                for ne in list_neighbors:
                    if ne not in marked:
                        stack.append(ne)
                        marked.add(ne)
                second_visit.add(node)
                
    return postorder


def bfs(adjacency_list, root, neighbor_func):
    # returns valid bfs sequence
    q = deque([root])
    marked = set([root])
    order = []
    while q:
        node = q.popleft() # visit node 
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

def preorder(root):
  return [root.val] + preorder(root.left) + preorder(root.right) if root else []

def inorder(root):
  return  inorder(root.left) + [root.val] + inorder(root.right) if root else []

def postorder(root):
  return  postorder(root.left) + postorder(root.right) + [root.val] if root else []


if __name__=="__main__":

    ###################
    # graph structure #
    ######   0   ######
    ####  1     2 #####
    ###  3 4 - 5 6 #### (node 4-5 are connected)
    ###################
    adjacency_list = [[1, 2], [0, 3, 4], [0, 5, 6], [1], [1, 5], [2, 4], [2]]
    neighbor_func = lambda x,y:x[y]
    print(dfs_preorder(adjacency_list, 0, neighbor_func)) # [0, 2, 6, 5, 4, 1, 3]
    print(dfs_postorder(adjacency_list, 0, neighbor_func)) # [6, 4, 5, 2, 3, 1, 0]
    print(bfs(adjacency_list, 0, neighbor_func)) # [0, 1, 2, 3, 4, 5, 6]

    ###################
    # graph structure #
    ######   0   ######
    ####  1     2 #####
    ###  3 4 - 5 6 #### (node 4-5 and 3-6 are connected)
    ##   |_______|   ##
    ###################
    print(dfs_postorder([[1, 2], [0, 3, 4], [0, 5, 6], [1,6], [1, 5], [2, 4], [2, 3]], 0, neighbor_func)) # [3, 6, 4, 5, 2, 1, 0]

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
    print(preorder(node0)) # [0, 1, 3, 4, 2, 5, 6]
    print(inorder(node0)) # [3, 1, 4, 0, 5, 2, 6]
    print(postorder(node0)) # [3, 4, 1, 5, 6, 2, 0]