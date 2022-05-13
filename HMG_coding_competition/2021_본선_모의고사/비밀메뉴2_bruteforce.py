import sys
import time

# st = time.time()

N, M, K = [int(el) for el in sys.stdin.readline().split()]

list_first = [int(el) for el in sys.stdin.readline().split()]
list_second = [int(el) for el in sys.stdin.readline().split()]
sys.stdin.readline()

set_seq = set()
n_first = len(list_first)
n_second = len(list_second)

for i in range(n_first):
    seq = (list_first[i], )
    set_seq.add(seq)
    for j in range(i+1, n_first):
        st = time.time()
        seq = seq + (list_first[j],)
        print("seq increase: {}".format(time.time() - st))
        st = time.time()
        set_seq.add(seq)
        print("add: {}".format(time.time() - st))

len_best = 0
for i in range(n_second):
    seq = (list_second[i], )
    if seq in set_seq:
        len_best = 1

for i in range(n_second):
    seq = (list_second[i], )
    for j in range(i+1, n_second):
        seq = seq + (list_second[j],)
        if seq in set_seq:
            if len_best < j - i + 1:
                len_best = j - i + 1

print(len_best)

# print("total: {}".format(time.time() - st))

