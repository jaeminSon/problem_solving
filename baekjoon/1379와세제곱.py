import sys

N = int(sys.stdin.readline().rstrip())
problems = [sys.stdin.readline().rstrip() for _ in range(N)]

mapping = {"1":"1", "3":"7", "7":"3", "9":"9"}

for s in problems:
    if len(s)==1:
        print(mapping[s])
    else:
        candidates = [mapping[s[-1]]]
        notFound = True
        while candidates and notFound:
            cand = candidates.pop()
            for i in range(10):
                val = i*(10**len(cand))+int(cand)
                if s[-len(cand)-1:] == str((val)**3)[-len(cand)-1:].zfill(len(cand)+1):
                    if len(cand)+1 == len(s):
                        print(val)
                        notFound = False
                        break
                    else:
                        candidates.append(str(val).zfill(len(cand)+1))
            
