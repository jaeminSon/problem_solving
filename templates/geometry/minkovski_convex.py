import sys
sys.path.append("..")
from custom_type import POLYGON2D

import sys
from functools import cmp_to_key


def dist_square(p1, p2):
    return ((p1[0] - p2[0]) * (p1[0] - p2[0]) +
            (p1[1] - p2[1]) * (p1[1] - p2[1]))


def cross(v1, v2):
    return v1[1] * v2[0] - v1[0]*v2[1]


def orientation(p, q, r):
    # p->q->r
    val = ((q[1] - p[1]) * (r[0] - q[0]) -
           (q[0] - p[0]) * (r[1] - q[1]))
    if abs(val) <= sys.float_info.epsilon:
        return "collinear"
    elif val > sys.float_info.epsilon:
        return "cw"
    else:
        return "ccw"


def compare(p0, p1, p2):

    o = orientation(p0, p1, p2)
    if o == "collinear":
        if dist_square(p0, p2) >= dist_square(p0, p1):
            return -1
        else:
            return 1
    else:
        if o == "ccw":
            return -1
        elif o == "cw":
            return 1


def minkovski_convex(A: POLYGON2D, B: POLYGON2D) -> POLYGON2D:

    # order vertices ccw
    start = min(A, key=lambda x: (x[0], x[1]))
    A = sorted(A, key=cmp_to_key(lambda x, y: compare(start, x, y)))
    A.extend([A[0], A[1]])  # make cycle
    start = min(B, key=lambda x: (x[0], x[1]))
    B = sorted(B, key=cmp_to_key(lambda x, y: compare(start, x, y)))
    B.extend([B[0], B[1]])

    S = []
    i, j = 0, 0
    while i < len(A) - 2 or j < len(B) - 2:
        # add point while maintaining convexity
        curr_point = (A[i][0]+B[j][0], A[i][1]+B[j][1])
        while len(S) >= 2 and orientation(S[-2], S[-1], curr_point) != "ccw":
            S.pop()
        S.append(curr_point)

        # advance vector with smaller ccw angle
        if cross((A[i + 1][0] - A[i][0], A[i + 1][1] - A[i][1]),
                 (B[j + 1][0] - B[j][0], B[j + 1][1] - B[j][1])) < 0:
            i += 1
        else:
            j += 1

    # remove non-convexity in S[-2]->S[-1]->S[0]
    if len(S) >= 3 and orientation(S[-2], S[-1], S[0]) != "ccw":
        S.pop()

    return S


if __name__ == "__main__":
    assert set(minkovski_convex([(0, 0), (0, 1), (1, 0)], [(0, 0), (0, 1), (1, 1), (1, 0)])) == set([(0, 0), (0, 2), (1, 2), (2, 1), (2, 0)])
    assert set(minkovski_convex([(-1, 0), (0, 1), (1, 0)], [(1, 0), (0, -1), (-1, 0)])) == set([(-2, 0), (-1, 1), (1, 1), (2, 0), (1, -1), (-1, -1)])
    assert set(minkovski_convex([(0, 0), (0, 1), (1, 3), (2, 4), (4, 5), (5, 5)], [(0, 0), (1, 3), (3, 6), (6, 8), (9, 9)])) == set(
        [(0, 0), (0, 1), (1, 4), (2, 6), (4, 9), (5, 10), (8, 12), (10, 13), (13, 14), (14, 14)])
    assert set(minkovski_convex([(0, 1), (0, 2), (1, 2), (1, 1)], [(1, 0), (1, 1), (2, 1), (2, 0)])) == set([(1, 1), (1, 3), (3, 3), (3, 1)])
