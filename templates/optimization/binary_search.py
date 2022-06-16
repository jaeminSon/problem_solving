def binary_search(list_val, query):
    lo, hi = 0, len(list_val)
    while lo < hi:
        mid = (lo + hi) // 2
        if list_val[mid] < query:
            lo = mid + 1
        else:
            hi = mid

import bisect
list_val = [-1,0,1,2,4,5,6]
val = 2
assert bisect.bisect_left(list_val, val) == 3 # first element >= val
assert bisect.bisect_right(list_val, val) == 4 # first element > val