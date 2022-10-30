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



def fft_inplace(v, inverse=False):

    def is_power_2(val):
        if val == 1:
            return True
        elif val % 2 == 1:
            return False
        else:
            return is_power_2(val//2)

    def bit_reverse(x,n):
        """
        >> bit_reverse(1, 3)
        >> 4  # (001 -> 100)
        """
        return sum(1<<(n-1-i) for i in range(n) if x>>i&1)

    def get_n_bit(val):
        bit = 0
        while val > 1:
            val >>= 1
            bit += 1
        return bit

    def permute_vector(v):
        reversed_indices = [bit_reverse(i, nbit)for i in range(len(v))]
        for i_from, i_to in enumerate(reversed_indices):
            if i_from < i_to:
                v[i_to], v[i_from] = v[i_from], v[i_to]

        return nbit

    N = len(v)
    nbit = get_n_bit(len(v))
    permute_vector(v)

    for b in range(1, nbit+1):
        i = 1 << b
        for j in range(0, N, i):
            for k in range(i//2):
                wk = exp(2j*pi*k/i) if inverse else exp(-2j*pi*k/i)
                even = v[j+k]
                odd = v[j+k+i//2]
                v[j+k] = even+wk*odd
                v[j+k+i//2] = even-wk*odd

    if inverse:
        for i in range(N):
            v[i] = round((v[i]/N).real)

    return v

def just_bigger_power_2(val):
    i=0
    while 2**i < val:
        i+=1
    return 2**i

def fast_polynomial_multiplication_inplace(a, b, x=1):
    n = len(a)
    
    new_n = just_bigger_power_2(2*n-1)
    a_fft = fft_inplace(a+[0]*(new_n-n))
    b_fft = fft_inplace(b+[0]*(new_n-n))
    c_fft = [a_fft[i]*b_fft[i] for i in range(new_n)]
    
    if x==1:
        return fft_inplace(c_fft, inverse=True)
    else:
        return [c*(x**i) for i, c in enumerate(fft_inplace(c_fft, inverse=True))]


odd_primes += [0]*(len(semi_primes)-len(odd_primes))
ans = fast_polynomial_multiplication_inplace(odd_primes, semi_primes)
T = int(sys.stdin.readline().rstrip())

for _ in range(T):
    query = int(sys.stdin.readline().rstrip())
    print(ans[query])