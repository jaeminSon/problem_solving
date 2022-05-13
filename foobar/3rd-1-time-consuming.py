def solution(l):
    # Your code here
    def gdc(bigger,smaller):
        remainder = bigger%smaller
        if remainder==0:
            return smaller
        return gdc(smaller,remainder)
    
    l_sorted = sorted(l)
    length = len(l_sorted)
    
    count = 0
    for i in range(1, length):
        for j in range(i+1, length):
            if l[j] % l[i] == 0:
                cand_max = gdc(l_sorted[j], l_sorted[i])
                for index_cand in range(i):
                    if l[index_cand] > cand_max:
                        break
                    elif cand_max % l[index_cand] == 0:
                        count+=1
            
    return count
    
print(solution([1,1,1]))
print(solution([1, 2, 3, 4, 5, 6]))
