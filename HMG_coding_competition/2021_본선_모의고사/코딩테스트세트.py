import sys

N, T = [int(el) for el in sys.stdin.readline().split()]

for _ in range(T):
    scenario = [int(el) for el in sys.stdin.readline().split()]
    n_problems = (len(scenario) + 1) // 2
    list_problems = [0] * n_problems
    list_problems[0] = scenario[0]
    for i in range(1, n_problems):
        list_problems[i] = scenario[2*i-1] + scenario[2*i]

    def flatten(s, e, average):
        modified = False
        for i in range(e, s, -1):
            if list_problems[i] > average:
                modified = True
                donate = min(list_problems[i] - average, scenario[2*i-1])
                scenario[2*i-1] -= donate
                list_problems[i] -= donate
                list_problems[i-1] += donate
        return modified
    
    modified = True
    while True:
        argmin = min(range(n_problems), key=lambda i:list_problems[i])
        if not modified or argmin == n_problems-1 or scenario[2*argmin+1] == 0:
            break
        
        end_period = argmin + 1
        while end_period < n_problems and scenario[2*end_period-1] != 0:
            end_period += 1
        
        average = sum(list_problems[argmin:end_period]) // (end_period - argmin)
        modified = flatten(argmin, end_period-1, average)
        
    print(list_problems[argmin])
