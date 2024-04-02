import sys
sys.path.append("..")
from custom_type import NAT, LIST1D, SEGMENTS1D


def mo(data: LIST1D, queries: SEGMENTS1D) -> LIST1D:
    """
    Sort range queries efficiently to achieve (N+Q)sqrt(N) where N==|data| and Q==|queries|.
    Return a list of answers to all queries.
    """
    Q = len(queries)

    sqrtN = int(len(data)**(1./2))
    l_sorted_queries = sorted(queries, key=lambda x: (x[0]//sqrtN, x[1]))

    def add(s, e):
        for i in range(s, e+1):
            pass

    def remove(s, e):
        for i in range(s, e+1):
            pass

    add(l_sorted_queries[0][0], l_sorted_queries[0][1])
    s, e = l_sorted_queries[0]
    dict_ans = {(s, e): initial_value}
    for i in range(1, Q):
        new_s, new_e = l_sorted_queries[i]

        if s > new_s:  # add (new_s, new_s+1, ..., s-1)
            add(new_s, s-1)
        if e < new_e:  # add (e+1, e+2, ..., new_e)
            add(e+1, new_e)
        if s < new_s:  # remove (s, s+1, ..., new_s-1)
            remove(s, new_s-1)
        if e > new_e:  # remove (new_e+1, ..., e-1, e)
            remove(new_e+1, e)

        dict_ans[(new_s, new_e)] = something

        s, e = new_s, new_e

    return [dict_ans[tuple(q)] for q in queries]
