import sys
import bisect


N  = int(sys.stdin.readline().rstrip())

fib = [1, 2]
while fib[-1] < 10**15:
    fib.append(fib[-1]+fib[-2])

if N in fib:
    print(-1)
else:
    val = N
    while val not in fib:
        i = bisect.bisect_left(fib, val)
        val -= fib[i-1]
        
    print(val)

        
