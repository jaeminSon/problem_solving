N, S = map(int, input().split())


def possible(N, S):
    if N < 3:
        return False
    elif N == 3:
        return S == 1
    else:
        l_tree = [({2: 1, 1: 2}, 1)]
        for _ in range(4, N+1):
            new_l_tree = []
            set_s = set()
            for counter, s in l_tree:
                for k in counter.keys():
                    new_counter = {k: v for k, v in counter.items()}
                    if k+1 in new_counter:
                        new_counter[k+1] += 1
                    else:
                        new_counter[k+1] = 1
                    new_counter[k] -= 1
                    if new_counter[k] == 0:
                        new_counter.pop(k)
                    new_counter[1] += 1

                    if s+k not in set_s:
                        new_l_tree.append((new_counter, s+k))
                        set_s.add(s+k)

            l_tree = new_l_tree
        
        return S in [s for _, s in l_tree]


if possible(N, S):
    print(1)
else:
    print(0)
