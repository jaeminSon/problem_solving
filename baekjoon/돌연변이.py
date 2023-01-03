import sys

def char2val(char):
    if char=="A":
        return 0
    elif char=="C":
        return 1 
    elif char=="G":
        return 2
    elif char=="T":
        return 3 
    else:
        raise ValueError

T = int(sys.stdin.readline().rstrip())
for _ in range(T):
    n,m  = [int(d) for d in sys.stdin.readline().rstrip().split()]

    text = sys.stdin.readline().rstrip()
    d = sys.stdin.readline().rstrip()

    words = set([d])
    for i in range(len(d)):
        for j in range(i+1, len(d)+1):
            words.add(d[:i]+ d[i:j][::-1]+ d[j:])
    words = list(words)
    
    max_states = sum([len(word) for word in words])
    max_characters = 4

    out = [0]*(max_states+1)
    fail = [-1]*(max_states+1)
    goto = [[-1]*max_characters for _ in range(max_states+1)]
    
    states = 1
    
    for i in range(len(words)):
        word = words[i]
        current_state = 0
        for character in word:
            ch = char2val(character)

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
            
    
    current_state = 0
    n_match = 0
    for i in range(len(text)):
        s = current_state
        ch = char2val(text[i])
        while goto[s][ch] == -1:
            s = fail[s]
        current_state = goto[s][ch]
        if out[current_state] != 0:
            n_match+=1

    print(n_match)


    
