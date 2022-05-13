import sys

list_dct = [int(el) for el in sys.stdin.readline().split()]

set_order = set()
for index in range(len(list_dct)-1):
    if list_dct[index] > list_dct[index+1]:
        set_order.add("descending")
    else:
        set_order.add("ascending")
    

if len(set_order)==2:
    print("mixed")
else:
    print(set_order.pop())
