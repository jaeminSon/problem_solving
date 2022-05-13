def solution(n):
    
    arr = [[0]*201 for _ in range(21)]
    
    for i in range(3, 201):
        arr[2][i] = (i+1) // 2 - 1

    n_stairs = int((2*n)**(1./2))
    for i in range(3, n_stairs+1):
        for t in range(i, n+1):
            for k in range(1, t//i+1):
                arr[i][t] += arr[i-1][t-i*k]

    return sum([arr[i][n] for i in range(21)])


if __name__ =="__main__":
    assert solution(5)==2
    assert solution(200)==487067745
    assert solution(3)==1
    