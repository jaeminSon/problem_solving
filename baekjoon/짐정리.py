import sys

N = int(sys.stdin.readline().rstrip())

w = [int(sys.stdin.readline().rstrip()) for _ in range(N)]
sorted_w = sorted(w)

marked = set()
l = []
for i in range(N):
    for j in range(N):
        if w[i]==sorted_w[j] and j not in marked:
            l.append(j)
            marked.add(j)
            break

l_cycle = []
set_sorted = set()
for i in range(N):
    if not (i in set_sorted):
        set_cycle = set()
        curr = i
        while curr not in set_cycle:
            set_cycle.add(curr)
            curr = l[curr]
        weights = [w[i] for i in set_cycle]
        l_cycle.append(weights)
        set_sorted = set_sorted.union(set_cycle)

ans = sum(w)
min_w = min(w)
for cycle in l_cycle:
    if min_w not in cycle:
        min_cycle = min(cycle)
        delta_exchange = min_w*len(cycle) + min_w + min_cycle
        delta_asis = min_cycle*(len(cycle)-2)
        if delta_exchange < delta_asis: # (1,2) + (3,4) => (1,2,3,4)
            ans += delta_exchange
        else:
            ans += delta_asis
    else:
        ans += min_w*(len(cycle)-2)

print(ans)