from collections import deque

class BipartiteGraph(object):
    def __init__(self, adjacency_list):
        self.n_left = len(adjacency_list)
        self.n_right = max([el for l in adjacency_list for el in l]) + 1
        self.adjacency_list = adjacency_list
        
    def hopcroft_karp(self):
        self.matching_from_L2R = [None] * self.n_left
        self.matching_from_R2L = [None] * self.n_right
        self.dist = [None] * self.n_left
    
        result = 0
        while self.bfs():
            for u in range(self.n_left):
                if self.matching_from_L2R[u] is None and self.dfs(u):
                    result+=1
        return result
 
    def bfs(self):
    
        q = deque()
        for u in range(self.n_left):
            if self.matching_from_L2R[u] is None:
                self.dist[u] = 0
                q.append(u)
            else:
                self.dist[u] = None
    
        dist_limit = self.n_left
        while q:
            u = q.popleft()
            if self.dist[u] < dist_limit:
                for v in self.adjacency_list[u]:
                    if self.matching_from_R2L[v] is None:  # no matching from v
                        dist_limit = self.dist[u] + 1
                    elif self.dist[self.matching_from_R2L[v]] is None: # v matched
                        self.dist[self.matching_from_R2L[v]] = self.dist[u] + 1
                        q.append(self.matching_from_R2L[v])

        return dist_limit < self.n_left
    
    def dfs(self, u):
        for v in self.adjacency_list[u]:
            matchable = self.matching_from_R2L[v] is None or \
                (self.matching_from_R2L[v] is not None and self.dist[self.matching_from_R2L[v]] == self.dist[u]+1 and self.dfs(self.matching_from_R2L[v]))
            if matchable:
                self.matching_from_R2L[v] = u
                self.matching_from_L2R[u] = v
                return True
        
        return False

if __name__ == "__main__":
    g = BipartiteGraph([[1,2], [0], [1],[1,3]])
    print(g.hopcroft_karp())