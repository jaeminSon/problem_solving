from collections import defaultdict


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
        if all([self._in[v]==self._out[v] for v in self._in.keys()]):
            self.dfs(next(iter(self._in)))
            return self.path[::-1]
        
        elif sum([self._in[v] == self._out[v] + 1 for v in self._in.keys()])==1 and \
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
                if not self.directed_edges:
                    self.g[ne][v] -= 1
                self.dfs(ne)
        self.path.append(v)
        
def get_Eulerian_path(g:defaultdict):
    """get eulerian path with loop (without recursion)
    """
    N = len(g.keys())
    
    # remove edges with 0 
    for i in range(N):
        remove = []
        for j in g[i]:
            if g[i][j] == 0:
                remove.append(j)
        for j in remove:
            del g[i][j]
    
    degree = {i:sum(g[i].values()) for i in range(N)}
    
    def _find_cycle():
        cycle = []
        stack = [next(iter(degree))]
        dict_repetitive = defaultdict(list)
        while stack:
            v = stack[-1]
            if sum(g[v].values()) == 0:
                cycle.append(v)
                
                # append repetitive cycles to node once
                cycle += dict_repetitive[v]
                del dict_repetitive[v]
                
                stack.pop()
            else:
                i = next(iter(g[v]))
                
                # save alternate paths
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
    
    elif sum([d%2==1 for d in degree.values()])==2 and sum([d%2==0 for d in degree.values()]) == N-2:
        s, e = [v for v, d in degree.items() if d%2==1]
        g[s][e] = g[s].get(e, 0) + 1
        g[e][s] = g[e].get(s, 0) + 1
        cycle = _find_cycle()
        for i in range(len(cycle)-1):
            if (cycle[i]==s and cycle[i+1]==e) or (cycle[i]==e and cycle[i+1]==s):
                return cycle[i+1:]+cycle[:i]
    
    else:
        raise ValueError("No Eulerian path exists.")

        
if __name__ == "__main__":
    assert EulerianPath({0:{1:1}, 1:{2:1}, 2:{}}, True).get_Eulerian_path() == [0,1,2]
    
    g = defaultdict(dict)
    g[0][1] = g[1][0] = g[1][2] = g[2][1]= 1
    assert get_Eulerian_path(g) == [2,1,0]
