import sys

def max_rectangle(histogram):
    s = []
    max_area = 0
    for i in range(len(h)):
        if s and h[s[-1]] > h[i]:
            while s and h[s[-1]] > h[i]:
                x = s.pop()
                w = i-(s[-1]+1) if s else i
                max_area = max(max_area, h[x] * w)
        s.append(i)
        
    while s:
        x = s.pop()
        w = len(h)-(s[-1]+1) if s else len(h)
        max_area = max(max_area, h[x] * w)
    
    return max_area


while True:
    h = [int(d) for d in sys.stdin.readline().rstrip().split()]
    if h[0]==0:
        break
    h = h[1:]
    print(max_rectangle(h))
    
    