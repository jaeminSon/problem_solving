def KMP(pattern, txt):
 
    table = generate_partial_match_table(pattern)
 
    i = 0
    j = 0
    while i < len(txt):
        if pattern[j] == txt[i]:
            i += 1
            j += 1
            if j == len(pattern):
                return i-j
            if i >= len(txt):
                return None
        else:
            if j != 0: # check if previous match could be used
                j = table[j-1]
            else:
                i += 1
 
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

if __name__ == "__main__":
    print(KMP("ABABCABAB", "ABABDABACDABABCABAB"))
    print(KMP("K", "ABABDABACDABABCABAB"))
 