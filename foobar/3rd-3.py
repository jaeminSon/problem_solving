def solution(x, y):
    # Your code here
    x_int = int(x)
    y_int = int(y)
    if x_int > y_int:
        bigger, smaller = x_int, y_int
    else:
        bigger, smaller = y_int, x_int
    
    count = 0
    while smaller!=0:
        n_replicates = bigger // smaller
        remainder = bigger % smaller
        bigger, smaller = smaller, remainder
        count+=n_replicates
    
    if bigger != 1:
        return "impossible"
    else:
        count-=1
    
    return str(count)
    
print(solution('1', '1'))
print(solution('4', '7'))
print(solution('2', '1'))
print(solution('2', '4'))
print(solution('1000000000000000000000000000000000000000000000000000000000000', '3'))
