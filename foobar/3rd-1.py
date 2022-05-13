def solution(l):
    # Your code here
    length = len(l)
    indices_divisible = [[] for _ in range(length)]
    for i in range(length):
        for j in range(i):
            if l[i] % l[j] == 0:
                indices_divisible[i].append(j)
            
    count = 0
    for i in range(2, length):
        for index_middle in indices_divisible[i]:
            count+=len(indices_divisible[index_middle])
            # print(index_smallest, index_middle, i)
    return count
    

print(solution([1]*2000))
# import numpy as np
# print(solution(list(np.random.randint(1_000_000, size=2000))))
print(solution([1,1]))
print(solution([1,1,1]))
print(solution([1, 2, 3, 4, 5, 6]))
