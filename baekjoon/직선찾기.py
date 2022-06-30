import sys
from random import sample


N = int(sys.stdin.readline())
P = int(sys.stdin.readline())
points = [(10**9,10**9)] * N
for i in range(N):
    x, y = [int(el) for el in sys.stdin.readline().split()]
    points[i] = (x,y)

set_points = set(points)

if len(set_points) <= 2:
    print("possible")
else:
    indices = range(len(set_points))
    for _ in range(1000):
        p1, p2 = sample(set_points, 2)
        n = 0
        for i in range(N):
            if (p1[0]-p2[0])*(p2[1]-points[i][1])==(p2[0]-points[i][0])*(p1[1]-p2[1]):
                n+=1
                if n*100 >= P*N:
                    print("possible")
                    exit(0)
            
    print("impossible")
