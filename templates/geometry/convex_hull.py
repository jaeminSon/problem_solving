import sys
sys.path.append("..")
from custom_type import POLYGON2D

from functools import cmp_to_key


def dist_square(p1, p2):
    return ((p1[0] - p2[0]) * (p1[0] - p2[0]) +
            (p1[1] - p2[1]) * (p1[1] - p2[1]))


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


def convex_hull_graham(points: POLYGON2D) -> POLYGON2D:
    n = len(points)

    p0 = min(points, key=lambda x: (x[1], -x[0]))
    points = sorted(points, key=cmp_to_key(lambda x, y: compare(p0, x, y)))

    S = [points[0], points[1], points[2]]

    for i in range(3, n):
        while ((len(S) > 1) and
               (orientation(S[-2], S[-1], points[i]) != "ccw")):
            S.pop()
        S.append(points[i])
    return S


def convex_hull_monotone(points: POLYGON2D) -> POLYGON2D:
    n = len(points)

    points = sorted(points, key=lambda x: (x[0], x[1]))

    # lower hull
    L = []
    for i in range(n):
        while len(L) >= 2 and orientation(L[-2], L[-1], points[i]) != "ccw":
            L.pop()
        L.append(points[i])

    # upper hull
    U = []
    for i in range(n-1, -1, -1):
        while len(U) >= 2 and orientation(U[-2], U[-1], points[i]) != "ccw":
            U.pop()
        U.append(points[i])

    return L[:-1]+U[:-1]


if __name__ == "__main__":
    assert convex_hull_graham([(0, 3), (1, 1), (2, 2), (4, 4),
                              (0, 0), (1, 2), (2, 1), (3, 1), (3, 3)]) == [(0, 0), (3, 1), (4, 4), (0, 3)]
    assert convex_hull_monotone([(0, 3), (1, 1), (2, 2), (4, 4),
                                (0, 0), (1, 2), (2, 1), (3, 1), (3, 3)]) == [(0, 0), (3, 1), (4, 4), (0, 3)]
    