def all_sum_chain(n, s=1):
    # >>> all_sum_chain(5)
    # >>> [[5], [1, 4], [1, 1, 3], [1, 1, 1, 2], [1, 1, 1, 1, 1], [1, 2, 2], [2, 3]]
    yield [n]
    for t in range(s, n//2+1):
        for chain in all_sum_chain(n-t, t):
            yield [t] + chain

def sum_chain(n, components, s=1):
    # >>> sum_chain(5, 2)
    # >>> [[1, 4], [2, 3]]
    if components==1:
        yield [n]
    else:
        for t in range(s, n//components+1):
            for chain in sum_chain(n-t, components-1, t):
                yield [t] + chain

def gcd(a, b):
    large, small = (a, b) if a>=b else (b, a)
    return large if small == 0 else gcd(small, large % small)

if __name__=="__main__":
    assert gcd(10,2)==2
    # print(list(all_sum_chain(5)))
    print(list(sum_chain(100,30)))