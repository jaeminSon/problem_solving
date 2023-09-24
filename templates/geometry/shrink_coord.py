import sys
sys.path.append("..")
from custom_type import LIST1D, LIST2D


def shrink_coord_1d(l: LIST1D, s=0):
    l_unique_sorted = sorted(list(set(l)))
    mapping = {v: i+s for i, v in enumerate(l_unique_sorted)}
    return [mapping[el] for el in l]


def shrink_coord_2d(l: LIST2D, s=(0, 0)):
    mapping = [[] for _ in range(2)]
    for dim in range(2):
        unique_sorted = sorted(list(set([el[dim] for el in l])))
        mapping[dim] = {v: i+s[dim] for i, v in enumerate(unique_sorted)}
    return [[mapping[i][v] for i, v in enumerate(el)] for el in l]


if __name__ == "__main__":
    assert shrink_coord_1d([-1000, 0, 1000]) == [0, 1, 2]
    assert shrink_coord_1d([-1000, 0, 1000], 1) == [1, 2, 3]

    assert shrink_coord_2d(
        [[-1000, 3], [0, 5], [1000, -100]]) == [[0, 1], [1, 2], [2, 0]]
    assert shrink_coord_2d([[-1000, 3], [0, 5], [1000, -100]],
                           (1, 1)) == [[1, 2], [2, 3], [3, 1]]
