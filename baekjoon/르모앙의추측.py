import sys
from cmath import exp, pi

MAX = 1_000_000

def sieve_eratosthenes(n:int) -> list:

    is_prime = [0, 0] + [1] * (n - 1)

    for j in range(4, n + 1, 2):
        is_prime[j] = 0

    for i in range(3, n + 1, 2):
        if is_prime[i] == 1:
            for j in range(i * i, n + 1, i):
                is_prime[j] = 0

    return is_prime

sieve = sieve_eratosthenes(MAX)

semi_primes = [0]*(MAX+1)
for i in range(len(sieve)//2+1):
    if sieve[i]==1:
        semi_primes[2*i] = sieve[i]
sieve[2] = 0 # set 0 for 2
odd_primes = sieve


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

def conv(a, b):
    n = len(a)
    assert n == len(b)
    
    new_n = just_bigger_power_2(2*n-1)
    a_fft = fft(a+[0]*(new_n-n))
    b_fft = fft(b+[0]*(new_n-n))
    c_fft = [a_fft[i]*b_fft[i] for i in range(new_n)]
    
    return inverse_fft(c_fft)

odd_primes += [0]*(len(semi_primes)-len(odd_primes))
ans = conv(odd_primes, semi_primes)

T = int(sys.stdin.readline().rstrip())

for _ in range(T):
    query = int(sys.stdin.readline().rstrip())
    print(ans[query])