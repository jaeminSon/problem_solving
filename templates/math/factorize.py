def factorize(v):
    if v == 1:
        return []
    elif v%2==0:
        return [2]+factorize(v//2)
    else:
        for i in range(3, v+1, 2):
            if v%i==0:
                return [i] + factorize(v//i)
            
print(factorize(100))
print(factorize(2**3))
print(factorize(2*3*7*11*13))