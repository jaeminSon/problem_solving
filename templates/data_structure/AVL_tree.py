class Node(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
 
class AVLTree(object):
 
    def _balance(self, root):
        balance = self.get_balance(root) # left-right
 
        # new node at left-left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root) # clockwise
 
        # new node at right-right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)  # counter-clockwise
 
        # new node at left-right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
 
        # new node at right-left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
 
        return root

    def insert(self, root, key):
     
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
 
        root.height = 1 + max(self.get_height(root.left),
                           self.get_height(root.right))
        
        return self._balance(root)

    def delete(self, root, key):
 
        if root is None:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        elif key == root.key: 
            if root.left is None:
                new_root = root.right
                root = None
                return new_root
            elif root.right is None:
                new_root = root.left
                root = None
                return new_root
            else:
                min_val = self.get_min_value(root.right)
                root.key = min_val
                root.right = self.delete(root.right, min_val)
    
        root.height = 1 + max(self.get_height(root.left),
                            self.get_height(root.right))
 
        return self._balance(root)
 
    def left_rotate(self, root):
        new_root = root.right 
        root.right = new_root.left
        new_root.left = root
 
        root.height = 1 + max(self.get_height(root.left),
                         self.get_height(root.right))
        new_root.height = 1 + max(self.get_height(new_root.left),
                         self.get_height(new_root.right))
 
        return new_root
 
    def right_rotate(self, root):
        new_root = root.left
        root.left = new_root.right
        new_root.right = root
 
        root.height = 1 + max(self.get_height(root.left),
                        self.get_height(root.right))
        new_root.height = 1 + max(self.get_height(new_root.left),
                        self.get_height(new_root.right))
 
        return new_root
 
    def get_height(self, root):
        if root is None:
            return 0
        else:
            return root.height
 
    def get_balance(self, root):
        if root is None:
            return 0
        else:
            return self.get_height(root.left) - self.get_height(root.right)
 
    def get_min_value(self, root):
        if root.left is None:
            return root.key
        else:
            return self.get_min_value(root.left)

    def preorder(self, root):
        if not root:
            return []
        else:
            return [root.key] + self.preorder(root.left) + self.preorder(root.right)
 
 
if __name__ == "__main__":
    avl = AVLTree()
    root = None
    
    # import time
    # st = time.time()
    # for i in range(1000000):
    #     root = avl.insert(root, i)
    # for i in range(1000000):
    #     root = avl.delete(root, i)
    # print(time.time()-st)

    root = avl.insert(root, 10)
    root = avl.insert(root, 20)
    root = avl.insert(root, 30)
    root = avl.insert(root, 40)
    root = avl.insert(root, 50)
    root = avl.insert(root, 25)
    #       30
    #      /  \
    #     20   40
    #    /  \    \
    #   10  25    50
    print(avl.preorder(root))

    root = avl.delete(root, 30)
    #       40
    #      /  \
    #     20   50
    #    /  \    
    #   10  25  
    print(avl.preorder(root))