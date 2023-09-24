import sys
sys.path.append("..")
from custom_type import LIST1D, NAT

import bisect


def max_increasing_sequence(seq: LIST1D) -> NAT:
    stack = []
    res = 0
    for val in seq:
        if not stack or val > stack[-1]:
            stack.append(val)
            res = max(res, len(stack))
        else:
            index_insert = bisect.bisect_left(stack, val)
            stack[index_insert] = val

    return res
