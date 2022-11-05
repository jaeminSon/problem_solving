import sys

N = int(sys.stdin.readline().rstrip())

l = [int(d) for d in sys.stdin.readline().rstrip().split()]

l_unique_sorted = sorted(list(set(l)))
val2rank = {v:i for i, v in enumerate(l_unique_sorted)}
print(" ".join([str(el) for el in [val2rank[el] for el in l]]))