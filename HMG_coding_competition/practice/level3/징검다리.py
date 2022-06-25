import sys
import bisect

N = int(sys.stdin.readline().rstrip())
list_height = [int(el) for el in sys.stdin.readline().split()]

stack = []
max_jump = 0
for height in list_height:
    if not stack or height > stack[-1]:
        stack.append(height)
        max_jump = len(stack)
    else:
        index_insert = bisect.bisect_left(stack, height)
        stack[index_insert] = height

print(max_jump)