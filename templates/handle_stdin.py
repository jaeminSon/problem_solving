import sys

# single line integer
N = int(sys.stdin.readline().rstrip())

# multi-line problems
problems = [sys.stdin.readline().rstrip() for _ in range(N)]

###################
##### integer #####
###################

# multiple integers in one line
l = [int(d) for d in sys.stdin.readline().rstrip().split()]

# two integers in one line
m,n  = [int(d) for d in sys.stdin.readline().rstrip().split()]

# three integers in one line
m,n,k  = [int(d) for d in sys.stdin.readline().rstrip().split()]

# four integers in one line
m,n,p,q  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    
#################
##### chars #####
#################
# multiple chars in one line
l = [d for d in sys.stdin.readline().rstrip().split()]

# two chars in one line
m,n  = [d for d in sys.stdin.readline().rstrip().split()]

# three chars in one line
m,n,k  = [d for d in sys.stdin.readline().rstrip().split()]

# four chars in one line
m,n,p,q  = [d for d in sys.stdin.readline().rstrip().split()]
    
