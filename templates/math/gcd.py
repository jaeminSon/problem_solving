def gcd(a, b):
    large, small = (a, b) if a>=b else (b, a)
    return large if small == 0 else gcd(small, large % small)

if __name__=="__main__":
    assert gcd(10,2)==2