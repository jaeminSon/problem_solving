def solution(s):
    # Your code here
    length = len(s)
    
    def count_sallute(index_start, direction):
        n_meets = 0
        indices_to_check = range(index_start+1,length) if direction=="r" else range(0, index_start)
        for j in indices_to_check:
            if s[j] != "-" and s[index_start] != s[j]:
                n_meets+=1
        return n_meets
    
    count = 0
    for i in range(length):
        if s[i] == ">":
            count+=count_sallute(i, "r")
        elif s[i] == "<":
            count+=count_sallute(i, "l")
    return count

print(solution(">----<"))
print(solution("<<>><"))