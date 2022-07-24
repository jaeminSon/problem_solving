import sys

K, M = [int(d) for d in sys.stdin.readline().rstrip().split()]

if M == 1:
    print(" ".join([str(el) for el in range(K)]))
else:
    s = 0
    msb = K**(M-1)
    start = [0] * msb
    start[0] = 1
    
    skip_count = 0
    
    stack = [s]
    while stack:
        v = stack[-1]
        lsb = v % msb
        if start[lsb]==K:
            if len(stack) == 1: # last element
                for _ in range(M):
                    print(v % K, end=" ")
                    v //= K
            else:
                if skip_count == M-1:
                    print(v % K, end=" ")
                else:
                    skip_count+=1    
            stack.pop()
        else:
            next_el = start[lsb]
            start[lsb]+=1
            stack.append(lsb*K + next_el)
    
