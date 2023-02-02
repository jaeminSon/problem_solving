class SqrtDecomposition:
    
    def __init__(self, arr) -> None:
        self.n = len(arr)
        self.arr = arr
        self.block_size = int(self.n**(1./2))
        self.block = [0] * (self.n // self.block_size + 1)
    
        # O(n)
        for i in range(self.n):
            self.block[i // self.block_size] += self.arr[i]
 
        
    def update(self, idx, val):
        # O(1)
        self.block[idx // self.block_size] += val - self.arr[idx]
        self.arr[idx] = val
    
    def query(self, l, r):
        # O(sqrt(n))
        sum = 0
        while l < r and l % self.block_size != 0:
            # pre-block
            sum += self.arr[l]
            l += 1
        
        while l + self.block_size - 1 <= r:
            # blocks
            sum += self.block[l//self.block_size]
            l += self.block_size
        
        while (l <= r):
            # post-block
            sum += self.arr[l]
            l += 1
        
        return sum


class SqrtDecompositionSearchNonZero:
    
    def __init__(self, arr) -> None:
        self.n = len(arr)
        self.arr = arr # distribution
        self.block_size = int(self.n**(1./2))
        self.block = [0] * (self.n // self.block_size + 1)
    
        # O(n)
        for i in range(self.n):
            self.block[i // self.block_size] += self.arr[i]
  
    def increment(self, idx, val):
        # O(1)
        self.block[idx // self.block_size] += val
        self.arr[idx] += val
    
    def query(self):
        # O(sqrt(n))
        for i in range(len(self.block)-1, -1, -1):
            if self.block[i] > 0:
                for j in range(self.block_size, -1, -1):
                    if self.arr[i*self.block_size + j] > 0:
                        return i*self.block_size + j
        
if __name__=="__main__":

    sqrt_decomposition = SqrtDecomposition([1, 5, 2, 4, 6, 1, 3, 5, 7, 10])
    
    assert sqrt_decomposition.query(3, 8) == 26
    assert sqrt_decomposition.query(1, 6) == 21
    sqrt_decomposition.update(8, 0)
    assert sqrt_decomposition.query(8, 8)==0

    sqrt_decomposition_nonzero = SqrtDecompositionSearchNonZero([1, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    sqrt_decomposition_nonzero.query() == 2
    sqrt_decomposition_nonzero.increment(3, 4)
    sqrt_decomposition_nonzero.query() == 3
