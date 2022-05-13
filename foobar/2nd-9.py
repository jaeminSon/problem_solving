def solution(src, dest):
    
    def board2coord(val):
        return (val//8, val%8)
    
    def inbound(y, x):
        return 0<=y and y<8 and 0<=x and x<8 
    
    dict_board2coord = {}
    dict_coord2board = {}
    for i in range(64):
        coord = board2coord(i)
        dict_board2coord[i] = coord
        dict_coord2board[coord] = i
    
    s_coord = dict_board2coord[src]
    d_coord = dict_board2coord[dest]
    visited = set()
    q = [(s_coord)+ (0,)]
    
    while q:
        el = q[0]
        q = q[1:] # pop in fifo queue
        y,x,d = el
        if (y,x)==d_coord:
            return d
        for dy, dx in [(-1, 2), (1, 2), (-1, -2), (1, -2), (2, -1), (2, 1), (-2, -1), (-2, 1)]:
            cand_y = y+dy
            cand_x = x+dx
            if inbound(cand_y, cand_x) and (cand_y, cand_x) not in visited:
                visited.add((cand_y, cand_x))
                q.append((cand_y, cand_x, d+1))
        
    
    

if __name__ == "__main__":
    print(solution(0, 1))
    # 3

    print(solution(19, 36))
    # 1