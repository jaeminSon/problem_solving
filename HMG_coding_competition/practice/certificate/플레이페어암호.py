import sys

s = sys.stdin.readline().rstrip()
e = sys.stdin.readline().rstrip()

pairs = []
i = 0
while i < len(s):
    if i==len(s)-1:
        pairs.append((s[i], "X"))
        i+=1
    else:
        if s[i] == s[i+1]:
            if s[i] == s[i+1] == "X":
                pairs.append(("X","Q"))
                i+=1
            else:
                pairs.append((s[i],"X"))
                i+=1
        else:
            pairs.append((s[i],s[i+1]))
            i+=2

alphabet = "abcdefghiklmnopqrstuvwxyz".upper()
matrix = [["a"]*5 for _ in range(5)]
set_appear = set([])
n = 0
for el in e + alphabet:
    if el not in set_appear:
        matrix[n//5][n%5] = el
        n+=1
        set_appear.add(el)

dict_coord = {matrix[i//5][i%5]:(i//5, i%5) for i in range(25)}

ans = ""
for c1,c2 in pairs:
    coord_c1_y, coord_c1_x = dict_coord[c1]
    coord_c2_y, coord_c2_x = dict_coord[c2]
    if coord_c1_y==coord_c2_y:
        ans+=matrix[coord_c1_y][(coord_c1_x+1)%5]
        ans+=matrix[coord_c2_y][(coord_c2_x+1)%5]
    elif coord_c1_x==coord_c2_x:
        ans+=matrix[(coord_c1_y+1)%5][coord_c1_x]
        ans+=matrix[(coord_c2_y+1)%5][coord_c2_x]
    else:
        ans+=matrix[coord_c1_y][coord_c2_x]
        ans+=matrix[coord_c2_y][coord_c1_x]

print(ans)