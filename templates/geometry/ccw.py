def ccw(p1, p2, p3):
    # p1 -> p2 -> p3 -> p1 is counter-clockwise
    # p1 = (x1,y1), p2 = (x2,y2), p3 = (x3,y3)
    x1,y1,x2,y2,x3,y3=p1[1],p1[0],p2[1],p2[0],p3[1],p3[0]
    return x1*y2+x2*y3+x3*y1-y1*x2-y2*x3-y3*x1<0

def is_convex(list_points):
    # list_points in ccw
    for i in range(len(list_points)):
        if not ccw(list_points[i], list_points[(i+1)%len(list_points)], list_points[(i+2)%len(list_points)]):
            return False
    return True

def is_inside(p, list_points, tol=1e-5):
    import math
    def dotproduct(v1, v2):
        return sum((a*b) for a, b in zip(v1, v2))

    def angle(v1, v2):
        return math.acos(dotproduct(v1,v2) / math.sqrt(dotproduct(v1, v1)*dotproduct(v2, v2)))

    sum_angle = 0
    for i in range(len(list_points)):
        v1 = [list_points[i][k]-p[k] for k in range(2)]
        v2 = [list_points[(i+1)%len(list_points)][k]-p[k] for k in range(2)]
        sum_angle += angle(v1, v2)

    return abs(sum_angle-2*math.pi) < tol

if __name__ == "__main__":
    assert is_convex([(0,0),(3,0),(3,3),(0,3)])
    assert not is_convex([(0,0),(2,2),(0,4),(1,2)])
    assert is_inside((1.5,2), [(0,0),(2,2),(0,4),(1,2)])
