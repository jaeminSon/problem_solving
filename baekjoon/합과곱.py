import sys

S, P = [int(d) for d in sys.stdin.readline().rstrip().split()]

if S == P:
    print(1)
else:
    for i in range(2, 31): # 1,000,000,000 < 2**30
        if S**i >= P*(i**i):
            print(i)
            exit(0)
    print(-1)