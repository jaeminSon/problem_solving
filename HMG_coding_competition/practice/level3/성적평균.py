import sys

N, K = [int(el) for el in sys.stdin.readline().split()]
list_score = [int(el) for el in sys.stdin.readline().split()]
list_sum = []
running_sum = 0
for score in list_score:
    running_sum+=score
    list_sum.append(running_sum)

for _ in range(K):
    start, end = [int(el) for el in sys.stdin.readline().split()]
    print("{:.02f}".format(round(1.*(list_sum[end-1] - (list_sum[start-2] if start > 1 else 0))/(end-start+1), 2)))