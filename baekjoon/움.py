MOD = 10**9+7

def find_codon(codon, start):
    ptr = 0
    for i in range(start, len(dna)):
        if codon[ptr] == dna[i]:
            ptr += 1
            if ptr == 3: 
                return i
    return len(dna)

def compute_combinations(lookup):
    dp = [1] + [0]*len(dna)
    for i in range(len(dna)):
        for codons in lookup.values():
            min_index = min(find_codon(codon, i) for codon in codons)
            if min_index != len(dna): 
                dp[min_index+1] = (dp[min_index+1]+dp[i]) % MOD
    return (sum(dp)-1) % MOD

dna = input()
m = int(input())
lookup = {}
for _ in range(m):
    codon, amino = input().split()
    lookup.setdefault(amino, []).append(codon)

print(compute_combinations(lookup))