import sys
from collections import defaultdict

N,K = [int(d) for d in sys.stdin.readline().rstrip().split()]

adj = defaultdict(dict)
for _ in range(N-1):
    s,e,l  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[s].update({e:l})
    adj[e].update({s:l})

# remove edges
for ne in adj[node]:
    del adj[ne][node]
del adj[node]
