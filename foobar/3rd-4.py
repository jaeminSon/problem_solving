def solution(n):
    n = int(n)
    
    count = 0
    while n > 0:
        if n % 2 == 0:
            n /= 2
            count+=1
        else:
            if n==3:
                n = 2
                count += 1
            elif n % 4 == 1:
                n -= 1
                count += 1 
            else:
                n += 1
                count += 1
    
    return count-1
            
    
if __name__ == "__main__":
    assert solution("1") == 0
    assert solution("2") == 1
    assert solution("3") == 2
    assert solution("19") == 6
    assert solution("11") == 5
    assert solution('15') == 5
    assert solution('4') == 2
    assert solution('3') == 2
    assert solution('2') == 1
    assert solution('6') == 3
    assert solution('7') == 4
    assert solution('10') == 4
    assert solution('1024') == 10
    assert solution('1025') == 11
    assert solution('1026') == 11
    assert solution('1027') == 12        
    # print(solution("9"*300))
