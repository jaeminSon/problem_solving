import sys

list_numbers = [int(d) for d in sys.stdin.readline().rstrip().split()]

def massage(l):
    while (sum(l)+1)//2 < max(l):
        i = max(range(10), key=lambda i:list_numbers[i])
        list_numbers[i]-=1
    return l

def avail(x, pos):
    if list_numbers[x]<=0:
        return False
    
    if len(val)>0 and int(val[-1])==x:
        return False
    
    list_numbers[x] -= 1
    index = max(range(10), key=lambda i:list_numbers[i])
    max_count = list_numbers[index] 
    list_numbers[x] += 1
    
    return max_count <= pos // 2

if list_numbers[0]>=0 and all([list_numbers[i]==0 for i in range(1, 10)]):
    print(0)
else:
    list_numbers = massage(list_numbers)
    pos = sum(list_numbers)
    val = ""
    while pos > 0:
        for x in range(9, -1, -1):
            if avail(x, pos):
                list_numbers[x] -= 1
                pos -= 1
                val+=str(x)
                break
            

    print(int(val))
