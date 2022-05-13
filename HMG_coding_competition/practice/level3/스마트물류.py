import sys

N, K = [int(el) for el in sys.stdin.readline().split()]

list_H = []
list_P = []
for index, ch in enumerate(sys.stdin.readline().rstrip()):
    if ch == "H":
        list_H.append(index)
    elif ch == "P":
        list_P.append(index)

count = 0
index_H = 0
index_P = 0
while index_H < len(list_H) and index_P < len(list_P):
    if list_H[index_H] > list_P[index_P] + K:
        index_P += 1
    elif list_H[index_H] + K < list_P[index_P]:
        index_H += 1
    else:
        index_H += 1
        index_P += 1
        count += 1

print(count)
