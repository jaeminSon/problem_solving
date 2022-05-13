def solution(h, q):
    
    def query(h, el):
        if el == 2**h-1:
            return -1
        elif el==2**(h-1)-1 or el==2**h-2:
            return 2**h - 1
        else:
            if el>=2**(h-1):
                return 2**(h-1)-1 + query(h-1, el-2**(h-1)+1)
            else:
                return query(h-1, el)
    
    list_ans = []
    for el in q:
        ans = query(h, el)
        list_ans.append(ans)
    
    return list_ans
    
    

if __name__ == "__main__":
    print(solution(3, [5]))
    print(solution(3, [7, 3, 5, 1]))
    # -1,7,6,3
    print(solution(5, [19, 14, 28]))
    # 21,15,29
    