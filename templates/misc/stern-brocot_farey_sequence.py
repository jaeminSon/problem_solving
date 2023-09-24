import sys
sys.path.append("..")
from custom_type import NAT, LIST1D


def stern_brocot_seq(n: NAT) -> LIST1D:
    assert n > 0 and sum([int(c) for c in bin(n + 1)[2:]]) == 1

    seq = [1]
    for i in range(n//2):
        seq.append(seq[i])
        seq.append(seq[i]+seq[i+1])

    return list(zip(seq, seq[::-1]))


def farey_seq(n: NAT) -> LIST1D:
    return [(0, 1)] + [el for el in stern_brocot_seq(2**n-1)[:2**(n-1)] if el[0] <= n and el[1] <= n]


if __name__ == "__main__":
    assert stern_brocot_seq(1) == [(1, 1)]
    assert stern_brocot_seq(3) == [(1, 2), (1, 1), (2, 1)]
    assert stern_brocot_seq(7) == [(1, 3), (1, 2), (2, 3), (1, 1), (3, 2), (2, 1), (3, 1)]

    assert farey_seq(1) == [(0, 1), (1, 1)]
    assert farey_seq(2) == [(0, 1), (1, 2), (1, 1)]
    assert farey_seq(3) == [(0, 1), (1, 3), (1, 2), (2, 3), (1, 1)]
    assert farey_seq(7) == [(0, 1), (1, 7), (1, 6), (1, 5), (1, 4), (2, 7), (1, 3), (2, 5), (3, 7),
                            (1, 2), (4, 7), (3, 5), (2, 3), (5, 7), (3, 4), (4, 5), (5, 6), (6, 7), (1, 1)]
