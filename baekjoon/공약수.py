import sys

N = int(sys.stdin.readline().rstrip())

MAX = 50_001

def set_mobius():
    mobius = [0]*MAX
    mobius[1]=1
    for i in range(2, MAX):
        if mobius[i] == 0: # not visited (prime)
            for j in range(i, MAX, i):
                mobius[j]+=1
            for j in range(i**2, MAX, i**2):
                mobius[j]=float('inf')
    
    for i in range(2, MAX):
        if mobius[i]==float('inf'):
            mobius[i]=0
        elif mobius[i] & 1 == 1:
            mobius[i]=-1
        elif mobius[i] & 1 == 0:
            mobius[i]=1
        else:
            raise ValueError("should not enter this condition.")
    
    return mobius
    
mobius = set_mobius()
prefix_mobius = [0]*len(mobius)
for i in range(1, len(mobius)):
    prefix_mobius[i] = prefix_mobius[i-1]+mobius[i]
    
for _ in range(N):
    a,b,d = [int(d) for d in sys.stdin.readline().rstrip().split()]
    a_prime = a//d
    b_prime = b//d
    m = min(a_prime, b_prime)
    
    ans = 0
    
    i=1
    while i<=m:
        j_a = a_prime//(a_prime//i)
        j_b = b_prime//(b_prime//i)
        j = min(j_a, j_b)
        ans+=(prefix_mobius[j]-prefix_mobius[i-1])*(a_prime//i)*(b_prime//i)
        i = j+1
    
    print(ans)