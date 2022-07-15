# TLE
import sys

from collections import defaultdict

N,K = [int(d) for d in sys.stdin.readline().rstrip().split()]

adj = defaultdict(dict)
for _ in range(N-1):
    s,e,l  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[s].update({e:l})
    adj[e].update({s:l})

def get_size(root):
    stack = [root]
    visited = set()
    marked = set([root])
    while stack:
        node = stack.pop()
        list_neighbors = [ne for ne in adj[node] if ne not in marked]
        if len(list_neighbors)==0:
            if node in visited: # intermediate node
                list_size[node] = 1 + sum([list_size[ne] for ne in adj[node]])
            else: # leaf node
                list_size[node] = 1
        else:
            stack.append(node) # push node at first visit of the intermediate node
            # push neighbors
            for ne in list_neighbors:
                if ne not in marked:
                    stack.append(ne)
                    marked.add(ne)
            visited.add(node)

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


def find_centroid(root, n_nodes):
    stack = [root]
    marked = set([root])
    while stack:
        node = stack.pop()
        for ne in adj[node]:
            if ne not in marked and list_size[ne]*2 > n_nodes:
                marked.add(ne)
                stack.append(ne)
    return node

list_size = [0]*N
ans = N
q = [0]
while q:
    s = q.pop()
    get_size(s)
    c = find_centroid(s, list_size[s])
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