# memory (seg fault due to recursion)
import sys
sys.setrecursionlimit(10**6)

from collections import defaultdict

N,K = [int(d) for d in sys.stdin.readline().rstrip().split()]

adj = defaultdict(dict)
for _ in range(N-1):
    s,e,l  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[s].update({e:l})
    adj[e].update({s:l})

def get_size(node, parent):
    list_size[node] = 1
    for ne in adj[node]:
        if ne != parent:
            list_size[node] += get_size(ne, node)
    return list_size[node]

def get_min_dist(node):

    def get_min_dist_branch(node, depth, length):
        d = defaultdict(int)
        q = [(node, depth, length)]
        while q:
            curr, depth, length = q.pop()
            if curr not in visited:
                visited.add(curr)
                d[length] = min(d[length], depth) if length in d else depth
                for ne in adj[curr]:
                    if ne != curr:
                        q.append((ne, depth+1, length+adj[curr][ne]))
        return d
    
    min_dist = N
    visited = set([node])
    prev = defaultdict(int, {0:0})
    for ne in adj[node]:
        curr = get_min_dist_branch(ne, 1, adj[node][ne])
        for v in curr:
            if K-v in prev:
                min_dist = min(min_dist, curr[v]+prev[K-v])
        for v in curr:
            prev[v] = min(prev[v], curr[v]) if v in prev else curr[v]
    return min_dist


def get_centroid(node, parent, n):
    if len(adj[node]) == 0:
        return None
    else:
        for ne in adj[node]:
            if ne != parent and list_size[ne]*2 > n:
                return get_centroid(ne, node, n)
        return node

list_size = [0]*N
get_size(0,-1)

ans = N
q = [0]
while q:
    s = q.pop()
    get_size(s,-1)
    c = get_centroid(s, -1, list_size[s])
    if c is not None:
        ans = min(ans, get_min_dist(c))
        for ne in adj[c]:
            q.append(ne)
            del adj[ne][c]
        del adj[c]

if ans == N:
    print(-1)
else:
    print(ans)