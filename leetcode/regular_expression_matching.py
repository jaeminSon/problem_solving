class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        n = len(s)
        l = []
        star_consecutive = False
        for c in p:
            if c=="*":
                if not star_consecutive:
                    l.append(c)
                star_consecutive = True
            else:
                l.append(c)
                star_consecutive = False
                
        p = "".join(l)
        m = len(p)
        
        
        dp = [[None]*m for _ in range(n)]
        
        def _recursive(i,j):
            if j == m:
                return i == n
            elif i == n:
                if p[j]=="*":
                    return _recursive(i, j+1)
                elif j<m-1 and p[j+1]=="*":
                    return _recursive(i, j+2)
                else:
                    return j == m
            elif dp[i][j] is not None:
                return dp[i][j]
            else:
                if p[j] == "*":
                    if p[j-1]=="." or s[i]==p[j-1]: # char match
                        dp[i][j] = _recursive(i,j+1) or _recursive(i+1,j) or _recursive(i+1,j+1)
                    else: # char no-match (ignore asterisk and proceed j)
                        dp[i][j] = _recursive(i,j+1)
                elif j<m-1 and p[j+1]=="*": # next is asterisk (then, push j)
                        dp[i][j] = _recursive(i, j+1)
                elif p[j] == ".":
                    dp[i][j] = _recursive(i+1,j+1)
                else:
                    dp[i][j] = (s[i]==p[j] and _recursive(i+1, j+1))
                return dp[i][j]

        return _recursive(0,0)

print(Solution().isMatch("a", "ab*"))
print(Solution().isMatch("ab", ".*c"))
print(Solution().isMatch("ab", ".*.."))
print(Solution().isMatch("ab", ".**.."))
