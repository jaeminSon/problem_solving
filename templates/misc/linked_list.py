
arr = [] # some list

# build_bidirectional_linked_list
left = [0] * len(arr)
right = [0] * len(arr)
for i in len(arr):
    left[i] = i-1
    right[i] = i+1

# remove l and r from the linked list
right[left[l]] = right[r]
left[right[r]] = left[l]