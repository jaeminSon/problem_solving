from itertools import combinations

def solution(num_buns, num_required):
    n_appear = num_buns + 1 - num_required

    list_list_key = [[] for _ in range(num_buns)]
    for index, comb in enumerate(combinations(range(num_buns), n_appear)):
        for el in comb:
            list_list_key[el].append(index)

    return list_list_key


if __name__=="__main__":
    print(solution(2, 1))
    print(solution(5, 3))
    print(solution(4, 4))
