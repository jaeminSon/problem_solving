import sys

class Node():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = "RED"

class RedBlack(object):

    def __init__(self):
        self.NULLNODE = Node(float("inf"))
        self.NULLNODE.color = "BLACK"
        self.root = self.NULLNODE

    def find(self, node_top, key):
        if node_top == self.NULLNODE:
            return None
        elif key == node_top.key:
            return node_top
        elif key < node_top.key:
            return self.find(node_top.left, key)
        elif key > node_top.key:
            return self.find(node_top.right, key)
        else:
            ValueError("Unexpected node ({}) and key ({})".format(node_top, key))

    def _is_left_child(self, node):
        return node == node.parent.left

    def _is_right_child(self, node):
        return node == node.parent.right

    def balance_after_delete(self, node):

        def _handle_red_sibling(node, sibling, left_sibling):
            #          /   \
            #        red  *black  <- node (left_sibling==True)
            sibling.color = "BLACK"
            node.parent.color = "RED"
            if left_sibling:
                self.right_rotate(node.parent)
            else:
                self.left_rotate(node.parent)

        def _handle_black_sibling_with_black_children(node, sibling):
            #            /   \
            #        black  *black  <- node (left_sibling==True)
            #        /    \  
            #    black    black     
            sibling.color = "RED"

        def _handle_black_sibling_with_red_child(node, sibling, left_sibling):
            #            /   \
            #        black  *black  <- node (left_sibling==True)
            #          /      
            #        red         
            if left_sibling:
                if sibling.left.color == "BLACK":
                    sibling.right.color = "BLACK"
                    sibling.color = "RED"
                    self.left_rotate(sibling)
                    sibling = node.parent.left
                
                sibling.color = node.parent.color
                node.parent.color = "BLACK"
                sibling.left.color = "BLACK"
                self.right_rotate(node.parent)

            else:
                if sibling.right.color == "BLACK":
                    sibling.left.color = "BLACK"
                    sibling.color = "RED"
                    self.right_rotate(sibling)
                    sibling = node.parent.right
                
                sibling.color = node.parent.color
                node.parent.color = "BLACK"
                sibling.right.color = "BLACK"
                self.left_rotate(node.parent)
                

        # maintain #blacknodes on both sides
        while node != self.root and node.color == "BLACK":
            if self._is_left_child(node):
                sibling = node.parent.right
                if sibling.color == "RED":
                    _handle_red_sibling(node, sibling, left_sibling=False)
                    sibling = node.parent.right
                
                if sibling.left.color == "BLACK" and sibling.right.color == "BLACK":
                    _handle_black_sibling_with_black_children(node, sibling)
                    node = node.parent
                else:
                    _handle_black_sibling_with_red_child(node, sibling, left_sibling=False)
                    node = self.root
            
            elif self._is_right_child(node):
                sibling = node.parent.left
                if sibling.color == "RED":
                    _handle_red_sibling(node, sibling, left_sibling=True)
                    sibling = node.parent.left
                
                if sibling.left.color == "BLACK" and sibling.right.color == "BLACK":
                    _handle_black_sibling_with_black_children(node, sibling)
                    node = node.parent
                else:
                    _handle_black_sibling_with_red_child(node, sibling, left_sibling=True)
                    node = self.root
            
            else:
                raise ValueError("Unknown node type.")
        node.color = "BLACK"

    def _connect(self, parent, child, is_right=True):
        child.parent = parent
        if is_right:
            parent.right = child
        else:
            parent.left = child

    def _replace(self, u, v):
        if u.parent == None: # u is root
            self.root = v
        elif self._is_left_child(u):
            u.parent.left = v
        elif self._is_right_child(u):
            u.parent.right = v
        else:
            raise ValueError("Unknown node type.")
        
        v.parent = u.parent

    def delete(self, key):
        
        # find the rightmost node with the same key
        node = self.root
        target = self.NULLNODE
        while node != self.NULLNODE:
            if node.key == key:
                target = node
            
            node = node.right if node.key <= key else node.left

        assert target != self.NULLNODE, "No node exists with the key"

        if target.left == self.NULLNODE:
            substituted_node = target.right
            target_color = target.color
            self._replace(target, target.right)
        elif target.right == self.NULLNODE:
            substituted_node = target.left
            target_color = target.color
            self._replace(target, target.left)
        else:
            successor_node = self.get_min_node(target.right)
            target_color = successor_node.color
            substituted_node = successor_node.right
            if successor_node.parent != target:
                self._replace(successor_node, successor_node.right)
                self._connect(parent=successor_node, child=target.right, is_right=True)
            
            self._replace(target, successor_node)
            successor_node.left = target.left
            successor_node.left.parent = successor_node
            successor_node.color = target.color
        
        if target_color == "BLACK":
            self.balance_after_delete(substituted_node)

    def balance_after_insert(self, k):

        def _handle_red_sibling_of_parent(node, left_parent):
            #            /   \
            #          red   red
            #         / 
            #       *red  <- node (left_parent==True)
            if left_parent:
                node.parent.parent.right.color = "BLACK"
            else:
                node.parent.parent.left.color = "BLACK"
            node.parent.color = "BLACK"
            node.parent.parent.color = "RED"
            return node.parent.parent

        def _handle_black_sibling_of_parent(node, left_parent):
            #            /   \
            #          red   black
            #         / 
            #       *red  <- node (left_parent==True)
            if left_parent:
                if self._is_right_child(node):
                    parent = node = node.parent
                    self.left_rotate(node)
            else:
                if self._is_left_child(node):
                    parent = node = node.parent
                    self.right_rotate(node)
            
            node.parent.color = "BLACK"
            node.parent.parent.color = "RED"
            
            if left_parent:
                self.right_rotate(node.parent.parent)
            else:
                self.left_rotate(node.parent.parent)

            return parent

        while k!=self.root and k.parent.color == "RED":
            if self._is_right_child(k.parent):
                sibling_of_parent = k.parent.parent.left
                if sibling_of_parent.color == "RED":
                    k = _handle_red_sibling_of_parent(k, left_parent=False)
                else:
                    k = _handle_black_sibling_of_parent(k, left_parent=False)
            elif self._is_left_child(k.parent):
                sibling_of_parent = k.parent.parent.right

                if sibling_of_parent.color == "RED":
                    _handle_red_sibling_of_parent(k, left_parent=True)
                    k = k.parent.parent
                else:
                    k = _handle_black_sibling_of_parent(k, left_parent=True)
            else:
                raise ValueError("Unknown node type.")
        self.root.color = "BLACK"

    def left_rotate(self, root):
        new_root = root.right
        root.right = new_root.left
        if new_root.left != self.NULLNODE:
            new_root.left.parent = root
        self._replace(root, new_root)
        self._connect(parent=new_root, child=root, is_right=False)

    def right_rotate(self, root):
        new_root = root.left
        root.left = new_root.right
        if new_root.right != self.NULLNODE:
            new_root.right.parent = root
        self._replace(root, new_root)
        self._connect(parent=new_root, child=root, is_right=True)

    def insert(self, key):

        def find_parent_for_insert(x):
            node = None
            while x != self.NULLNODE:
                node = x
                x = x.left if new_node.key < x.key else x.right
            return node

        new_node = Node(key)
        new_node.left = self.NULLNODE
        new_node.right = self.NULLNODE
        new_node.parent = find_parent_for_insert(self.root)
        if new_node.parent == None:
            new_node.color = "BLACK"
            self.root = new_node
        else:
            if new_node.key < new_node.parent.key:
                new_node.parent.left = new_node
            else:
                new_node.parent.right = new_node

            if new_node.parent.parent is not None:
                self.balance_after_insert(new_node)

    def print_tree(self):
        self.__print_helper(self.root, "", True)

    def __print_helper(self, node, indent, last):
        if node != self.NULLNODE:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = node.color
            print(str(node.key) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def get_min_node(self, root):
        while root.left != self.NULLNODE:
            root = root.left
        return root

    def get_max_node(self, root):
        while root.right != self.NULLNODE:
            root = root.right
        return root


if __name__ == "__main__":
    bst = RedBlack()

    bst.insert(55)
    bst.insert(40)
    bst.insert(65)
    bst.insert(60)
    bst.insert(75)
    bst.insert(57)
    bst.insert(11)
    bst.insert(30)
    bst.insert(19)

    assert bst.get_max_node(bst.root).key == 75
    assert bst.get_min_node(bst.root).key == 11

    bst.print_tree()
    
    print("\nAfter deleting an element")
    bst.delete(55)
    bst.delete(40)
    bst.delete(75)
    bst.delete(11)
    bst.delete(19)
    bst.print_tree()