def solution(x, y):
    # Your code here
    sum_coord=x+y
    id_last=sum_coord*(sum_coord-1)//2
    stepback=(sum_coord-1)-x
    
    return id_last-stepback

print(solution(1,1))
print(solution(3,2))
print(solution(5,10))
