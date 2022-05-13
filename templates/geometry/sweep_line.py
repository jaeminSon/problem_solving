from sortedcontainers import SortedDict, SortedList
import gmpy2
from typing import List, Optional


NT = gmpy2.mpq
ZERO = NT(0)
ONE = NT(1)
MONE = NT(-1)
BONE = NT(1.1)
MBONE = NT(-1.1)
#NT = float


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = NT(x), NT(y)

    def __sub__(self, o: "Point") -> "Point":
        return Point(self.x - o.x, self.y - o.y)

    def dot(self, o: "Point") -> "Point":
        return self.x * o.x + self.y * o.y

    def __eq__(self, o: "Point") -> bool:
        return self.x == o.x and self.y == o.y

    def __lt__(self, o: "Point") -> bool:
        return self.y > o.y or (self.y == o.y and self.x < o.x)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class ScanLine(object):
    def __init__(self, pt: Optional[Point] = None):
        self.pt = pt

    def isect_seg(self, seg: "Segment") -> Point:
        dy = seg.end.y - seg.start.y
        if dy == 0:
            assert seg.end.y == self.pt.y
            return seg.start

        t = (self.pt.y - seg.start.y) / dy
        x = t * seg.end.x + (1 - t) * seg.start.x
        return Point(x, self.pt.y)

    def set_pt(self, pt: Point):
        self.pt = pt


class SegTreeCmp(object):
    def __init__(self):
        self.scanline = ScanLine()
        self.after_scanline = True

    def set_pt(self, pt: Point):
        self.scanline.set_pt(pt)

    def __call__(self, seg: "Segment") -> (NT, NT, Point, Point, int):
        """
        This defines a total ordering of segment in
        tree based on intersecting order on the scanline
        The tricky part is: segments passing through the same isect point would
        have reversed ordering depending on whether current scanpoint is before
        or after the common isect point
        """
        scanline = self.scanline
        assert seg.end.y <= scanline.pt.y <= seg.start.y
        assert seg.inf or seg.start != seg.end

        if seg._last_pt and seg._last_pt == (self.after_scanline, scanline.pt):
            return seg._last_cmp

        # "Inf" segs, used for range query at pt
        if seg.inf:
            assert not self.after_scanline
            isect_x = seg.start.x
            isect_angle = BONE if seg.inf > 0 else MBONE
        else:
            # Horizontal segment
            if seg.start.y == seg.end.y:
                if seg.start.x <= scanline.pt.x <= seg.end.x:
                    isect_angle = ONE if self.after_scanline else MONE
                    isect_x = scanline.pt.x
                elif seg.start.x > scanline.pt.x:
                    isect_angle = MONE
                    isect_x = seg.start.x
                else:
                    isect_angle = ONE
                    isect_x = seg.start.x
            # General segment
            else:
                if seg._last_pt and seg._last_pt[1] == scanline.pt:
                    isect_x = seg._last_isect_x
                else:
                    isect_xy = scanline.isect_seg(seg)
                    isect_x = isect_xy.x
                    seg._last_isect_x = isect_x

                isect_angle = seg._right_angle
                # seg_angle is squared cos(v, right_v)
                if not self.after_scanline:
                    isect_angle = -isect_angle

        ret = (isect_x, isect_angle, seg.start, seg.end, id(seg))
        seg._last_pt = (self.after_scanline, scanline.pt)
        seg._last_cmp = ret
        return ret


segtree_cmp = SegTreeCmp()


class Segment(object):
    def __init__(self, p1: Point, p2: Point, inf: int = 0):
        if p1 > p2:
            p1, p2 = p2, p1
        self.p1 = p1
        self.p2 = p2
        self.inf = inf
        self._right_angle = self.angle()
        self._last_pt = None
        self._last_cmp = None
        self._last_isect_x = None
        self.set_inf(inf)

    @property
    def start(self) -> Point:
        return self.p1

    @property
    def end(self) -> Point:
        return self.p2

    def ends_with(self, p: Point) -> bool:
        return self.end == p

    def angle(self, o=Point(1, 0)) -> NT:
        v = self.end - self.start
        dot = v.dot(o)
        length = v.dot(v)
        if length != 0:
            isect_angle = (dot * dot) / length
            if dot < 0:
                isect_angle = -isect_angle
        else:
            isect_angle = ZERO

        return isect_angle

    def isect(self, o: "Segment") -> Optional[Point]:
        x1, x2 = self.start.x, self.end.x
        y1, y2 = self.start.y, self.end.y
        ox1, ox2 = o.start.x, o.end.x
        oy1, oy2 = o.start.y, o.end.y
        t = (y1 - y2, x2 - x1, x1 * y2 - x2 * y1)
        ot = (oy1 - oy2, ox2 - ox1, ox1 * oy2 - ox2 * oy1)
        d = (t[1] * ot[2] - t[2] * ot[1], t[2] * ot[0] - t[0] * ot[2],
             t[0] * ot[1] - t[1] * ot[0])

        if d[2] == 0:
            return None
        isect = Point(d[0] / d[2], d[1] / d[2])
        if x1 != x2 and (isect.x < min(x1, x2) or isect.x > max(x1, x2)):
            return None
        if ox1 != ox2 and (isect.x < min(ox1, ox2) or isect.x > max(ox1, ox2)):
            return None
        if y1 != y2 and (isect.y < y2 or isect.y > y1):
            return None
        if oy1 != oy2 and (isect.y < oy2 or isect.y > oy1):
            return None
        return isect

    def set_inf(self, val: int):
        assert val in [-1, 0, 1] and (val == 0 or self.start == self.end)
        self.inf = val

    def __eq__(self, o: "Segment"):
        return segtree_cmp(self) == segtree_cmp(o)

    def __lt__(self, o: "Segment"):
        return segtree_cmp(self) < segtree_cmp(o)

    def __repr__(self):
        if self.inf == 0:
            return "{} -> {}".format(self.p1, self.p2)
        else:
            return "{} -> {}(inf: {})".format(self.p1, self.p2, self.inf)


