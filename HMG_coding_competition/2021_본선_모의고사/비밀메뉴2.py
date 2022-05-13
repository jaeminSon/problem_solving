import sys

N, M, K = [int(el) for el in sys.stdin.readline().split()]

list_first = [int(el) for el in sys.stdin.readline().split()]
list_second = [int(el) for el in sys.stdin.readline().split()]
sys.stdin.readline()

set_seq = set()
n_first = len(list_first)
n_second = len(list_second)

def max_common(i,j,n):
    max_found = 0
    max_len = 0
    for d in range(n):
        if i+d >= len(list_first) or j+d >= len(list_second):
            return max_found
        elif list_first[i+d] == list_second[j+d]:
            max_len += 1
            if max_found < max_len:
                max_found = max_len
        else:
            max_len = 0
    
    return max_found

curr_max = 0
for i in range(n_first-1, -1, -1):
    max_len = max_common(i, 0, n_first-i)
    if max_len > curr_max:
        curr_max = max_len

for i in range(1, n_second):
    print(i)
    max_len = max_common(0, i, n_second-i)
    if max_len > curr_max:
        curr_max = max_len

print(curr_max)