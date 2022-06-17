from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:

        if len(lists) == 0:
            return None
        elif all([l is None for l in lists]):
            return None

        from heapq import heappush, heappop

        front = []
        for i, node in enumerate(lists):
            if node is not None:
                heappush(front, (node.val, i, node))
                lists[i] = lists[i].next
            
        prev = dummy = ListNode()
        while front:
            _, li, next = heappop(front)
            prev.next = next
            prev = next
            if lists[li] is not None:
                heappush(front, (lists[li].val, li, lists[li]))
                lists[li] = lists[li].next
            
        return dummy.next


a = ListNode(1)
b = ListNode(4)
c = ListNode(5)
a.next=b
b.next=c

l = ListNode(2)
m = ListNode(6)
l.next=m
print(Solution().mergeKLists([a,None,l]))

