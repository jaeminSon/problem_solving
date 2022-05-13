import sys


def intersection_two_lines(a1,b1,c1,a2,b2,c2):
    # a1x+b1y+c1=0
    # a2x+b2y+c2=0
    d = a1*b2-a2*b1
    if abs(d) < sys.float_info.epsilon: # parallel
        return float('inf')
    else:
        return (1.*(c2*b1-c1*b2)/d, 1.*(a2*c1-c2*a1)/d) # (x,y)
    
def intersection_two_segments(x1, y1, x2 ,y2, x3, y3, x4, y4):
    # segment (x1, y1)-(x2, y2) and (x3, y3)-(x4, y4)
    def points2line(x1,y1,x2,y2):
        a = y1-y2
        b = x2-x1
        c = -a*x1 - b*y1
        return a,b,c # ax+by+c=0
    
    a1,b1,c1 = points2line(x1,y1,x2,y2)
    a2,b2,c2 = points2line(x3,y3,x4,y4)

    d = a1*b2-a2*b1
    if abs(d) < sys.float_info.epsilon: # parallel
        if min(x1,x2) > max(x3, x4) or max(x1,x2) < min(x3, x4):
            return None
        elif abs(min(x1,x2) - max(x3, x4)) < sys.float_info.epsilon:
            return (x1, y1) if x1 < x2 else (x2, y2)
        elif abs(max(x1,x2) - min(x3, x4)) < sys.float_info.epsilon:
            return (x1, y1) if x1 > x2 else (x2, y2)
        else:
            return float('inf')
    else:
        x = 1.*(c2*b1-c1*b2)/d
        y = 1.*(a2*c1-c2*a1)/d
        if min(x1,x2) - sys.float_info.epsilon < x and x < max(x1,x2) + sys.float_info.epsilon:
            return x, y
        else:
            return None

def circle_line(cx,cy,r_square,a,b,c):
    # cicle: (x-cx)^2+(y-cy)^2=r^2
    # line: ax+by+c=0
    r = r_square**(0.5)
    c-=cx*a+cy*b # move (cx,cy) to (0,0)
    
    sum_a_b_squre = (a**2+b**2)
    x0 = -a*c/sum_a_b_squre
    y0 = -b*c/sum_a_b_squre
    d_square = r**2-c**2/sum_a_b_squre
    m = (d_square/sum_a_b_squre)**(0.5)
    return (x0+b*m+cx,y0-a*m+cy), (x0-b*m+cx,y0+a*m+cy) # move (0,0) back to (cx,cy)
    
def two_circles(cx1,cy1,r1_square,cx2,cy2,r2_square):
    # cicle 1: (x-cx1)^2+(y-cy1)^2=r1^2
    # cicle 2: (x-cx2)^2+(y-cy2)^2=r2^2
    # move (cx1,cy1) to (0,0)
    cx2 -= cx1
    cy2 -= cy1
    
    a=-2*cx2
    b=-2*cy2
    c=cx2**2+cy2**2+r1_square-r2_square 
    
    intersections = circle_line(0,0,r1_square, a,b,c)
    return [(p[0]+cx1, p[1]+cy1) for p in intersections]
    
if __name__ == "__main__":
    assert intersection_two_lines(1,1,1,1,-1,1) == (-1,0)
    assert intersection_two_segments(0,0,1,1,0,1,1,0) == (0.5,0.5)
    assert all([abs((p[0]**2+p[1]**2)-18) < (sys.float_info.epsilon)**(0.5) for p in circle_line(0,0,18, 1,1,0)])
    assert all([p==(3,0) for p in two_circles(0,0,9, 1,0,4)])