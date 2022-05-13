from collections import Counter

def solution(data, n): 
    list_res = []
    c = Counter(data)
    for el in data:
        if c[el]<=n:
            list_res.append(el)
    
    return list_res
        
        
if __name__ == "__main__":
    print(solution([1, 2, 3], 0))
    # 

    print(solution([1, 2, 2, 3, 3, 3, 4, 5, 5], 1))
    # 1,4
