import sys
import heapq
input = sys.stdin.readline

n = int(input())

period = []
for _ in range(n):
    start, end = map(int, input().split())
    heapq.heappush(period, (end, start))

ans = 0
now = 0
while period:
    end, start = heapq.heappop(period)
    if start >= now:
        now = end
        ans += 1

print(ans)
