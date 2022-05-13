def solution(s):
    # Your code here
    length = len(s)
    if length==1:
        return 1
    else:
        chunk_cand = [i for i in range(1, length//2+1) if length%i==0]
        for len_chunk in chunk_cand:
            n_chunk = length//len_chunk
            if all([s[:len_chunk]==s[i*len_chunk:(i+1)*len_chunk] for i in range(n_chunk)]):
                return n_chunk * solution(s[:len_chunk])
        return 1

print(solution("zzzzz"))
