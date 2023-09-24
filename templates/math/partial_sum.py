import sys
sys.path.append("..")
from custom_type import LIST1D, LIST2D


def cumulative_sum(l: LIST1D) -> LIST1D:
    # s[i] = sum(l[:i])
    s = [0]
    for i in range(len(l)):
        s.append(s[-1]+l[i])
    return s


def partial_sum(l: LIST1D) -> LIST2D:
    # ps[i][j] = sum([i:j])
    s = cumulative_sum(l)
    n = len(l)+1
    ps = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            ps[i][j] = s[j] - s[i]
    return ps


if __name__ == "__main__":
    assert cumulative_sum([1, 2, 3]) == [0, 1, 3, 6]
    assert partial_sum([1, 2, 3]) == [[0, 1, 3, 6], [0, 0, 2, 5], [0, 0, 0, 3], [0, 0, 0, 0]]
