from cmath import exp, pi


def fft(a):
    if len(a) == 1:
        return a
    else:
        a_even=fft(a[0::2])
        a_odd=fft(a[1::2])
        w_N=[exp(2j*pi*n/len(a)) for n in range(len(a)//2)]
        return [a_even[n] +w_N[n]*a_odd[n] for n in range(len(a)//2)] + [a_even[n]-w_N[n]*a_odd[n] for n in range(len(a)//2)]
 
def inverse_fft(a):

    def _inverse_fft(a):
        if len(a) == 1:
            return a
        else:
            a_even=_inverse_fft(a[0::2])
            a_odd=_inverse_fft(a[1::2])
            w_N=[exp(-2j*pi*n/len(a)) for n in range(len(a)//2)]
            return [a_even[n] +w_N[n]*a_odd[n] for n in range(len(a)//2)] + [a_even[n]-w_N[n]*a_odd[n] for n in range(len(a)//2)]
    
    return [round(c.real / len(a)) for c in _inverse_fft(a)]

def is_power_2(val):
    if val == 1:
        return True
    elif val % 2 == 1:
        return False
    else:
        return is_power_2(val//2)

def just_bigger_power_2(val):
    i=0
    while 2**i < val:
        i+=1
    return 2**i

def convolution(a, b):
    # c[k] = sum_{l=0..N-1} a[l]*b[k-l]
    n = len(a)
    assert n == len(b)
    
    if is_power_2(n):
        a_fft = fft(a) 
        b_fft = fft(b)
        c_fft = [a_fft[i]*b_fft[i] for i in range(n)]
    else:
        new_n = just_bigger_power_2(2*n)
        a_fft = fft(a+[0]*(new_n-n))
        b_fft = fft(b+[0]*(new_n-2*n)+b)
        c_fft = [a_fft[i]*b_fft[i] for i in range(new_n)]
    
    return inverse_fft(c_fft)

def fast_polynomial_multiplication(a, b, x=1):
    # f(x) = a[0]+a[1]x+...+a[n-1]x^(n-1)
    # g(x) = b[0]+b[1]x+...+b[n-1]x^(n-1)
    # f(x)*g(x) = sum_{k=1..2n-1} sum_{l=0..2n-1} a[l]*b[k-l]*(x^k) = sum_{k=1..2n-1} c[k]*(x^k)
    #    where c[k] = sum_{l=0..2n-1} a[l]*b[k-l] where a[n]=...=a[2n-1]=b[n]=...=b[2n-1]=0
    n = len(a)
    assert n == len(b)
    
    new_n = just_bigger_power_2(2*n-1)
    a_fft = fft(a+[0]*(new_n-n))
    b_fft = fft(b+[0]*(new_n-n))
    c_fft = [a_fft[i]*b_fft[i] for i in range(new_n)]
    
    if x==1:
        return inverse_fft(c_fft)
    else:
        return [c*(x**i) for i, c in enumerate(inverse_fft(c_fft))]

if __name__=="__main__":
    assert convolution([1,1,1,1],[1,1,1,1])==[4, 4, 4, 4]
    assert fast_polynomial_multiplication([2,1], [3,1]) == [6, 5, 1, 0]
    assert fast_polynomial_multiplication([9, -10, 7, 6], [-5, 4, 0, -2]) == [-45, 86, -75, -20, 44, -14, -12, 0]