import sys
sys.path.append("..")
from custom_type import LIST1D, REAL, INT, NAT

import bisect


def binary_search_func(func: callable, lo: INT, hi: INT) -> NAT:
    """
    Find a largest value within [a,b] such that func(val) is True.
    """
    while lo < hi:
        mid = (lo + hi) // 2
        if func(mid):
            lo = mid + 1
        else:
            hi = mid - 1
    return lo - 1


def binary_search_right_exclusive(list_val: LIST1D, query: REAL) -> NAT:
    # [l, r)
    lo, hi = 0, len(list_val)
    while lo < hi:
        mid = (lo + hi) // 2
        if list_val[mid] < query:
            lo = mid + 1
        else:
            hi = mid
    return lo  # find lo such that list_val[:lo] < query


def binary_search_right_inclusive(list_val: LIST1D, query: REAL) -> NAT:
    # [l, r]
    lo, hi = 0, len(list_val)-1
    while lo <= hi:
        mid = (lo + hi) // 2
        if list_val[mid] < query:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo  # find lo such that list_val[:lo] < query


def parallel_binary_search(min_val: REAL, max_val: REAL, n_queries: LIST1D):

    l = [min_val] * n_queries
    r = [max_val] * n_queries
    ans = [None] * n_queries

    while True:
        # group queries by mid point
        mid2query = {i: [] for i in range(min_val, max_val+1)}
        finished = True
        for i in range(len(n_queries)):
            if l[i] <= r[i]:  # binary search of [l,r]
                # if l[i] < r[i]:  # binary search of [l,r)
                finished = False
                mid2query[(l[i] + r[i]) // 2].append(i)
        if finished:
            break

        # run algorithm and handle each query
        for op_count in range(1, max_val+1):  # TODO set for-loop
            # TODO fill some operation here
            for index_query in mid2query[op_count]:
                if None:  # TODO set hit-condition
                    ans[index_query] = None  # TODO set answer
                    r[index_query] = op_count - 1  # binary search of [l,r]
                    # r[index_query] = op_count # binary search of [l,r)
                else:
                    l[index_query] = op_count + 1


list_val = [-1, 0, 1, 2, 4, 5, 6]
val = 2
assert bisect.bisect_left(list_val, val) == 3  # first element >= val
assert bisect.bisect_right(list_val, val) == 4  # first element > val

for index, val in enumerate(list_val):
    assert binary_search_right_inclusive(list_val, val) == index and binary_search_right_exclusive(list_val, val) == index
    assert binary_search_right_inclusive(list_val, val-1) == binary_search_right_exclusive(list_val, val -
                                                                                           1) and bisect.bisect_left(list_val, val-1) == binary_search_right_exclusive(list_val, val-1)
    assert binary_search_right_inclusive(list_val, val+1) == binary_search_right_exclusive(list_val, val +
                                                                                           1) and bisect.bisect_left(list_val, val+1) == binary_search_right_exclusive(list_val, val+1)
