import numpy as np

# N = 500
# H = 128
# W = 128
# C = 2

N = 20
H = 10
W = 10
C = 3

print("{} {} {}".format(N, H, W))

for _ in range(H):
    row = []
    for _ in range(W):
        row.append(np.random.randint(C))
    print(" ".join([str(el) for el in row]))


for _ in range(N):
    row = [np.random.randint(1, H+1), np.random.randint(1, W+1), np.random.randint(C)]
    print(" ".join([str(el) for el in row]))
