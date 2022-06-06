class SqrtDecomposition:
    
    def __init__(self, arr) -> None:
        self.n = len(arr)
        self.arr = arr
        self.block_size = int(self.n**(1./2))
        self.block = [0] * self.n
    
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
        
        
if __name__=="__main__":

    sqrt_decomposition = SqrtDecomposition([1, 5, 2, 4, 6, 1, 3, 5, 7, 10])
    
    assert sqrt_decomposition.query(3, 8) == 26
    assert sqrt_decomposition.query(1, 6) == 21
    sqrt_decomposition.update(8, 0)
    assert sqrt_decomposition.query(8, 8)==0