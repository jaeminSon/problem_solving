import sys
from queue import PriorityQueue

N, M = [int(el) for el in sys.stdin.readline().split()]

INF = 1_000_000_001

list_level = [[] for _ in range(N)]
for _ in range(M):
    start, end, level = [int(el) for el in sys.stdin.readline().split()]
    list_level[start-1].append((level, end-1))
    list_level[end-1].append((level, start-1))

list_required_level = [INF for _ in range(N)]
queue = PriorityQueue()
queue.put((0,0))
while list_required_level[N-1] == INF:
    required_level, index_cand = queue.get()
    if list_required_level[index_cand] == INF:
        list_required_level[index_cand] = required_level
        for level, target in list_level[index_cand]:
            required_level = max(level, list_required_level[index_cand])
            queue.put((required_level, target))

def isprime(value):
    if value < 2 or value % 2 == 0:
        return False
    else:
        for denom in range(3, int(value**(1/2))+2,2):
            if value % denom == 0:
                return False
        return True

required_level = list_required_level[N-1] + 1
while not isprime(required_level):
    required_level+=1

print(required_level)