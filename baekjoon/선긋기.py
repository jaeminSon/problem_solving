import sys

N = int(sys.stdin.readline().rstrip())

l = [[int(el) for el in sys.stdin.readline().rstrip().split()] for _ in range(N)]

sorted_l = sorted(l, key=lambda x:x[0])

curr_s, curr_e = sorted_l[0]
ans = curr_e - curr_s

for i in range(1, len(sorted_l)):
    s,e = sorted_l[i]
    if s < curr_e < e:
        ans += (e-curr_e)
        curr_e = e
    elif s >= curr_e:
        ans += (e-s)
        curr_s = s
        curr_e = e

print(ans)