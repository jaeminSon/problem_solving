import sys
from cmath import exp, pi

a = [0] * 524288
a[0] = 1

N = int(sys.stdin.readline().rstrip())
for _ in range(N):
    a[int(sys.stdin.readline().rstrip())] = 1

query = []
M = int(sys.stdin.readline().rstrip())
for _ in range(M):
    query.append(int(sys.stdin.readline().rstrip()))

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


def convolution(a, b):
    a_fft = fft(a) 
    b_fft = fft(b)
    c_fft = [a_fft[i]*b_fft[i] for i in range(len(a))]
    return inverse_fft(c_fft)

c = convolution(a, a)
print(sum([c[q]>0 for q in query]))
