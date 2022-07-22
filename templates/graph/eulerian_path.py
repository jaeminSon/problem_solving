class EulerianPath:
    def __init__(self, g:dict, _in:dict, _out:dict):
        assert set(_in.keys()) == set(_out.keys())
        self.g = g
        self._in = _in
        self._out = _out
        self.path = []
        
    def get_Eulerian_path(self):
        if all([self._in[v]==self._out[v] for v in self._in.keys()]):
            self.dfs(self._in.keys()[0])
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
                self.dfs(ne)
        self.path.append(v)
        
        
if __name__ == "__main__":
    assert EulerianPath({0:{1:1}, 1:{2:1}, 2:{}}, {0:0, 1:1, 2:1}, {0:1, 1:1, 2:0}).get_Eulerian_path() == [0,1,2]