import sys
from collections import defaultdict

N = int(sys.stdin.readline().rstrip())

g = defaultdict(dict)
degree = defaultdict(int)
for i in range(N):
    row = [int(d) for d in sys.stdin.readline().rstrip().split()]
    for j,v in enumerate(row):
        g[i][j] = g[i].get(j, 0) + v
for i in range(N):
    degree[i] = sum([g[i][j] for j in range(len(g[i]))])

if N==1:
    print(-1)
else:    
    def get_Eulerian_path(g:dict):
        # remove edges with 0 
        for i in range(N):
            remove = []
            for j in g[i]:
                if g[i][j] == 0:
                    remove.append(j)
            for j in remove:
                del g[i][j]
                    
        degree = {}
        for i in range(N):
            degree[i] = sum(g[i].values())

        def _find_cycle():
            cycle = []
            stack = [next(iter(degree))]
            dict_repetitive = defaultdict(list)
            while stack:
                v = stack[-1]
                if sum(g[v].values()) == 0:
                    cycle.append(v)
                    cycle += dict_repetitive[v]
                    del dict_repetitive[v]
                    stack.pop()
                else:
                    i = next(iter(g[v]))
                    if g[v][i] > 2:
                        dec = (g[v][i]-2)//2
                        dict_repetitive[v] += [i, v] * dec
                        g[v][i] -= 2*dec
                        g[i][v] -= 2*dec
                        
                    g[v][i]-=1
                    g[i][v]-=1
                    if g[v][i] == 0:
                        del g[v][i]
                    if g[i][v] == 0:
                        del g[i][v]
                    
                    stack.append(i)
                    
            return cycle

        if all([d%2==0 for d in degree.values()]):
            return _find_cycle()
        else:
            return -1

            
    ans = get_Eulerian_path(g)
    if ans == -1:
        print(-1)
    else:
        print(" ".join([str(el+1) for el in ans]))
        