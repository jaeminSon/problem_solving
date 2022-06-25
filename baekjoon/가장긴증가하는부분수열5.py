import sys
import bisect

N = int(sys.stdin.readline().rstrip())
list_height = [int(el) for el in sys.stdin.readline().split()]

d = [-1]*N
stack = []
max_len = 0
for i, height in enumerate(list_height):
    if not stack or height > stack[-1]:
        stack.append(height)
        max_len = len(stack)
        d[i] = len(stack)
    else:
        index_insert = bisect.bisect_left(stack, height)
        stack[index_insert] = height
        d[i] = index_insert + 1

print(max_len)
backward_step = []
for i in range(N-1, -1, -1):
    if d[i] == max_len:
        backward_step.append(list_height[i])
        max_len-=1
print(" ".join([str(el) for el in backward_step][::-1]))