import sys

c2d = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5,
    'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 
    'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 
    'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25,
    '!': 26, '?': 27, '.': 28, ',': 29, ':': 30, ';': 31, 
    '-': 32, '_': 33, "'": 34, '#': 35, '$': 36, '%': 37, 
    '&': 38, '/': 39, '=': 40, '*': 41, '+': 42, '(': 43, 
    ')': 44, '{': 45, '}': 46, '[': 47, ']': 48, 
    '0': 49, '1': 50, '2': 51, '3': 52, '4': 53, 
    '5': 54, '6': 55, '7': 56, '8': 57, '9': 58, " ":59,
    'A': 60, 'B': 61, 'C': 62, 'D': 63, 'E': 64, 'F': 65, 
    'G': 66, 'H': 67, 'I': 68, 'J': 69, 'K': 70, 'L': 71, 
    'M': 72, 'N': 73, 'O': 74, 'P': 75, 'Q': 76, 'R': 77, 
    'S': 78, 'T': 79, 'U': 80, 'V': 81, 'W': 82, 'X': 83, 'Y': 84, 'Z': 85}


while True:

    n,m  = [int(d) for d in sys.stdin.readline().rstrip().split()]

    if n==0 and m==0:
        break

    words = [sys.stdin.readline().rstrip() for _ in range(n)]
    queries = [sys.stdin.readline().rstrip() for _ in range(m)]
    
    max_states = sum([len(word) for word in words])
    max_characters = 26 + len(c2d.keys())

    out = [0]*(max_states+1)
    fail = [-1]*(max_states+1)
    goto = [[-1]*max_characters for _ in range(max_states+1)]
    
    states = 1
    
    for i in range(len(words)):
        word = words[i]
        current_state = 0
        for character in word:
            ch = c2d[character]

            if goto[current_state][ch] == -1:
                goto[current_state][ch] = states
                states += 1

            current_state = goto[current_state][ch]

        out[current_state] |= (1<<i)

    for ch in range(max_characters):
        if goto[0][ch] == -1:
            goto[0][ch] = 0
    
    queue = []
    for ch in range(max_characters):
        if goto[0][ch] != 0:
            fail[goto[0][ch]] = 0
            queue.append(goto[0][ch])
    
    while queue:
        state = queue.pop(0)
        for ch in range(max_characters):
            if goto[state][ch] != -1:

                failure = fail[state]

                while goto[failure][ch] == -1:
                    failure = fail[failure]
                
                failure = goto[failure][ch]
                fail[goto[state][ch]] = failure
                out[goto[state][ch]] |= out[failure]
                queue.append(goto[state][ch])
            
    
    n_delete = 0
    for text in queries:
        current_state = 0
        for i in range(len(text)):
            s = current_state
            ch = c2d[text[i]]
            while goto[s][ch] == -1:
                s = fail[s]
            current_state = goto[s][ch]
            if out[current_state] != 0:
                current_state = 0
                n_delete+=1

    print(n_delete)


    
