import time

n = "1"*5000

st = time.time()
while len(n) > 0:
    n = n[:-1]
print("string truncation: ", time.time()-st)

st = time.time()
n = int("1"*5000)

while n > 0:
    n = n//2
print("int division: ", time.time()-st)
