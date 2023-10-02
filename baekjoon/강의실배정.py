import heapq

n = int(input())

period = []
for i in range(n):
    start, end = map(int, input().split())
    period.append([start, end])

period.sort()

room = []
heapq.heappush(room, period[0][1])

for i in range(1, n):
    if period[i][0] < room[0]:
        heapq.heappush(room, period[i][1])
    else:
        heapq.heappop(room)
        heapq.heappush(room, period[i][1])

print(len(room))
