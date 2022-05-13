def area(list_points):
    def area_triangle(p1, p2):
        return (1./2) * (p1[0]*p2[1]-p1[1]*p2[0])
        
    s = 0
    for i in range(len(list_points)):
        s+=area_triangle(list_points[i], list_points[(i+1)%len(list_points)])
    
    return s
    
    
if __name__ == "__main__":
    print(area([(0,0),(3,0),(3,3),(0,3)]))