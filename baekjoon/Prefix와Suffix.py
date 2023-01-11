import sys
from itertools import islice, chain

sys.setrecursionlimit(100000)

s = sys.stdin.readline().rstrip()

def generate_partial_match_table(pattern):
    table = [0] * len(pattern)
 
    i = 1
    j = 0
    while i < len(pattern):
        if pattern[i]== pattern[j]:
            table[i] = j + 1
            i += 1
            j += 1
        else:
            if j != 0: # check if previous match could be used
                j = table[j-1]
            else:
                i += 1
    return table

def suffix_array(A):
    """Return a list of the starting positions of the suffixes of the
    sequence A in sorted order.

    For example, the suffixes of ABAC, in sorted order, are ABAC, AC,
    BAC and C, starting at positions 0, 2, 1, and 3 respectively:

    >>> suffix_array('ABAC')
    [0, 2, 1, 3]

    """
    # This implements the algorithm of Vladu and Negruşeri; see
    # http://web.stanford.edu/class/cs97si/suffix-array.pdf

    L = sorted((a, i) for i, a in enumerate(A))
    n = len(A)
    count = 1
    while count < n:
        # Invariant: L is now a list of pairs such that L[i][1] is the
        # starting position in A of the i'th substring of length
        # 'count' in sorted order. (Where we imagine A to be extended
        # with dummy elements as necessary.)

        P = [0] * n
        for (r, i), (s, j) in zip(L, islice(L, 1, None)):
            P[j] = P[i] + (r != s)

        # Invariant: P[i] is now the position of A[i:i+count] in the
        # sorted list of unique substrings of A of length 'count'.

        L = sorted(chain((((P[i],  P[i+count]), i) for i in range(n - count)),
                         (((P[i], -1), i) for i in range(n - count, n))))
        count *= 2
    return [i for _, i in L]

def longest_common_prefix(s, suffix_arr):
    rank = [0] * len(suffix_arr)
    for i in range(len(suffix_arr)):
        rank[suffix_arr[i]] = i
    
    lcp = [-1] * len(suffix_arr)
    l = 0
    for i in range(len(suffix_arr)):
        k = rank[i]
        if k > 0:
            j = suffix_arr[k - 1]
            while j+l < len(s) and i+l < len(s) and s[j + l] == s[i + l]:
                l+=1
            lcp[k] = l
            if l > 0:
                l-=1
    return lcp, rank

length = len(s)
pi = generate_partial_match_table(s)
sa = suffix_array(s)
lcp, rank = longest_common_prefix(s, sa)

dp = [-1]*length

def recursive(index):
    global length
    if dp[index] != -1:
        return dp[index]
    else:
        ret = 1
        i = index+1
        while i < length:
            if lcp[i] >= length - sa[index]:
                ret += recursive(i)
                i += recursive(i)
            else:
                break
        dp[index] = ret
        return dp[index]

for i in range(length):
    recursive(i)

l_ans = [(len(s),1)]
prefix = pi[-1]
while prefix>0:
    index = rank[length-prefix]
    l_ans.append((prefix, dp[index]))
    prefix = pi[prefix-1]

print(len(l_ans))
for i,c in l_ans[::-1]:
    print("{} {}".format(i,c))