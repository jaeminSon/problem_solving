def stern_brocot_seq(n):
    assert n > 0 and sum([int(c) for c in bin(n + 1)[2:]]) == 1
    
    seq = [1]
    for i in range(n//2):
        seq.append(seq[i])
        seq.append(seq[i]+seq[i+1])
        
    return list(zip(seq, seq[::-1]))

def farey_seq(n):
    return [(0,1)] + [el for el in stern_brocot_seq(2**n-1)[:2**(n-1)] if el[0] <=n and el[1] <= n]

if __name__ == "__main__":
    print(stern_brocot_seq(1))
    print(stern_brocot_seq(3))
    print(stern_brocot_seq(7))

    print(farey_seq(1))
    print(farey_seq(2))
    print(farey_seq(3))
    print(farey_seq(7))