import sys
sys.path.append("..")
from custom_type import HALFPLANES, POLYGON2D

from collections import deque
from typing import List
import math


# reference: http://www.secmem.org/blog/2019/09/17/Half-Plane-Intersection/


def intersection(half_plane1, half_plane2):
    # a1x+b1y+c1=0
    # a2x+b2y+c2=0
    a1, b1, c1 = half_plane1
    a2, b2, c2 = half_plane2
    d = a1*b2-a2*b1
    if abs(d) < sys.float_info.epsilon:  # parallel
        return float('inf')
    else:
        return (1.*(c2*b1-c1*b2)/d, 1.*(a2*c1-c2*a1)/d)  # (x,y)


def angle(a, b):
    # half plane (ax+by+c<=0)| angle (ccw from (-1,0))
    #         -x+c <=0       | 0
    #          x+c <=0       | pi
    return math.acos(-a/(a**2+b**2)**(1./2)) if b <= 0 else math.acos(a/(a**2+b**2)**(1./2)) + math.pi


def same_sign(a, b):
    return a*b > 0


def parallel(half_plane1, half_plane2):
    a1, b1, _ = half_plane1
    a2, b2, _ = half_plane2
    return (a1 == 0 and a2 == 0 and same_sign(b1, b2)) or (b1 == 0 and b2 == 0 and same_sign(a1, a2)) or (same_sign(a1, a2) and same_sign(b1, b2) and a1 * b2 == b1 * a2)


def cover(half_plane1, half_plane2):
    # whether half_plane1 covers half_plane2 (assume two are parallel)
    assert parallel(half_plane1, half_plane2)

    a1, b1, c1 = half_plane1
    a2, b2, c2 = half_plane2
    if b1 == 0 and b2 == 0:
        return a2*c1 >= a1*c2 if a1 < 0 else a2*c1 <= a1*c2
    else:
        return b2*c1 >= b1*c2 if b1 < 0 else b2*c1 <= b1*c2


def outbound(half_plane, point):
    a, b, c = half_plane
    x, y = point
    return a*x+b*y+c > 0


def half_plane_intersection(list_half_plane: HALFPLANES) -> POLYGON2D:
    # half plane: ax+by+c<=0
    # # [(a1,b1,c1), ..., (an,bn,cn)] where a,b,c are integers

    list_sorted_half_plane = sorted(list_half_plane, key=lambda x: angle(x[0], x[1]))

    q = deque()
    for half_plane in list_sorted_half_plane:
        if len(q) == 0:
            q.append(half_plane)
        elif len(q) >= 1 and parallel(q[-1], half_plane):
            if cover(q[-1], half_plane):
                q.pop()
                q.append(half_plane)
        else:
            while len(q) >= 2 and outbound(half_plane, intersection(q[-1], q[-2])):
                q.pop()
            while len(q) >= 2 and outbound(half_plane, intersection(q[0], q[1])):
                q.pop()
            q.append(half_plane)

    return [intersection(q[i], q[(i+1) % len(q)]) for i in range(len(q))]


if __name__ == "__main__":
    print(half_plane_intersection([[-1, 0, 0], [-1, 0, -1], [0, -1, 0], [2, 1, -4], [-1, 2, -4]]))
    print(half_plane_intersection([[-1, 1, 1], [1, -1, -1]]))
