def solution(n, b):
    
    def base2int(val, b):
        res = 0
        running_exp = 1
        for i in range(len(val)-1, -1, -1):
            res += (int(val[i]) * running_exp)
            running_exp *= b
        return res
    
    def int2base(val, b, k):
        list_digit = []
        while val > 0:
            digit = val % b
            list_digit.append(str(digit))
            val //= b
        
        res = "".join(list_digit[::-1])
        
        return res.zfill(k)
        
    
    def diff(x, y, b, k):
        return int2base(base2int(x, b) - base2int(y, b), b, k)
    
    k = len(n)
    
    dict_vals = {n:0}
    
    curr_val = n
    count = 0
    while True:
        count += 1
        x = sorted([c for c in curr_val], reverse=True)
        y = sorted([c for c in curr_val])
        z = diff("".join(x), "".join(y), b, k)
        
        if z in dict_vals:
            return count - dict_vals[z]
        else:
            dict_vals[z] = count
            curr_val = z
            

if __name__ == "__main__":
    print(solution('1211', 10))
    # 1
    print(solution('210022', 3))
    # 3
    