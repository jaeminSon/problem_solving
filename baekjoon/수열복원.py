import sys
from collections import defaultdict

N,M  = [int(d) for d in sys.stdin.readline().rstrip().split()]

g = defaultdict(dict)
seq2node = dict()
node2seq = dict()
in_neighbors = dict()
out_neighbors = dict()
node_index = 0
for _ in range(N-M+1):
    l = tuple(int(d) for d in sys.stdin.readline().rstrip().split())
    s_seq = l[:-1]
    if s_seq not in seq2node:
        node2seq[node_index] = s_seq
        seq2node[s_seq] = node_index
        node_index+=1
    e_seq = l[1:]
    if e_seq not in seq2node:
        node2seq[node_index] = e_seq
        seq2node[e_seq] = node_index
        node_index+=1
    s = seq2node[s_seq]
    e = seq2node[e_seq]
    g[s][e] = g[s].get(e, 0) + 1
    in_neighbors[e] = in_neighbors.get(e, 0) + 1
    in_neighbors[s] = in_neighbors.get(s, 0)
    out_neighbors[e] = out_neighbors.get(e, 0)
    out_neighbors[s] = out_neighbors.get(s, 0) + 1
    
    
class EulerianPath:
    def __init__(self, g:dict, directed_edges=True):
        self.g = g
        self._in = defaultdict(int)
        self._out = defaultdict(int)
        
        nodes = set(g.keys()).union(set([v for e in g for v in g[e]]))
        
        for v in nodes:
            self._in[v] = sum([g[j][v] for j in g if v in g[j]])
        for v in nodes:
            self._out[v] = sum(g[v].values())
        self.directed_edges = directed_edges
        self.path = []
        
    def get_Eulerian_path(self):
        if sum([self._in[v] == self._out[v] + 1 for v in self._in.keys()])==1 and \
             sum([self._in[v] + 1 == self._out[v] for v in self._in.keys()])==1 and \
             sum([self._in[v] == self._out[v] for v in self._in.keys()]) == len(self._in.keys())-2:
            
            self.dfs([v for v in self._in.keys() if self._in[v] + 1 == self._out[v]][0])
            return self.path[::-1]
        else:
            raise ValueError("No Eulerian path exists.")

    
    def dfs(self, v):
        for ne in self.g[v]:
            if self.g[v][ne] > 0:
                self.g[v][ne] -= 1
                self.dfs(ne)
        self.path.append(v)


eulerian = EulerianPath(g)
path = eulerian.get_Eulerian_path()

ans = list(node2seq[path[0]])
for i in range(1, len(path)):
    ans.append(node2seq[path[i]][-1])

print(" ".join([str(e) for e in ans]))
