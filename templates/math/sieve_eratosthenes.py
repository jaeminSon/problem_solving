def sieve_eratosthenes(n:int) -> list:
    # sieve starts with 0
    is_prime = [False, False, True] + [True, False] * ((n - 2) // 2)
    if n % 2 == 1:
        is_prime += [True]
    primes = [2]

    for i in range(3, n + 1, 2):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return primes, is_prime

if __name__ == "__main__":
    list_primes, sieve = sieve_eratosthenes(10)
    assert len(list_primes) == 4
    assert sieve==[False, False, True, True, False, True, False, True, False, False, False]

