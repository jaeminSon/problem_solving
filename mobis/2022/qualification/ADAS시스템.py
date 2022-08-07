import sys
from heapq import heappush, heappop

UNIT_DIFF_TYPE = -1000**2+1
UNIT_DIFF_COORD = 1000

Score2Type = {0:"0", UNIT_DIFF_TYPE:"P", UNIT_DIFF_TYPE*2:"N"}

W, H  = [int(d) for d in sys.stdin.readline().rstrip().split()]
l = [[0]*H for _ in range(W)]
s = [[0]*H for _ in range(W)]
for i in range(W):
    row = sys.stdin.readline().rstrip()
    for j in range(H):
        l[i][j] = row[j]
        if row[j] == "P":
            s[i][j] = UNIT_DIFF_TYPE+i*UNIT_DIFF_COORD+j
        elif row[j] == "S":
            s[i][j] = UNIT_DIFF_TYPE*2+i*UNIT_DIFF_COORD+j
            S = (i,j)
        elif row[j] == "E":
            s[i][j] = UNIT_DIFF_TYPE*2+i*UNIT_DIFF_COORD+j
            E = (i,j)

score = 0
q = [(0,)+S+("S",)]
marked = set([S])
while True:
    _, i, j, t = heappop(q)
    if t == "0" or t == "P":
        for dx in range(-1, 2, 1):
            for dy in range(-1, 2, 1):
                if not (dx==0 and dy==0) and 0<=i+dx<W and 0<=j+dy<H and l[i+dx][j+dy]=="P":
                    score += 1
        if t=="P":
            score-=3
    
    if (i,j) == E:
        break
    
    for ne in [(i+dx,j+dy) for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)] if 0<=i+dx<W and 0<=j+dy<H and (i+dx,j+dy) not in marked]:
        heappush(q, (s[ne[0]][ne[1]], ne[0], ne[1], l[ne[0]][ne[1]]))
        marked.add(ne)

print(max(0,score))