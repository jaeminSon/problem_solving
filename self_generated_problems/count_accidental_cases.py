from itertools import permutations

# [0, 2, 1, 3] ok (index sort: [0, 2, 1, 3])
# [1, 3, 0, 2] not ok (index sort: [2, 0, 3, 1])

# solution
sol = [1, 2]
for n in range(3, 11):
    sol.append(sol[-1]+(n-1)*sol[-2])

# test
for n in range(1,  11):
    n_no_matching_elem = []
    match = 0
    for l in permutations(range(n)):
        l_sorted = sorted(l)
        val2rank = {l_sorted[i] : i for i in range(len(l_sorted))}
        l1 = [val2rank[el] for el in l]

        ind = sorted(range(len(l)), key=lambda i:l[i])
        val2rank = {l[i]:r for i,r in enumerate(ind)}
        l2 = [val2rank[el] for el in l]
        
        if l1==l2:
            match+=1
            base = list(range(len(l)))
            n_no_matching_elem.append(sum([base[i]!=l[i] for i in range(len(l))]))

    assert sol[n-1] == match
