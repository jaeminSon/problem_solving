import math
from decimal import Decimal, getcontext

import numpy as np

def solution(s):
    n = int(s)
    getcontext().prec = 101
    root2 = Decimal(2).sqrt()
    root2minus1 = root2 - Decimal(1)
    
    def S(k):
        if k==0:
            return 0
        l = int(Decimal(k) * root2minus1)
        m = k + l
        addition = m*(m+1)//2 - l*(l+1)
        return addition - S(l)
        
    return str(S(n))
        

def examine_diff():
    sqrt2 = 2**(1./2)
    # for i in range(1000000, 1000100):
    for i in range(1, 100001):
        floor_sum = math.floor(i*(i+1)//2 * sqrt2)
        sum_floor = np.sum([math.floor(k*sqrt2) for k in range(i+1)])
        diff = floor_sum - sum_floor
        
        if abs(diff != i//2) > 1:
            print(i, diff, diff - i//2)
    


def examine_interval():
    offset = 0
    list_jump = []
    for i in range(100):
        if i + offset != math.floor(i*2**(1./2)):
            list_jump.append(i)
            offset += 1
    print(np.array(list_jump[1:]) - np.array(list_jump[:-1]))

if __name__=="__main__":
    # examine_diff()
    # examine_interval()
    
    print(solution('77'))
    print(solution('5'))
