import sys
import bisect

N = int(sys.stdin.readline())

dict_earning = {}
for _ in range(N):
    l = [int(el) for el in sys.stdin.readline().split()]
    query = list(zip(l[1::2], l[2::2]))
    query_sorted = sorted(query, key=lambda x:x[0])
    
    for i, q in enumerate(query_sorted):
        if i == 0:
            curr_max = query_sorted[0][1]
            val = curr_max
            prev_max = curr_max
        else:
            curr_max = max(curr_max, q[1])
            val = curr_max - prev_max
            prev_max = curr_max
        dict_earning[q[0]] = dict_earning.get(q[0], 0) + val

w_query_sorted = sorted(dict_earning.keys())
earnings = [dict_earning[w] for w in w_query_sorted]
for i in range(1, len(earnings)):
    earnings[i] += earnings[i-1]

Q = int(sys.stdin.readline())
Qs = [int(el) for el in sys.stdin.readline().split()]

n_earnings = len(earnings)
ans = [bisect.bisect_left(earnings, q) for q in Qs]
print(" ".join([str(w_query_sorted[i]) if i < n_earnings else str(-1) for i in ans]))