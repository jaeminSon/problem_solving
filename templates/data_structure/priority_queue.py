from heapq import heappush, heappop

h = []
heappush(h, (5, 'write code'))
heappush(h, (7, 'release product'))
heappush(h, (1, 'write spec'))
heappush(h, (3, 'create tests'))
heappush(h, (1, 'create tests'))
assert heappop(h) == (1, 'create tests')
assert heappop(h) == (1, 'write spec') # compare with first elements and then second and so on


from queue import PriorityQueue
que = PriorityQueue()
que.put(4)
que.put(1)
que.put(7)
que.put(3)
assert que.get() == 1