import sys
sys.path.append("..")
from custom_type import STRING, LIST1D

from itertools import chain, islice
from bisect import bisect_left


"""
# radix sort slow due to overhead

def counting_sort(arr, exp):
    n = len(arr)
 
    count = [0] * 10
    for i in range(n):
        count[(arr[i] // exp) % 10] += 1
    
    for i in range(1, 10): 
        count[i] += count[i - 1]
 
    output = [0] * n
    for i in range(n-1, -1, -1):
        val = (arr[i] // exp) % 10
        output[count[val] - 1] = arr[i]
        count[val] -= 1

    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    max_val = max(arr) 
    exp = 1
    while max_val / exp > 1:
        counting_sort(arr, exp)
        exp *= 10

def update_orders_radix_sort(l):
    l_unique = list(set(l))
    radix_sort(l_unique)
    val2index = {v: i for i, v in enumerate(l_unique)}
    return [val2index[v] for v in l]

def str2int(string):
    return [ord(s) for s in string]

"""


def suffix_array(A):
    """
    suffix array of s
    O(n * log(n)^2)
    https://louisabraham.github.io/notebooks/suffix_arrays.html

    # string =     "banana"
    # index  =     [0, 1, 2, 3, 4, 5]
    # suffix_arr = [5, 3, 1, 0, 4, 2]
    # ----------------------------
    # suffix (ordered)    index   
    # ----------------------------
    # a                     5
    # ana                   3
    # anana                 1
    # banana                0
    # na                    4
    # nana                  2
    """
    # algorithm: page 5 in http://web.stanford.edu/class/cs97si/suffix-array.pdf

    # P: order of A[i,i+count] in substrings the length of count
    # L: ((P[i],P[i+count]) , start of substring)

    L = sorted((a, i) for i, a in enumerate(A))
    n = len(A)
    count = 1
    while count < n:

        P = [0] * n
        for (r, i), (s, j) in zip(L, islice(L, 1, None)):
            P[j] = P[i] + (r != s)

        L = sorted(chain((((P[i],  P[i+count]), i) for i in range(n - count)),
                         (((P[i], -1), i) for i in range(n - count, n))))
        count *= 2
    return [i for _, i in L]


def longest_common_prefix(s, suffix_arr):
    """
    # string =     "banana"
    # lcp: longest common prefix between sa[i] and sa[i-1]
    # --------------------------------------------------------------------------------------------------
    # suffix (ordered)    index     lcp                             rank (when alphabetically ordered)
    # --------------------------------------------------------------------------------------------------
    # a                     5        x                                3 (banana comes in 3rd place when ordered)      
    # ana                   3        1 ('a' and 'ana')                2 (anana comes in 2nd place when ordered)
    # anana                 1        3 ('ana' and 'anana')            5 (nana comes in 5th place when ordered)
    # banana                0        0 ('anana' and 'banana')         1 (ana comes in 1st place when ordered)
    # na                    4        0 ('banana' and 'na')            4 (na comes in 4th place when ordered)
    # nana                  2        2 ('na' and 'nana')              0 (a comes in 0th place when ordered)
    """
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
                l += 1
            lcp[k] = l
            if l > 0:
                l -= 1
    return lcp


def search(pattern: STRING, txt: STRING, suffix_arr: LIST1D) -> int:
    list_str = [txt[i:] for i in suffix_arr]
    index = suffix_arr[bisect_left(list_str, pattern)]
    if len(pattern)+index <= len(txt) and all([c == txt[i+index] for i, c in enumerate(pattern)]):
        return index
    else:
        return None


def longest_substring(txt: STRING, suffix_arr: LIST1D) -> STRING:
    # string =     "GATAGACA$"
    # index =      [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # suffix_arr = [8, 7, 5, 3, 1, 6, 4, 0, 2]
    # prev_suffix =[4, 3, 0, 5, 6, 7, 1, 8, -1]
    # plcp =       [2, 1, 0, 1, 0, 1, 0, 0, 0]
    prev_suffix = [0] * len(txt)
    prev_suffix[suffix_arr[0]] = -1
    for i in range(1, len(txt)):
        prev_suffix[suffix_arr[i]] = suffix_arr[i-1]

    plcp = [0] * len(txt)
    max_l = 0
    l = 0
    for i in range(len(txt)):
        if prev_suffix[i] == -1:
            plcp[i] = 0
        else:
            while txt[i+l] == txt[prev_suffix[i]+l]:
                l += 1
            plcp[i] = l
            if max_l < l:
                max_l = l
                lcp = txt[i:i+l]
            l = max(l-1, 0)  # plcp[i] >= plcp[i-1]-1

    return lcp


def longest_common_substring(concat_txt: STRING, suffix_arr: LIST1D) -> STRING:
    # concat_txt: <str1>$<str2>#
    prev_suffix = [0] * len(concat_txt)
    prev_suffix[suffix_arr[0]] = -1
    for i in range(1, len(concat_txt)):
        prev_suffix[suffix_arr[i]] = suffix_arr[i-1]

    index_split = concat_txt.index("$")

    plcp = [0] * len(concat_txt)
    max_l = 0
    l = 0
    for i in range(len(concat_txt)):
        if prev_suffix[i] == -1:
            plcp[i] = 0
        else:
            while concat_txt[i+l] == concat_txt[prev_suffix[i]+l]:
                l += 1
            plcp[i] = l
            if max_l < l and (index_split-i) * (index_split-prev_suffix[i]) < 0:
                max_l = l
                lcs = concat_txt[i:i+l]
            l = max(l-1, 0)  # plcp[i] >= plcp[i-1]-1

    return lcs


def suffix_array_alternative_naive(s):
    return [rank for _, rank in sorted((s[i:], i) for i in range(len(s)))]


if __name__ == "__main__":

    string = "GATAGACA$"
    suffix_arr = suffix_array(string)
    assert search("ACA", string, suffix_arr) == 5

    suffix_arr = suffix_array_alternative_naive("GATAGACA$")
    assert suffix_arr == [8, 7, 5, 3, 1, 6, 4, 0, 2]

    string = "BJAEMIsNLLJJAEMIsdfkj#"
    suffix_arr = suffix_array(string)
    assert longest_substring(string, suffix_arr) == "JAEMIs"

    string = "JAEMIN$MMJAEMIsdfkj#"
    suffix_arr = suffix_array(string)
    assert longest_common_substring(string, suffix_arr) == "JAEMI"

    assert longest_common_prefix("banana", suffix_array("banana")) == [-1, 1, 3, 0, 0, 2]
