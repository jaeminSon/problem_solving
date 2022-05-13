import sys

W, N = [int(el) for el in sys.stdin.readline().split()]

list_jewelry = []
for _ in range(N):
    weight, price = [int(el) for el in sys.stdin.readline().split()] 
    list_jewelry.append((weight, price))

list_jewelry = sorted(list_jewelry, key=lambda x:x[1], reverse=True)
total_price = 0
for jewelry in list_jewelry:
    weight, price = jewelry
    
    actual_weight = min(weight, W)
    total_price += actual_weight*price
    W-=actual_weight
    
    if W <= 0:
        break

    


print(total_price)