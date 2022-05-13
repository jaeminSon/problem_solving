def solution(area):
    
    list_side = []
    while area > 0:
        side = int(area ** (1./2))
        list_side.append(side**2)
        area -= side**2
        
    return list_side

if __name__ == "__main__":
    print(solution(15324))
    # 15129,169,25,1

    print(solution(12))
    # 9,1,1,1
