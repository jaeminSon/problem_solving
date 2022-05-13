def solution(l):
    
    def list2int(l):
        return int("".join([str(el) for el in l]))

    def get_best(l):
        if sum(l) % 3 == 0:
            return list2int(sorted(l, reverse=True))
        else:
            if len(l)==1:
                return 0
            else:
                l_cand = []
                for i in range(len(l)):
                    val = get_best(l[:i] + l[i+1:])
                    l_cand.append(val)
                return max(l_cand)

    res = get_best(l)

    return res
    
    

if __name__ == "__main__":
    print(solution([3, 1, 4, 1]))
    # 4311

    print(solution([3, 1, 4, 1, 5, 9]))
    # 94311

    print(solution([4]))
