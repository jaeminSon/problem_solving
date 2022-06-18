class Solution:
    def strongPasswordChecker(self, password: str) -> int:
        
        MAX_CHAR = 20
        
        n = len(password)
        
        def get_n_reapts(s):
            l = []
            i = 2
            while i<len(s):
                if s[i] == s[i-1] == s[i-2]:
                    r = 2
                    while i<len(s) and s[i]==s[i-1]:
                        r+=1
                        i+=1
                    l.append(r)
                else:
                    i+=1
                
            return l
            
        def count_missing_type(password):
            return 3 - int(any([c.islower() for c in password])) \
                     - int(any([c.isupper() for c in password])) \
                     - int(any([c.isdigit() for c in password]))
        
        if n<=4:
            return 6-n
        else:
            list_repeats = get_n_reapts(password)
            n_missing_type = count_missing_type(password)
            if n==5:
                if len(list_repeats) > 0:
                    return max(n_missing_type, 2 if list_repeats[0]==5 else 1)
                else:
                    return max(n_missing_type, 1)
            elif 6 <= n and n <= MAX_CHAR:
                if len(list_repeats) > 0:
                    return max(n_missing_type, sum([r//3 for r in list_repeats]))
                else:
                    return n_missing_type
            elif n > MAX_CHAR:
                if len(list_repeats) > 0:
                    list_dec = []
                    for r in list_repeats:
                        list_dec.append((r%3+1)%3)
                    budget = n - MAX_CHAR
                    for amount in range(1,3):
                        for i, dec in enumerate(list_dec):
                            if dec == amount and budget >= amount:
                                list_repeats[i]-=amount
                                budget-=amount
                    for i, r in enumerate(list_repeats):
                        for _ in range(r//3):
                            if budget >= 3:
                                list_repeats[i]-=3
                                budget-=3
                    
                    if budget == sum(list_repeats):
                        return  n_missing_type + n - MAX_CHAR
                    else:
                        return max(n_missing_type, sum([r//3 for r in list_repeats])) + n - MAX_CHAR
                else:
                    return n_missing_type + n - MAX_CHAR
                
            
Solution().strongPasswordChecker("aaa111")