import sys
sys.path.append("..")
from custom_type import SEGMENTS1D, NAT


def imos1D(segments: SEGMENTS1D, max_val: NAT) -> NAT:
    """
    Count the maximum overlaps among given segments.
    The implementation assumes that the smallest coordinate is not less than 0. Otherwise, shrink coordinate first.
    """
    enter = [0] * (max_val+1)
    for s, e in segments:
        # increment 1 at 's' and decrement at 'e' to sweep from left to right
        enter[s] += 1
        enter[e] -= 1

    ans = 0
    for i in range(1, max_val):
        enter[i] += enter[i-1]  # sweep from left to right
        ans = max(ans, enter[i])
    return ans


def find_max_overlap(element_segments: SEGMENTS1D, query_segments: SEGMENTS1D, max_val: NAT) -> NAT:
    """
    Find the maximum overlap among given query segments.
    The implementation assumes that the smallest coordinate is not less than 0. Otherwise, shrink coordinate first.
    """

    rsum = [0] * (max_val+1)  # rsum[i] == N[i<=x]
    lsum = [0] * (max_val+1)  # lsum[i] == N[x<=i]
    for s, e in element_segments:
        rsum[s] += 1
        lsum[e] += 1

    for i in range(max_val-1, 0, -1):
        rsum[i] += rsum[i+1]

    for i in range(max_val):
        lsum[i+1] += lsum[i]

    min_exclude = max_val
    for s, e in query_segments:
        min_exclude = min(min_exclude, lsum[s] + rsum[e])  # lsum[s] + rsum[e] == N[no overlaps with (s,e)]

    return len(element_segments) - min_exclude


if __name__ == "__main__":
    assert imos1D([(1, 3), (1, 3), (3, 6), (3, 6)], 6) == 2
    assert imos1D([(1, 2), (2, 3), (1, 3), (3, 4)], 6) == 2

    assert find_max_overlap([(1, 3), (1, 3), (3, 6), (3, 6)], [(1, 3), (1, 3), (3, 6), (3, 6)], 6) == 2
    assert find_max_overlap([(1, 2), (2, 3), (1, 3), (3, 4)], [(1, 2), (2, 3), (1, 3), (3, 4)], 6) == 3
