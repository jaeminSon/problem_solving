n = int(input())

rsum = [0] * 100_001
lsum = [0] * 100_001
imos = [0] * 100_001
period = []
for i in range(n):
    s, e = map(int, input().split())
    rsum[s] += 1
    lsum[e] += 1
    imos[s] += 1
    imos[e] -= 1
    period.append((s, e))

economic = 0
for i in range(1, 100_000):
    imos[i] += imos[i-1]
    economic = max(economic, imos[i])

for i in range(99_999, 0, -1):
    rsum[i] += rsum[i+1]

for i in range(1, 100_000):
    lsum[i+1] += lsum[i]

min_exclude = n
for s, e in period:
    min_exclude = min(min_exclude, lsum[s] + rsum[e])

lavish = n - min_exclude

print(f"{lavish} {economic}")
