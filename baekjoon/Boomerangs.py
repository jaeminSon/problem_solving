import sys
from collections import defaultdict
from sys import stdin
input = stdin.readline
sys.setrecursionlimit(10_000_000)


def dfs(curr):
    visited[curr] = True
    cand = None
    for ch in adj[curr]:
        if not visited[ch]:
            remained = dfs(ch)
            if remained:
                boomerangs.append((remained, ch, curr))
            else:
                if cand:
                    boomerangs.append((cand, curr, ch))
                    cand = None
                else:
                    cand = ch

    return cand


def get_root(k):
    if parent[k] != k:
        parent[k] = get_root(parent[k])
    return parent[k]


N, M = map(int, input().split())

original = {i: i for i in range(N+M+1)}
parent = [i for i in range(N+M+1)]

adj = defaultdict(dict)
for _ in range(M):
    u, v = map(int, input().split())
    r_u = get_root(u)
    r_v = get_root(v)
    if r_u == r_v:
        N += 1
        original[N] = v
        v = N
    else:
        parent[r_u] = r_v
    adj[u].update({v: 1})
    adj[v].update({u: 1})

boomerangs = []

visited = [False]*(N+1)
for i in range(N+1):
    if not visited[i]:
        dfs(i)

print(len(boomerangs))
for sol in boomerangs:
    u, v, w = sol
    print(f"{original[u]} {original[v]} {original[w]}")
