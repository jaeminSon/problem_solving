import sys

N = int(sys.stdin.readline().rstrip())

problems = []
for _ in range(N):
    problems.append(int(sys.stdin.readline().rstrip()))

pow = [1]
for i in range(1,22):
    pow.append(pow[i-1]*3) 

def solve(val, a, b):
    if val==1:
        results.append((a,b))
    elif val % 2==0:
        solve(val//2, a+1, b)
    else:
        i=21
        while pow[i] > val:
            i-=1
        results.append((a,b+i))
        if pow[i]!=val:
            solve(val-pow[i], a, b)
        
for p in problems:
    results = []
    solve(p, 0, 0)
    print(len(results))
    for a,b in results:
        print("{} {}".format(a, b))
    
