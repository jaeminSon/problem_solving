import sys
sys.path.append("..")
from custom_type import POLYGON2D, NAT

import math


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


def dist(p1, p2):
    return math.sqrt((p1.x - p2.x) *
                     (p1.x - p2.x) +
                     (p1.y - p2.y) *
                     (p1.y - p2.y))


def bruteForce(P, n):
    min_val = float('inf')
    for i in range(n):
        for j in range(i + 1, n):
            if dist(P[i], P[j]) < min_val:
                min_val = dist(P[i], P[j])

    return min_val


def stripClosest(strip, size, d):
    min_val = d
    for i in range(size):
        j = i + 1
        while j < size and dist(strip[i], strip[j]) < min_val:
            min_val = min(min_val, dist(strip[i], strip[j]))
            j += 1

    return min_val


def closestUtil(P, n_total_points):

    if n_total_points <= 3:
        return bruteForce(P, n_total_points)

    mid = n_total_points // 2
    midPoint = P[mid]

    Pl = P[:mid]
    Pr = P[mid:]

    dl = closestUtil(Pl, mid)
    dr = closestUtil(Pr, n_total_points - mid)
    d = min(dl, dr)

    # candidates for closest points
    stripP = []
    lr = Pl + Pr
    for i in range(n_total_points):
        if abs(lr[i].x - midPoint.x) < d:
            stripP.append(lr[i])
    stripP.sort(key=lambda point: point.y)
    return min(d, stripClosest(stripP, len(stripP), d))


def closest(P: POLYGON2D, n: NAT) -> Point:
    P.sort(key=lambda point: point.x)
    return closestUtil(P, n)


if __name__ == "__main__":
    P = [Point(2, 3), Point(12, 30),
         Point(40, 50), Point(5, 1),
         Point(12, 10), Point(3, 4)]
    n = len(P)
    print("The smallest distance is",
          closest(P, n))
