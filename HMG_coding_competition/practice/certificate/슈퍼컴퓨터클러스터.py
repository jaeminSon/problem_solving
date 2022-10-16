import sys

N,B  = [int(d) for d in sys.stdin.readline().rstrip().split()]
l = [int(d) for d in sys.stdin.readline().rstrip().split()]

lo, hi = 0, 10**18
while lo <= hi:
    mid = (lo + hi) // 2
    cost = sum([(el-mid)**2 if el<mid else 0 for el in l])
    if cost <= B:
        lo = mid + 1
    else:
        hi = mid - 1

print(lo-1)