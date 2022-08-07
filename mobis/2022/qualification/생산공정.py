import sys

sys.setrecursionlimit(500_000)

DEFAULT_STR = "Z"*11

root = [{}, DEFAULT_STR, 0] # children, most-frequent-word, count-most-frequent-word

def insert(word):
    node = root
    for char in word:
        if char in node[0]:
            node = node[0][char]
        else:
            new_node = [{}, DEFAULT_STR, 0]
            node[0][char] = new_node
            node = new_node
    node[1] = word
    node[2] += 1
    
def dp(node):
    for ch in node[0].values():
        w, c = dp(ch)
        if c > node[2] or (c == node[2] and w < node[1]):
            node[1] = w
            node[2] = c
    return node[1], node[2]
        
def query(x):
    node = root
    
    for char in x:
        if char in node[0]:
            node = node[0][char]
        else:
            return 0
    
    return "{} {}".format(node[1], node[2])
    
    

N = int(sys.stdin.readline().rstrip())
for _ in range(N):
    insert(sys.stdin.readline().rstrip())

dp(root)

K = int(sys.stdin.readline().rstrip())
queries = [sys.stdin.readline().rstrip() for _ in range(K)]
for q in queries:
    print(query(q))
        
    
