import sys
sys.path.append("..")
from custom_type import SEGMENTS1D, SEGMENT1D, NAT


def imos1D(segments: SEGMENTS1D) -> NAT:
    """
    Count the maximum overlaps among segments.
    The implementation ignores boundary and assumes that the smallest coordinate is not less than 0. Otherwise, shrink coordinate first.
    >>> imos1D([(1, 2), (2, 3), (1, 3), (3, 4)])
    2
    """
    assert all(s<e for s,e in segments)
    assert min(s for s,e in segments) >= 0
    
    max_val = max(e for s,e in segments)

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


def imos1D_range(segments: SEGMENTS1D, query_range: SEGMENT1D) -> NAT:
    """
    Count the number of overlap between query_range and segments.
    The implementation ignores boundary and assumes that the smallest coordinate is not less than 0. Otherwise, shrink coordinate first.
    
    >>> imos1D_range([(1, 3), (2, 3), (3, 6), (3, 6)], (1, 2))
    1
    """
    assert all(s<e for s,e in segments)
    assert min(s for s,e in segments) >= 0
    
    q_s, q_e = query_range
    assert 0<= q_s <= q_e

    max_val = max(max(e for s,e in segments), max(query_range))

    rsum = [0] * (max_val+1)  # rsum[i] == #elements[i<=x]
    lsum = [0] * (max_val+1)  # lsum[i] == #elements[x<=i]
    for s, e in segments:
        rsum[s] += 1
        lsum[e] += 1

    for i in range(max_val-1, 0, -1):
        rsum[i] += rsum[i+1]

    for i in range(max_val):
        lsum[i+1] += lsum[i]

    non_overlap = lsum[q_s] + rsum[q_e] # #elements[x<=q_s | q_e<=x] 

    return len(segments) - non_overlap


if __name__ == "__main__":
    assert imos1D([(1, 3), (1, 3), (3, 6), (3, 6)]) == 2
    assert imos1D([(1, 2), (2, 3), (1, 3), (3, 4)]) == 2

    assert imos1D_range([(1, 3), (2, 3), (3, 6), (3, 6)], (1, 2)) == 1
    assert imos1D_range([(1, 2), (2, 3), (1, 3), (3, 4)], (1, 2)) == 2
    assert imos1D_range([(1, 2), (2, 3), (1, 3), (3, 4)], (1, 1)) == 0
    assert imos1D_range([(1, 2), (2, 3), (1, 3), (3, 4)], (9, 9)) == 0
