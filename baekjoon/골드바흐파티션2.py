import sys
from cmath import exp, pi

T = int(sys.stdin.readline().rstrip())

l_p = [int(sys.stdin.readline().rstrip()) for _ in range(T)]

def is_power_2(val):
    if val == 1:
        return True
    elif val % 2 == 1:
        return False
    else:
        return is_power_2(val//2)

def fft_inplace(v, inverse=False):

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
        assert is_power_2(len(v))
        nbit = get_n_bit(len(v))
        reversed_indices = [bit_reverse(i, nbit)for i in range(len(v))]
        for i_from, i_to in enumerate(reversed_indices):
            if i_from < i_to:
                v[i_to], v[i_from] = v[i_from], v[i_to]

        return nbit

    N = len(v)
    nbit = permute_vector(v)

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

def fast_polynomial_multiplication_inplace(a, b, x=1):
    # f(x) = a[0]+a[1]x+...+a[n-1]x^(n-1)
    # g(x) = b[0]+b[1]x+...+b[n-1]x^(n-1)
    # f(x)*g(x) = sum_{k=1..2n-1} sum_{l=0..2n-1} a[l]*b[k-l]*(x^k) = sum_{k=1..2n-1} c[k]*(x^k)
    #    where c[k] = sum_{l=0..2n-1} a[l]*b[k-l] where a[n]=...=a[2n-1]=b[n]=...=b[2n-1]=0
    n = len(a)
    assert n == len(b)
    
    new_n = just_bigger_power_2(2*n-1)
    a_fft = fft_inplace(a+[0]*(new_n-n))
    b_fft = fft_inplace(b+[0]*(new_n-n))
    c_fft = [a_fft[i]*b_fft[i] for i in range(new_n)]
    
    if x==1:
        return fft_inplace(c_fft, inverse=True)
    else:
        return [c*(x**i) for i, c in enumerate(fft_inplace(c_fft, inverse=True))]

def just_bigger_power_2(val):
    i=0
    while 2**i < val:
        i+=1
    return 2**i


n = 1_000_000
is_prime = [False, False, False] + [True, False] * ((n - 2) // 2)
for i in range(3, n + 1, 2):
    if is_prime[i]:
        for j in range(i * i, n + 1, i):
            is_prime[j] = False

new_coeff = [0] * 500_001
for i,b in enumerate(is_prime):
    if b:
        new_coeff[(i-1) // 2] = 1

v = fast_polynomial_multiplication_inplace(new_coeff, new_coeff)

for p in l_p:
    if p==4:
        print(1)
    else:
        print((v[p//2-1]+1)//2)
