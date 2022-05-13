def solution(i):

    def isprime(x):
        if x==2:
            return True
        for i in range(2, int(x**1./2)+2):
            if x%i==0:
                return False
        return True
            
        
    curr_val = 2
    concat_str = ""
    while len(concat_str) < i + 5:
        if isprime(curr_val):
            concat_str += str(curr_val)
        curr_val += 1
        
    return concat_str[i:i+5]

if __name__ == "__main__":
    print(solution(0))
    # 23571

    print(solution(3))
    # 71113
