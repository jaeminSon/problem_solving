from collections import Counter


def solution(x, y):
    if len(x)>len(y):
        c = Counter(x) - Counter(y)
    else:
        c = Counter(y) - Counter(x)
        
    return [l for l in c.elements()][0]
        
if __name__ == "__main__":
    print(solution([13, 5, 6, 2, 5], [5, 2, 5, 13]))
    # 6

    print(solution([14, 27, 1, 4, 2, 50, 3, 1], [2, 4, -4, 3, 1, 1, 14, 27, 50]))
    # -4
