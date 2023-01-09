from bisect import bisect_left
from itertools import zip_longest, islice

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

def suffix_array(s):
    """
    suffix array of s
    O(n * log(n)^2)
    https://louisabraham.github.io/notebooks/suffix_arrays.html
    """
    def update_orders(l):
        val2index = {v: i for i, v in enumerate(sorted(set(l)))}
        return [val2index[v] for v in l]

    orders = update_orders(s)
    
    k = 1
    n = len(s)
    while max(orders) < n - 1:
        orders = update_orders(
            [a * (n + 1) + b + 1
             for (a, b) in
             zip_longest(orders, islice(orders, k, None),
                         fillvalue=0)])
        k <<= 1
    
    index2val = {v:i for i, v in enumerate(orders)}
    return [index2val[i] for i in range(n)]
 
def search(pattern, txt, suffix_arr):
    list_str = [txt[i:] for i in suffix_arr]
    index = suffix_arr[bisect_left(list_str, pattern)]
    if len(pattern)+index <= len(txt) and all([c==txt[i+index] for i, c in enumerate(pattern)]):
        return index
    else:
        return None

def longest_common_substring(concat_txt, suffix_arr):
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
                l+=1
            plcp[i] = l
            if max_l < l and (index_split-i) * (index_split-prev_suffix[i]) < 0:
                max_l = l
                lcp = concat_txt[i:i+l]
            l = max(l-1, 0) # plcp[i] >= plcp[i-1]-1
    
    return lcp

def suffix_array_alternative_naive(s):
    return [rank for _, rank in sorted((s[i:], i) for i in range(len(s)))]

if __name__ == "__main__":
     
    string = "GATAGACA$"
    suffix_arr = suffix_array(string)
    assert search("ACA", string, suffix_arr) == 5
    
    suffix_arr = suffix_array_alternative_naive("GATAGACA$")
    assert suffix_arr == [8, 7, 5, 3, 1, 6, 4, 0, 2]
    

    string = "JAEMIN$MMJAEMIsdfkj#"
    suffix_arr = suffix_array(string)
    assert longest_common_substring(string, suffix_arr) == "JAEMI"