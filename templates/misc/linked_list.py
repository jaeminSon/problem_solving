class BidirectionalLinkedList:
    def build_bidirectional_linked_list(self, arr):
        self.left = [0] * len(arr)
        self.right = [0] * len(arr)
        for i in len(arr):
            self.left[i] = i-1
            self.right[i] = i+1
    
    def remove(self, l, r):
        # remove l and r from the linked list
        self.right[self.left[l]] = self.right[r]
        self.left[self.right[r]] = self.left[l]

def index_prev_occurrence(arr):
    prev = []
    v2i = {}
    for i, v in enumerate(arr):
        if v in v2i:
            prev.append(v2i[v])
        else:
            prev.append(-1)
        v2i[v] = i
    return prev