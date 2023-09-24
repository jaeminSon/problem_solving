import sys
sys.path.append("..")
from custom_type import NAT


def all_sum_chain(n: NAT, s: NAT = 1) -> NAT:
    # >>> all_sum_chain(5)
    # >>> [[5], [1, 4], [1, 1, 3], [1, 1, 1, 2], [1, 1, 1, 1, 1], [1, 2, 2], [2, 3]]
    yield [n]
    for t in range(s, n//2+1):
        for chain in all_sum_chain(n-t, t):
            yield [t] + chain


def sum_chain(n: NAT, components: NAT, s=1):
    # >>> sum_chain(5, 2)
    # >>> [[1, 4], [2, 3]]
    if components == 1:
        yield [n]
    else:
        for t in range(s, n//components+1):
            for chain in sum_chain(n-t, components-1, t):
                yield [t] + chain


if __name__ == "__main__":
    assert list(all_sum_chain(5)) == [[5], [1, 4], [1, 1, 3], [1, 1, 1, 2], [1, 1, 1, 1, 1], [1, 2, 2], [2, 3]]
    assert list(sum_chain(5, 2)) == [[1, 4], [2, 3]]
