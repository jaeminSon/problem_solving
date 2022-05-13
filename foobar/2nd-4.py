import math


def solution(total_lambs):
    
    if total_lambs < 3:
        n_max = 2
    else:
        curr_total = 2
        prev = 1
        curr = 1
        n_fib = 0
        while True:
            new_curr = prev + curr
            prev = curr
            curr = new_curr
            curr_total += new_curr
            if curr_total > total_lambs:
                break
            else:
                n_fib+=1
        
        n_max = 2 + n_fib
    
    n_min = int(math.log(total_lambs+1,2))
    return n_max - n_min
    
if __name__ == "__main__":
    print(solution(143))
    # 3

    print(solution(10))
    # 1
