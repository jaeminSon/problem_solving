def solution(xs):
    
    if len(xs)==1:
        return str(xs[0])
    else:
        list_neg = []
        mul = 1
        for x in xs:
            if abs(x) >= 1 :
                mul *= x
            if x < 0:
                list_neg.append(x)

        if mul > 0:
            return str(mul)
        else:
            if len(list_neg) == 1:
                return str(max(xs))
            else:   
                max_neg = max(list_neg)
                return str(mul // max_neg)


if __name__ == "__main__":
    print(solution([2, 0, 2, 2, 0]))
    # 8
    print(solution([-2, -3, 4, -5]))
    # 60
    print(solution([-4]))
    print(solution([-4, 0]))
    