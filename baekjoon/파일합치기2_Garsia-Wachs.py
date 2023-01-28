import sys

arr = [0] * 5003
w = [0] * 5003

def insert(c,e):
    # add c to cost and remove arr[e] and arr[e-1] 
    global ans
    global st

    ans += c
    st-=1
    
    # move elements [e+1, st+1] to left by 1
    for i in range(e, st+1):
        arr[i] = arr[i+1]
	# find index s.t. c<=arr[index] and move elements [index+1, e-2] to right by 1 and set arr[index+1]=c
    for i in range(e-2, -1,-1):
        if c<=arr[i]:
            arr[i+1]=c
            break
        arr[i+1] = arr[i]
	# recursively insert when arr[i-1] <= arr[i+1]
    while i > 1 and arr[i - 1] <= c: # invariant: arr[i+1]==c
        d = st - i
        insert(arr[i - 1] + arr[i], i)
        i = st - d

T = int(sys.stdin.readline().rstrip())
for _ in range(T):
    m = int(sys.stdin.readline())
    w[0] = 100000001
    w[m + 1] = 100000000
    for i,d in enumerate(sys.stdin.readline().rstrip().split()):
        w[i+1] = int(d)
    
    arr[1]=w[0]
    arr[2]=w[1]
    st = 2
    
    ans = 0
    for i in range(2, m+2):
        while arr[st - 1] <= w[i]:
            insert(arr[st - 1] + arr[st], st) # add arr[size(stack)-1] and arr[size(st)] and update size(stack)
        st+=1
        arr[st] = w[i]
        
    print(ans)