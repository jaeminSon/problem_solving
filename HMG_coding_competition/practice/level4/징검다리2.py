import sys
import bisect

N = int(sys.stdin.readline().rstrip())
list_height = [int(el) for el in sys.stdin.readline().split()]

list_height_reverse  = list_height[::-1]

def get_max_jump(l):
    stack = []
    list_max_jump = []
    for el in l:
        if not stack or stack[-1] < el:
            stack.append(el)
            max_jump = len(stack)
        else:
            index_replace = bisect.bisect_left(stack, el)
            stack[index_replace] = el
            max_jump = index_replace + 1
            
        list_max_jump.append(max_jump)
    
    return list_max_jump

list_max_jump_left_to_right = get_max_jump(list_height)
list_max_jump_right_to_left = get_max_jump(list_height_reverse)
list_solution = []
for i in range(N):
    list_solution.append(list_max_jump_left_to_right[i] + list_max_jump_right_to_left[N-1-i] - 1)

print(max(list_solution))