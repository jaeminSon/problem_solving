import sys

M = int(sys.stdin.readline().rstrip())

K = int(sys.stdin.readline().rstrip())

l = [int(d) for d in sys.stdin.readline().rstrip().split()]

LEN_DP = 1_002_000
LEN_BRUTE_THRESH = 1_000
LEN_CYCLE = 1_000

win = [False]*LEN_DP
for i in range(LEN_DP):
    for el in l:
        if el > i:
            break
        else:
            win[i] = win[i] or (not win[i-el])

if M < LEN_BRUTE_THRESH:
    print(sum([not win[i] for i in range(1, M+1)]))
else:
    for d in range(1, LEN_CYCLE+1):
        has_cycle = True
        for i in range(LEN_BRUTE_THRESH+1, LEN_BRUTE_THRESH+LEN_CYCLE+1):
            if win[i]!=win[i+d]:
                has_cycle = False
                break

        if has_cycle:
            len_cycle = d
            break

    head = sum([not win[i] for i in range(1, LEN_BRUTE_THRESH+1)])
    middle = sum([not win[i] for i in range(LEN_BRUTE_THRESH+1, LEN_BRUTE_THRESH+len_cycle+1)]) * ((M-LEN_BRUTE_THRESH) // len_cycle)
    tail = sum([not win[i] for i in range(LEN_BRUTE_THRESH+1 , LEN_BRUTE_THRESH + (M-LEN_BRUTE_THRESH) % len_cycle + 1)])

    print(head + middle + tail)