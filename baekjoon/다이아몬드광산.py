import sys

R, C = [int(d) for d in sys.stdin.readline().rstrip().split()]

l = [[None]*C for _ in range(R)]
for i in range(R):
    line = sys.stdin.readline().rstrip()
    for j, v in enumerate(line):
        l[i][j] = int(v)

SW = [[0]*C for _ in range(R)]
NW = [[0]*C for _ in range(R)]

for i in range(R):
    for j in range(C):
        if l[i][j] == 0:
            NW[i][j] = 0
        elif i <=0 or j <= 0:
            NW[i][j] = 1
        else:
            NW[i][j] = NW[i-1][j-1]+1
        
        if l[R-i-1][j] == 0:
            SW[R-i-1][j] = 0
        elif i <= 0 or j <= 0:
            SW[R-i-1][j] = 1
        else:
            SW[R-i-1][j] = SW[R-i][j-1]+1

S = min(R, C)
for s in range((S+1)//2, 0, -1):
    max_index = 2*s-2
    for h in range(R-max_index):
        for w in range(C-max_index):
            if SW[h][s-1+w] >=s and NW[s-1+h][2*s-2+w] >=s and \
                SW[s-1+h][2*s-2+w] >=s and NW[2*s-2+h][s-1+w] >=s:
                print(s)
                exit(0)
print(0)

    

# complete search (takes long time for python)
# def exist(s):
#     max_index = 2*s-2
#     for dh in range(R-max_index):
#         for dw in range(C-max_index):
#             Found = True
#             for k in range(s):
#                 if l[k+dh][s-1+k+dw]!=1 or l[k+dh][s-1-k+dw]!=1:
#                     Found = False
#                     break
#             if not Found:
#                 continue
#             for k in range(s, 2*s-1):
#                 if l[k+dh][k-s+1+dw]!=1 or l[k+dh][3*s-3-k+dw]!=1:
#                     Found = False
#                     break
#             if Found:
#                 return True
# S = min(R, C)
# for s in range((S+1)//2, 0, -1):
#     if exist(s):
#         print(s)
#         exit(0)
# print(0)
