class Node(object):

    def __init__(self, k):
        self.key = k
        self.P = self.L = self.R = None

def build_cartesian_tree(arr):

    n = len(arr)
    root = Node(arr[0])
    nearest_parent = root
    for i in range(1, n):
        # position new node (arr[i]) at the right child of the rightmost node
        # and find the parent with value > arr[i]
        while nearest_parent.key <= arr[i] and nearest_parent.P is not None:
            nearest_parent = nearest_parent.P
 
        new_node = Node(arr[i])
        if nearest_parent.key <= arr[i]:
            # arr[i] is greater than root (set new root)
            root.P = new_node
            new_node.L = root
            root = new_node
        elif nearest_parent.R is None:
            # right node is empty (position new node here)
            nearest_parent.R = new_node
            new_node.P = nearest_parent
        else:
            # right node is not empty (replace with new node)
            nearest_parent.R.P = new_node
            new_node.L = nearest_parent.R
            nearest_parent.R = new_node
            new_node.P = nearest_parent
    
        nearest_parent = new_node
        
    return root

def print_inorder(node):
    if node is None:
        return
    else:
        print_inorder(node.L)
        print(node.key)
        print_inorder(node.R)

if __name__=="__main__":
    # max tree    
    #      40
    #    /   \
    #   10     30
    #  /         \
    # 5          28 
 
    arr = [5, 10, 40, 30, 28]
    t = build_cartesian_tree(arr)
    print_inorder(t)