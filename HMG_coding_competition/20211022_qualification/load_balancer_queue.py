import sys
from queue import Queue

N, K = [int(el) for el in sys.stdin.readline().split()]

list_node = []
for _ in range(N):
    row = [int(el) for el in sys.stdin.readline().split()]
    n_ch = row[0]
    list_ch = [el-1 for el in row[1:]]
    list_node.append((n_ch, list_ch))
dict_parent = {i:set() for i in range(N)}
for index, el in enumerate(list_node):
    _, list_ch = el
    for ch in list_ch:
        dict_parent[ch].add(index)

q = Queue()
q.put(0)
call = [K] + [0]*(N-1)
set_conquered = set()
while not q.empty():
    curr = q.get()
    if curr not in set_conquered:
        set_conquered.add(curr)
        n_ch = list_node[curr][0]
        list_ch = list_node[curr][1]
        for ch in list_ch:
            call[ch] += call[curr] // n_ch
        for i in range(call[curr] % n_ch):
            call[list_ch[i]] += 1
        for ch in list_ch:
            if list_node[ch][0]!=0 and dict_parent[ch].issubset(set_conquered):
                q.put(ch)

print(" ".join([str(d) for d in call]))