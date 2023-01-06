import sys
from collections import defaultdict

N,K = [int(d) for d in sys.stdin.readline().rstrip().split()]

# no weight (uniform weight)
adj = defaultdict(dict)
for _ in range(N-1):
    s,e  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[s].update({e:1})
    adj[e].update({s:1})

# with weight
adj = defaultdict(dict)
for _ in range(N-1):
    s,e,l  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[s][e] = l
    adj[e][s] = l

# remove edges
for ne in adj[node]:
    del adj[ne][node]
del adj[node]

# convert list -> dict of set
adj = defaultdict(set)
for i, neighbors in enumerate(adjacency_list):
    adj[i].update(neighbors)
    for ne in neighbors:
        adj[ne].add(i)
    