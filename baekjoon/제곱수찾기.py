import sys

N, M = [int(d) for d in sys.stdin.readline().rstrip().split()]

l = [[] for _ in range(N)]
for i in range(N):
    line = sys.stdin.readline().rstrip()
    for d in line:
        l[i].append(int(d))

def is_square(val):
    return int(val**(1./2)+0.5)**2 == val

C = max(N, M)
ans = -1
for di in range(-N, N):
    for dj in range(-M, M):
        for si in range(N):
            for sj in range(M):
                if not (di==0 and dj==0):
                    digit = ""
                    for c in range(C):
                        if si+di*c>=0 and si+di*c<N and sj+dj*c>=0 and sj+dj*c<M:
                            digit += str(l[si+di*c][sj+dj*c])
                            if is_square(int(digit)):
                                ans = max(ans, int(digit))

print(ans)
