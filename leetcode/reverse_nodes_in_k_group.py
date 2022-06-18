from typing import List, Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        
        remain = 0
        while head is None:
            remain+=1
            head = head.next
        
        q = []
        curr = dummy = ListNode()
        while remain >= k:
            for _ in range(k):
                q.append(head)
                head = head.next
            while q:
                node = q.pop()
                curr.next = node
                curr = node
            
            remain -= k
            
        return dummy.next