import sys

n_limit, n_test = [int(el) for el in sys.stdin.readline().split()]

def extract_speed_info_from_std(n_rows):
    l = []
    curr_height = 0
    for _ in range(n_rows):
        limit_height, limit_speed = [int(el) for el in sys.stdin.readline().split()]
        l.append((curr_height, curr_height + limit_height, limit_speed))
        curr_height += limit_height
    return l

list_limit = extract_speed_info_from_std(n_limit)
list_test = extract_speed_info_from_std(n_test)

index_limit = 0
curr_max = 0
for test_el in list_test:
    start_height, end_height, speed = test_el
    while list_limit[index_limit][1] <= start_height:
        index_limit+=1
    
    index_delta_overlap = 0
    while index_limit+index_delta_overlap < len(list_limit) and list_limit[index_limit+index_delta_overlap][0] < end_height:
        curr_diff = speed - list_limit[index_limit+index_delta_overlap][2]
        curr_max = max(curr_max, curr_diff)
        index_delta_overlap+=1

print(curr_max)