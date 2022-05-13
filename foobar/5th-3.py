def solution(g):
    h = len(g)
    w = len(g[0])

    def legitimate(val, list_cell):
        if val:
            if sum([el for el in list_cell])==1:
                return True
            else:
                return False
        else:
            if sum([el for el in list_cell])!=1:
                return True
            else:
                return False


    def get_preimages(col):
        list_preimages = []
        len_preimage = 2*len(col)+2

        stack = [[0, 0], [0, 1], [1, 0], [1, 1]]
        while stack:
            el = stack.pop()
            if len(el)==len_preimage:
                list_preimages.append(el)
            else:
                for new_el in [[0, 0], [0, 1], [1, 0], [1, 1]]:
                    val = col[len(el)//2-1]
                    if legitimate(val, el[-2:] + new_el):
                        stack.append(el + new_el)
        return list_preimages

    def get_right_val(preimage):
        return "".join([str(el) for el in preimage[1::2]])
        
    def get_left_val(preimage):
        return "".join([str(el) for el in preimage[0::2]])
    

    list_image_val = []
    for i_w in range(w):
        preimages = get_preimages([g[i][i_w] for i in range(h)])
        left_vals = [get_left_val(preimage) for preimage in preimages]
        right_vals = [get_right_val(preimage) for preimage in preimages]
        list_image_val.append(list(zip(left_vals, right_vals)))

    
    dp_front = {}
    for lv, rv in list_image_val[0]:
        dp_front[rv] = dp_front.get(rv, 0) + 1
    for i_w in range(1, w):
        new_dp_front = {}
        for lv, rv in list_image_val[i_w]:
            if lv in dp_front:
                new_dp_front[rv] = new_dp_front.get(rv, 0) + dp_front[lv] 
        dp_front = new_dp_front
    
    return sum([el for el in dp_front.values()])

if __name__=="__main__":
    print(solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]))
    print(solution([[True, False, True], [False, True, False], [True, False, True]]))
    print(solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]]))
