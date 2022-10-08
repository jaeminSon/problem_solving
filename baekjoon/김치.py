import sys

N,D  = [int(d) for d in sys.stdin.readline().rstrip().split()]

T = [int(d) for d in sys.stdin.readline().rstrip().split()]
V = [int(d) for d in sys.stdin.readline().rstrip().split()]

ans = 0

def recursive(s, e, l, r):
    global ans

    if s > e:
        return
    else:
        # set value for mid position
        mid = (s+e)//2
        opt_k = max(l, mid-D)
        max_val = 0
        for i in range(opt_k, min(r+1, mid+1)): 
            val = (mid-i)*T[mid]+V[i]
            if max_val < val:
                opt_k = i
                max_val = val

        ans = max(ans, max_val)

        recursive(s, mid-1, l, opt_k)
        recursive(mid+1, e, opt_k, r)

recursive(0, N-1, 0, N-1)

print(ans)