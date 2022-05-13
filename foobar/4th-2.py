def solution(dimensions, your_position, trainer_position, distance):
    w, h = dimensions

    max_w_repeat = distance//w + 2
    max_h_repeat = distance//h + 2

    def get_trainer_coord(index, length, ori_coord):
        if index % 2 == 0:
            return index * length + ori_coord
        else:
            return index * length + length - ori_coord

    def get_trainer_position(ori_trainer_position, width, height, index_w, index_h):
        ori_x, ori_y = ori_trainer_position
        new_x = get_trainer_coord(index_w, width, ori_x)
        new_y = get_trainer_coord(index_h, height, ori_y)
        return new_x, new_y        

    def dist(p1, p2):
        return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1./2)

    def gcd(large, small):
        if small == 0:
            return large
        else:
            return gcd(small, large % small)

    def slope(p1, p2):
        # (dx,dy) where dx dy are coprime
        dx = p1[0]-p2[0]
        dy = p1[1]-p2[1]

        abs_dx = abs(dx)
        abs_dy = abs(dy)
        divisor = gcd(max(abs_dx, abs_dy), min(abs_dx, abs_dy))
        
        if divisor !=0:
            return dx // divisor, dy // divisor
        else:
            return 0, 0

    def get_hit_slope(min_i_w, max_i_w, min_i_h, max_i_h, target_ori_coord, origin):
        dict_avail_directions = dict()
        for i_w in range(min_i_w, max_i_w+1):
            for i_h in range(min_i_h, max_i_h+1):
                new_coord = get_trainer_position(target_ori_coord, w, h, i_w, i_h)
                d = dist(new_coord, origin)
                if d <= distance:
                    s = slope(new_coord, origin)
                    min_distance = min(d, dict_avail_directions[s]) if s in dict_avail_directions else d
                    dict_avail_directions[s] = min_distance
        return dict_avail_directions

    dict_trainer_hit_slopes = get_hit_slope(-max_w_repeat, max_w_repeat, -max_h_repeat, max_h_repeat, trainer_position, your_position)
    dict_self_hit_slopes = get_hit_slope(-max_w_repeat, max_w_repeat, -max_h_repeat, max_h_repeat, your_position, your_position)
    set_perfect_hit_slopes = set()
    for slope, dist in dict_trainer_hit_slopes.items():
        if slope in dict_self_hit_slopes:
            if dict_self_hit_slopes[slope] > dict_trainer_hit_slopes[slope]:
                set_perfect_hit_slopes.add(slope)
        else:
            set_perfect_hit_slopes.add(slope)

    return len(set_perfect_hit_slopes)


if __name__=="__main__":

    print(solution([3,2], [1,1], [2,1], 4))
    print(solution([300,275], [150,150], [185,100], 500))
