def solution(start, length):
    
    def XOR_upto(val):
        if val < 0:
            return 0
        elif (val+1) % 4 == 0:
            return 0
        elif (val+1) % 4 == 1:
            return val
        elif (val+1) % 4 == 2:
            return (val-1)^val
        elif (val+1) % 4 == 3:
            return (val-2)^(val-1)^val
    
    res = 0
    for line in range(length):
        s = line*length + start
        e = line*length + start + length - line - 1
        res ^= (XOR_upto(e) ^ XOR_upto(s-1))

    return res

if __name__ =="__main__":
    assert solution(0, 3)==2
    assert solution(17, 4)==14
    print(solution(2000000000, 10000))
