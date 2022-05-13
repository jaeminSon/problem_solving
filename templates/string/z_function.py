def get_zarr(string):
    # element[i] = max_x string[i:i+x] == string[:x]
    # Index            0   1   2   3   4   5   6   7   8   9  10  11 
    # Text             a   a   b   c   a   a   b   x   a   a   a   z
    # Z values         X   1   0   0   3   1   0   0   2   2   1   0 
    n = len(string)
    z = [0] * n
 
    # z-box: [l, r]
    l, r, k = 0, 0, 0
    for i in range(1, n):
        if i > r: # outside the z-box (count naively)
            l, r = i, i
            while r < n and string[r - l] == string[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else: # inside the z-box
            k = i - l # start index of previously discovered substring, z[i] >= min(z[K], r-i+1)
            if z[k] < r - i + 1: # z[k] could not exceed the z-box as something in the way for z[i]
                z[i] = z[k]
            else:
                l = i # z[k] exceeded the z-box (z[i] has potential to grow)
                while r < n and string[r - l] == string[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    return z
 
def search(text, pattern):
 
    concat = pattern + "$" + text
    l = len(concat)
 
    z = get_zarr(concat)
    for i in range(l):
        if z[i] == len(pattern):
            return i - len(pattern) - 1
 
if __name__ == "__main__":
    text = "GEEKS FOR GEEKSK"
    pattern = "GEEKS"
    print(search(text, pattern))