class SegTree(object):
    def __init__(self):
        self.tree = SortedList()

    def insert(self, seg: Segment):
        self.tree.add(seg)

    def remove(self, seg: Segment):
        self.tree.remove(seg)

    def clear(self):
        self.tree.clear()

    def bisect_pt(self, pt: Point) -> List[Segment]:
        assert pt == segtree_cmp.scanline.pt
        left_seg = Segment(pt, pt, -1)
        right_seg = Segment(pt, pt, 1)

        return list(self.tree.irange(minimum=left_seg, maximum=right_seg))

    def bisect_lleft_pt(self, pt: Point) -> Optional[Segment]:
        inf_seg = Segment(pt, pt, -1)
        ind = self.tree.bisect_left(inf_seg)
        return self.tree[ind - 1] if ind > 0 else None

    def bisect_rright_pt(self, pt: Point) -> Optional[Segment]:
        inf_seg = Segment(pt, pt, 1)
        ind = self.tree.bisect_right(inf_seg)

        return self.tree[ind] if ind < len(self.tree) else None


class SweepLine(object):
    def __init__(self, include_endpoints=False):
        self.include_endpoints = include_endpoints
        self.event_queue = SortedDict()
        self.seg_tree = SegTree()

    def _lower_cover_set(self, pt: Point) -> (List[Segment], List[Segment]):
        isect_segs = self.seg_tree.bisect_pt(pt)
        l_set = []
        c_set = []
        for seg in isect_segs:
            if seg.ends_with(pt):
                l_set.append(seg)
            else:
                c_set.append(seg)
        return l_set, c_set

    def _find_new_event(self, segl: Segment, segr: Segment, pt: Point):
        assert segl and segr
        npt = segl.isect(segr)
        if npt is None:
            return

        if (npt.y < pt.y or (npt.y == pt.y and npt.x > pt.x)) \
                and npt not in self.event_queue:
            self.event_queue[npt] = list()

    def __call__(self, segs: [Segment]) -> List[Point]:
        event_queue = self.event_queue
        seg_tree = self.seg_tree
        event_queue.clear()
        seg_tree.clear()
        isects = []

        # Insert endpoints to event_queue
        for seg in segs:
            st = seg.start
            ed = seg.end
            if st not in event_queue:
                event_queue[st] = list()
            event_queue[st].append(seg)
            if ed not in event_queue:
                event_queue[ed] = list()

        while event_queue:
            pt, u_set = event_queue.popitem(0)
            segtree_cmp.set_pt(pt)
            segtree_cmp.after_scanline = False

            # At this point, even though we have changed scanpoint to pt,
            # but we have to assume the ordering in segtree_cmp to be same
            # as before. Otherwise, tree structure is broken
            # Find l_set with seg covering pt
            l_set, c_set = self._lower_cover_set(pt)
            sl = seg_tree.bisect_lleft_pt(pt)
            sr = seg_tree.bisect_rright_pt(pt)
            if self.include_endpoints:
                if len(u_set) + len(l_set) + len(c_set) > 1:
                    isects.append(pt)
            else:
                if len(c_set):
                    isects.append(pt)

            for seg in l_set + c_set:
                seg_tree.remove(seg)

            # Remove degenerate segs
            u_set = list(filter(lambda x: x.start != x.end, u_set))

            # Changing scanpoint would change the ordering(used in the tree).
            # But only affecting segs passing through pt. At this point,
            # all such segs are removed from the tree and ready to be
            # re-inserted with the new ordering
            uc_set = u_set + c_set
            segtree_cmp.after_scanline = True
            for seg in uc_set:
                seg_tree.insert(seg)

            if not uc_set:
                if sl and sr:
                    self._find_new_event(sl, sr, pt)
            else:
                sp = min(uc_set, key=segtree_cmp)
                if sl:
                    self._find_new_event(sl, sp, pt)
                spp = max(uc_set, key=segtree_cmp)
                if sr:
                    self._find_new_event(spp, sr, pt)

        return isects


def isect_segments(segs: List, include_endpoints: bool = False) -> List:
    seg_objs = [Segment(Point(*seg[0]), Point(*seg[1])) for seg in segs]
    sl = SweepLine(include_endpoints=include_endpoints)
    results = sl(seg_objs)
    return [(float(res.x), float(res.y)) for res in results]

if __name__ == "__main__":
    segments = [((0, 0), (10, 10)), ((5, -5), (5, 5)), ((3,-3), (3,3))]
    ret = isect_segments(segments)
    print(ret)