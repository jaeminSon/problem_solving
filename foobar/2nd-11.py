def solution(l, t):
    
    n = len(l)
    
    for s in range(n):
        for e in range(s, n):
            if sum(l[s:e+1]) == t:
                return [s, e]
    
    return [-1,-1]

if __name__ == "__main__":
    print(solution([1, 2, 3, 4], 15))
    # -1,-1

    print(solution([4, 3, 10, 2, 8], 12))
    # 2,3

    print(solution([101]*100, 100))
    
    print(solution([5], 5))
