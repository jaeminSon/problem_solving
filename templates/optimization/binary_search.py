def binary_search(list_val, query):
    lo, hi = 0, len(list_val)
    while lo < hi:
        mid = (lo + hi) // 2
        if list_val[mid] < query:
            lo = mid + 1
        else:
            hi = mid