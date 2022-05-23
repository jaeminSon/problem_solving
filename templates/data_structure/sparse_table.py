import math
 
def build_sparse_table(arr):
    n = len(arr)
    sparse_table = [[0]*int(math.log2(n)+1) for _ in range(n)]
    for i in range(n):
        sparse_table[i][0] = arr[i]
     
    j = 1
    while (1 << j) <= n:
        i = 0
        while i + (1 << j) - 1 < n:
            # min in [i, i+2^j-1] = min(min in [i,i+2^(j-1)-1], min in [i+2^(j-1), i+2^j-1])
            sparse_table[i][j] = min(sparse_table[i][j - 1], sparse_table[i + (1 << (j - 1))][j - 1])
            i += 1
        j += 1       
    
    return sparse_table

def query(sparse_table, L, R):
    # min range in [L, R] (both sides inclusive)
    j = int(math.log2(R - L + 1))
    return min(sparse_table[L][j], sparse_table[R - (1 << j) + 1][j])
 
if __name__ == "__main__":
    arr = [7, 2, 3, 0, 5, 10, 3, 12, 18]
    sparse_table = build_sparse_table(arr)
    print(query(sparse_table, 0, 4))
    print(query(sparse_table, 4, 7))
    print(query(sparse_table, 7, 8))