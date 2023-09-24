import sys
sys.path.append("..")
from custom_type import POLYGON2D, REAL


class SegmentTree:
    """Segment tree to maintain a set of integer intervals 
    and query the size of their union.
    """

    def __init__(self, L):
        assert L != []
        self.N = 1
        while self.N < len(L):
            self.N *= 2
        self.full_cover_count = [0] * (2 * self.N)
        self.actual_cover = [0] * (2 * self.N)
        self.length = [0] * (2 * self.N)
        for i, _ in enumerate(L):
            self.length[self.N + i] = L[i]
        for p in range(self.N - 1, 0, -1):
            self.length[p] = self.length[2 * p] + self.length[2 * p + 1]

    def coverage(self):
        return self.actual_cover[1]

    def update(self, i, k, offset):
        """interval [i,k]
        offset == +1 => adds interval [i, k],
        offset == -1 => removes interval [i, k],
        """
        self._update_fn(1, 0, self.N, i, k, offset)

    def _update_fn(self, p, start, span, i, k, offset):
        if start + span <= i or k <= start:  # no overlap between [i,k] and [start, start+span]
            return
        if i <= start and start + span <= k:  # [start, start+span] in [i,k]
            self.full_cover_count[p] += offset
        else:  # [start, start+span] not in [i,k] but there exists overlap
            self._update_fn(2 * p, start, span // 2, i, k, offset)
            self._update_fn(2 * p + 1, start + span // 2, span // 2,
                            i, k, offset)

        if self.full_cover_count[p] == 0:
            if p >= self.N:  # leaf
                self.actual_cover[p] = 0
            else:  # non-leaf (aggregate leaves)
                self.actual_cover[p] = self.actual_cover[2 * p] + self.actual_cover[2 * p + 1]
        else:
            self.actual_cover[p] = self.length[p]


def union_rectangles(list_points: POLYGON2D) -> REAL:
    # list of (x1, y1, x2, y2) where (x1, y1) is top left corner and (x2, y2) bottom right corner (e.g. (0,0,3,3))
    if list_points == []:
        return 0
    X = set()
    events = []
    for x1, y1, x2, y2 in list_points:
        assert x1 <= x2 and y1 <= y2
        X.add(x1)
        X.add(x2)
        events.append((y1, +1, x1, x2))
        events.append((y2, -1, x1, x2))

    i_to_x = list(sorted(X))
    x_to_i = {i_to_x[i]: i for i in range(len(i_to_x))}

    L = [i_to_x[i + 1] - i_to_x[i] for i in range(len(i_to_x) - 1)]
    C = SegmentTree(L)
    area = 0
    previous_y = 0
    for y, offset, x1, x2 in sorted(events):
        area += (y - previous_y) * C.coverage()
        i1 = x_to_i[x1]
        i2 = x_to_i[x2]
        C.update(i1, i2, offset)
        previous_y = y

    return area


if __name__ == "__main__":
    assert union_rectangles([[0, 0, 2, 2], [0, 0, 2, 2]]) == 4
    assert union_rectangles([[0, 0, 2, 2], [1, 1, 3, 3]]) == 7
