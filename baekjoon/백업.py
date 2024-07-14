from heapq import heappush, heappop

n, k = map(int, input().split())
left = [0] * (n+2)
right = [1] * (n+2)
dist = [0] * (n+1)
pos = [0] * (n+2)
pos[-1] = n+1

for i in range(1, n+1):
    x = int(input())
    pos[i] = x
    left[i] = i-1
    right[i] = i+1
for i in range(1, n):
    dist[i] = pos[i+1] - pos[i]

pq = []
for i in range(1, n):
    heappush(pq, (dist[i], i, i+1))

ans = 0
while k > 0:
    d, l, r = heappop(pq)
    if 1 <= l <= n and 1 <= r <= n and left[r] == l and right[l] == r:
        ans += d
        k -= 1
        right[left[l]] = right[r]
        left[right[r]] = left[l]
        new_dist = dist[left[l]] + dist[r] - d
        dist[left[l]] = new_dist
        heappush(pq, (new_dist, left[l], right[r]))

print(ans)
