def binary_search_right_exclusive(list_val, query):
    # [l, r)
    lo, hi = 0, len(list_val)
    while lo < hi:
        mid = (lo + hi) // 2
        if list_val[mid] < query:
            lo = mid + 1
        else:
            hi = mid
    return lo # find lo such that list_val[:lo] < query


def binary_search_right_inclusive(list_val, query):
    # [l, r]
    lo, hi = 0, len(list_val)-1
    while lo <= hi:
        mid = (lo + hi) // 2
        if list_val[mid] < query:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo # find lo such that list_val[:lo] < query


import bisect
list_val = [-1,0,1,2,4,5,6]
val = 2
assert bisect.bisect_left(list_val, val) == 3 # first element >= val
assert bisect.bisect_right(list_val, val) == 4 # first element > val

for index, val in enumerate(list_val):
    assert binary_search_right_inclusive(list_val, val) == index and binary_search_right_exclusive(list_val, val) == index
    assert binary_search_right_inclusive(list_val, val-1) == binary_search_right_exclusive(list_val, val-1) and bisect.bisect_left(list_val, val-1)==binary_search_right_exclusive(list_val, val-1)
    assert binary_search_right_inclusive(list_val, val+1) == binary_search_right_exclusive(list_val, val+1) and bisect.bisect_left(list_val, val+1)==binary_search_right_exclusive(list_val, val+1)
