MOD = 998_244_353

class SegmentTreeLazyPropagation:
    def __init__(self, arr):
        
        self.power = [1]
        for _ in range(1_000_010):
            self.power.append((self.power[-1] * 10) % MOD)

        N = len(arr)
        self.tree = [[0] * 10 for _ in range(2 * self.just_bigger_power_2(N))] 
        self.lazy = [list(range(10)) for _ in range(2 * self.just_bigger_power_2(N))] 
        self.len = N
        self.initialize(arr, 0, N-1, 0)
        
    def just_bigger_power_2(self, val):
        i=0
        while 2**i < val:
            i+=1
        return 2**i

    def initialize(self, arr, s, e, index):
        if s <= e:
            if s == e: # leaf node
                self.tree[index][arr[s]] = 1
            else:
                mid = (s + e) // 2 
                self.initialize(arr, s, mid, index * 2 + 1) 
                self.initialize(arr, mid + 1, e, index * 2 + 2)
                for i in range(10):
                    self.tree[index][i] = (self.power[e - mid] * self.tree[index * 2 + 1][i] + self.tree[index * 2 + 2][i]) % MOD
            
    def update(self, s, e, fr, to):
        self.update_util(0, 0, self.len - 1, s, e, fr, to)
    
    def propagate(self, node_index, node_s, node_e):
        if any(self.lazy[node_index][i] != i for i in range(10)):
            target = [0] * 10
            for i in range(10):
                target[self.lazy[node_index][i]] = (target[self.lazy[node_index][i]] + self.tree[node_index][i]) % MOD
            for i in range(10):
                self.tree[node_index][i] = target[i]
            if node_s != node_e:
                for ch in [node_index * 2 + 1, node_index * 2 + 2]:
                    for i in range(10):
                        self.lazy[ch][i] = self.lazy[node_index][self.lazy[ch][i]]
            for i in range(10):
                self.lazy[node_index][i] = i
    
    def update_util(self, node_index, node_s, node_e, s, e, fr, to):
        self.propagate(node_index, node_s, node_e)
        
        if node_s <= node_e and node_s <= e and node_e >= s:
            if node_s >= s and node_e <= e: # [node_s, node_e] in [s,e]
                self.lazy[node_index][fr] = to
                self.propagate(node_index, node_s, node_e)
            else: # [node_s, node_e] and [s,e] overlapping but not inclusive
                mid = (node_s + node_e) // 2 
                self.update_util(node_index * 2 + 1, node_s, mid, s, e, fr, to) 
                self.update_util(node_index * 2 + 2, mid + 1, node_e, s, e, fr, to) 
                for i in range(10):
                    self.tree[node_index][i] = (self.power[node_e - mid] * self.tree[node_index * 2 + 1][i] + self.tree[node_index * 2 + 2][i]) % MOD
            
    def query_util(self, node_index, node_s, node_e, s, e):
        self.propagate(node_index, node_s, node_e)

        if node_s <= node_e and node_s <= e and node_e >= s:        
            if node_s >= s and node_e <= e: # [node_s, node_e] in [s,e]
                ret = 0
                for i in range(10):
                    ret = (ret + self.tree[node_index][i] * i) % MOD
                return ret
            else: # [node_s, node_e] and [s,e] overlapping but not inclusive
                mid = (node_s + node_e) // 2
                if e >= mid+1:
                    return (self.power[min(node_e, e)-mid] * self.query_util(2 * node_index + 1, node_s, mid, s, e) + self.query_util(2 * node_index + 2, mid + 1, node_e, s, e)) % MOD
                else:
                    return self.query_util(2 * node_index + 1, node_s, mid, s, e) % MOD
        else:
            return 0
        
    def query(self, s, e):
        return self.query_util(0, 0, self.len-1, s, e)

S = input().rstrip()
segtree = SegmentTreeLazyPropagation([int(i) for i in list(S)])

Q = int(input().rstrip())
for _ in range(Q):
    row = list(map(int, input().split()))
    if row[0] == 1:
        i, j, f, t = row[1:]
        segtree.update(i-1, j-1, f, t)
    elif row[0] == 2:
        i, j = row[1:]
        ans = segtree.query(i-1, j-1)
        print(ans)
