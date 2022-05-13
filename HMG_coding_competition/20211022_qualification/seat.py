import sys

N,M,Q = [int(el) for el in sys.stdin.readline().split()]

set_all_seats = set([(i,j) for i in range(1, N+1) for j in range(1, M+1)])
set_occupied_seats = set()
set_eating = set()
set_finished = set()
dict_uid2seat = {}

def get_seat(set_all_seats, set_occupied_seats):

    if set_occupied_seats:
        set_avail_seats = set_all_seats - set_occupied_seats
        for occupied_seat in set_occupied_seats:
            for d in [(-1,0), (1,0), (0,-1), (0,1)]:
                set_avail_seats -= set([(occupied_seat[0]+d[0], occupied_seat[1]+d[1])])
        if set_avail_seats:
            list_seat_dist = []
            for coord in set_avail_seats:
                dist = min([(c[0]-coord[0])**2+(c[1]-coord[1])**2 for c in set_occupied_seats])
                list_seat_dist.append((coord, dist))
            return max(list_seat_dist, key=lambda x:x[1])[0]
        else:
            return (-1, -1)

    else:
        return (1,1)
    
for _ in range(Q):
    prompt, uid = sys.stdin.readline().split()
    if prompt == "In":
        if uid in set_eating:
            print("{} already seated.".format(uid))
        elif uid in set_finished:
            print("{} already ate lunch.".format(uid))
        else:
            x, y = get_seat(set_all_seats, set_occupied_seats)
            if x!=-1 and y!=-1:
                print("{} gets the seat ({}, {}).".format(uid, x, y))
                set_eating.add(uid)
                set_occupied_seats.add((x,y))
                dict_uid2seat[uid] = (x,y)
            else:
                print("There are no more seats.")
    elif prompt == "Out":
        if uid not in set_eating and uid not in set_finished:
            print("{} didn't eat lunch.".format(uid))
        elif uid in set_finished:
            print("{} already left seat.".format(uid))
        elif uid in set_eating:
            x, y = dict_uid2seat[uid]
            print("{} leaves from the seat ({}, {}).".format(uid, x, y))
            dict_uid2seat.pop(uid)
            set_occupied_seats.remove((x,y))
            set_eating.remove(uid)
            set_finished.add(uid)

