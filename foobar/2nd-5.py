from fractions import Fraction


def solution(pegs):
    
    def verify(diff, f):
        if f < 1:
            return False
        
        curr_val = f
        for d in diff:
            curr_val = d-curr_val
            if curr_val <= 1:
                return False
        return True
    
    n = len(pegs)
    diff = [pegs[i]-pegs[i-1] for i in range(1, n)]
    
    s = 0
    for i, d in enumerate(diff):
        if i%2==0:
            s+=d
        else:
            s-=d
    
    if s <= 0:
        return -1,-1    
    elif n%2==0:
        f = Fraction(s) * Fraction(2,3)
        if verify(diff, f):
            return f.numerator, f.denominator
        else:
            return -1, -1
    else:
        f = Fraction(s) * Fraction(2)
        if verify(diff, f):
            return f.numerator, f.denominator
        else:
            return -1, -1
    
if __name__ == "__main__":
    print(solution([4, 30, 50]))
    # 12,1
    print(solution([4, 17, 50]))
    # -1,-1