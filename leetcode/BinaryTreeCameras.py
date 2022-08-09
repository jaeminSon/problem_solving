# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minCameraCover(self, root) -> int:
        def dp(root, depth):
            if root is None:
                return False, True, 0 # install, cover, n

            if root.left is None and root.right is None: # no children
                if depth == 0: # root node only
                    return True, True, 1
                else: # leaf node
                    return False, False, 0
            else:
                if root.left:
                    install_left, cover_left, n_left = dp(root.left, depth+1)
                else:
                    install_left, cover_left, n_left = False, True, 0

                if root.right:
                    install_right, cover_right, n_right = dp(root.right, depth+1)
                else:
                    install_right, cover_right, n_right = False, True, 0

                if (not cover_left) or (not cover_right): # any of children not covered, node should be installed
                    return True, True, n_left+n_right+1
                else: # both children covered (node need not be installed)
                    if (not install_left) and (not install_right):
                        if depth==0: # root should be installed if both children are not installed
                            return True, True, n_left+n_right+1
                        else: # push to root
                            return False, False, n_left+n_right
                    else:
                        return False, True, n_left+n_right
                
        return dp(root, 0)[-1]