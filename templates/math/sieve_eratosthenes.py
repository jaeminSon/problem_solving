def sieve_eratosthenes(n:int):

    is_prime = [False, False] + [True] * (n - 1)
    primes = [2]

    for j in range(4, n + 1, 2):
        is_prime[j] = False

    for i in range(3, n + 1, 2):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return primes

if __name__ == "__main__":
    assert len(sieve_eratosthenes(10)) == 4

