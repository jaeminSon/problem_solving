import sys

N = int(sys.stdin.readline().rstrip())

l = [ch for ch in sys.stdin.readline().rstrip()]

index_i = [i for i, el in enumerate(l) if el=="I"]

def isvalid(v):
    if v > len(index_i):
        return False
    else:
        index_i_thresh = index_i[-v]
        count_first = 0
        count_second = 0
        count_complete = 0
        for i in range(N):
            if l[i] == "J":
                count_first += 1
            elif l[i] == "I" and i < index_i_thresh:
                count_first += 1
            elif l[i] == "O" and count_first > 0:
                count_first -= 1
                count_second += 1
            elif l[i] == "I" and i >= index_i_thresh and count_second > 0:
                count_second -= 1
                count_complete += 1

        return v==count_complete


ans = 0
lo, hi = 1, N
while lo <= hi:
    mid = (lo + hi) // 2
    if isvalid(mid):
        ans = mid
        lo = mid + 1
    else:
        hi = mid - 1

print(ans)