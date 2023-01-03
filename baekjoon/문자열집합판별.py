import sys

N = int(sys.stdin.readline().rstrip())
words = [sys.stdin.readline().rstrip() for _ in range(N)]

Q = int(sys.stdin.readline().rstrip())
queries = [sys.stdin.readline().rstrip() for _ in range(Q)]

class AhoCorasick:
    def __init__(self, words):
    
        for i in range(len(words)):
          words[i] = words[i].lower()
        self.words = words

        self.max_states = sum([len(word) for word in words])
        self.max_characters = 26 # [a-z]
 
        self.out = [0]*(self.max_states+1)
        self.fail = [-1]*(self.max_states+1)
        self.goto = [[-1]*self.max_characters for _ in range(self.max_states+1)]
         
        self.__build_matching_machine()
 
 
    def __build_matching_machine(self):
 
        states = 1
 
        for i in range(len(self.words)):
            word = self.words[i]
            current_state = 0
            for character in word:
                ch = ord(character) - 97 # Ascii value of 'a' = 97
 
                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1
 
                current_state = self.goto[current_state][ch]
 
            self.out[current_state] |= (1<<i)
 
        for ch in range(self.max_characters):
            if self.goto[0][ch] == -1:
                self.goto[0][ch] = 0
         
        queue = []
        for ch in range(self.max_characters):
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])
        
        while queue:
            state = queue.pop(0)
            for ch in range(self.max_characters):
                if self.goto[state][ch] != -1:
 
                    failure = self.fail[state]
 
                    while self.goto[failure][ch] == -1:
                        failure = self.fail[failure]
                     
                    failure = self.goto[failure][ch]
                    self.fail[self.goto[state][ch]] = failure
                    self.out[self.goto[state][ch]] |= self.out[failure]
                    queue.append(self.goto[state][ch])
         
 
    def __find_next_state(self, current_state, next_input):
        answer = current_state
        ch = ord(next_input) - 97 # Ascii value of 'a' is 97
 
        while self.goto[answer][ch] == -1:
            answer = self.fail[answer]
 
        return self.goto[answer][ch]
 
 
    def has_word(self, text):
        
        text = text.lower()
 
        current_state = 0
        
        for i in range(len(text)):
            current_state = self.__find_next_state(current_state, text[i])
            if self.out[current_state] != 0:
                for j in range(len(self.words)):
                    if (self.out[current_state] & (1<<j)) > 0:
                        return True
 
        return False


aho_chorasick = AhoCorasick(words)
for q in queries:
    if aho_chorasick.has_word(q):
        print("YES")
    else:
        print("NO")
