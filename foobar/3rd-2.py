from fractions import Fraction


def solution(m):
    # Your code here
    
    def count2prob(mat):
        n_entire_states = len(mat)
        prob = [[] for _ in range(n_entire_states)]
        for i in range(n_entire_states):
            total = 0
            for j in range(n_entire_states):
                total += mat[i][j]
            if total != 0: # skip terminal states
                for j in range(n_entire_states):
                    prob[i].append(Fraction(numerator=mat[i][j], denominator=total))
        return prob
    
    def mat2RQ(mat):
        # convert matrix to R, Q in absorbing Markov Chain
        n_entire_states = len(mat)
        indices_non_terminal = []
        indices_terminal = []
        for i in range(n_entire_states):
            if len(mat[i]) == 0:
                indices_terminal.append(i)
            else:
                indices_non_terminal.append(i)
        
        indices_non_terminal = sorted(indices_non_terminal)
        indices_terminal = sorted(indices_terminal)
        R = [[] for _ in range(len(indices_non_terminal))]
        Q = [[] for _ in range(len(indices_non_terminal))]
        for index_new_row, i in enumerate(indices_non_terminal):
            for j in indices_terminal:
                R[index_new_row].append(mat[i][j])
            for j in indices_non_terminal:
                Q[index_new_row].append(mat[i][j])
            
        return R, Q
    
    def build_I_minus_Q(Q):
        length = len(Q)
        I_minus_Q = [[] for _ in range(length)]
        for i in range(length):
            for j in range(length):
                if i==j:
                    I_minus_Q[i].append(Fraction(1, 1) - Q[i][j])
                else:
                    I_minus_Q[i].append(-Q[i][j])
        return I_minus_Q
        
    def invert(mat): # copy-pasted from web

        def transposeMatrix(m):
            return map(list,zip(*m))

        def getMatrixMinor(m,i,j):
            return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

        def getMatrixDeternminant(m):
            if len(m) == 1:
                return m[0][0]
            elif len(m) == 2:
                return m[0][0]*m[1][1]-m[0][1]*m[1][0]
            determinant = 0
            for c in range(len(m)):
                determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
            return determinant
        
        
        determinant = getMatrixDeternminant(mat)
        if len(mat) == 1:
            return [[1/mat[0][0]]]
        elif len(mat) == 2:
            return [[mat[1][1]/determinant, -1*mat[0][1]/determinant],
                    [-1*mat[1][0]/determinant, mat[0][0]/determinant]]

        # find matrix of cofactors
        cofactors = []
        for r in range(len(mat)):
            cofactorRow = []
            for c in range(len(mat)):
                minor = getMatrixMinor(mat,r,c)
                cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
            cofactors.append(cofactorRow)
        cofactors = transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c]/determinant
        return cofactors
    
    
    def mat_mult(A,B):
        """
        A: NxN list of list
        B: Nxk list of list
        """
        row_A = len(A)
        col_B = len(B[0])
        new_mat = [[] for _ in range(row_A)]
        for i in range(row_A):
            col = len(A[i])
            for k in range(col_B):
                val = 0
                for j in range(col):
                    val+=A[i][j]*B[j][k]
                new_mat[i].append(val)    
        return new_mat
    
    def cast2submit_format(fractions):
        
        def gcd(x,y):
            if x>y: 
                bigger, smaller = x, y
            else: 
                bigger, smaller = y, x
            
            if bigger % smaller==0:
                return smaller
            else:
                return gcd(smaller, bigger % smaller)
            
        def lcm(x, y):
            return x*y//gcd(x,y)
        
        denominators = [fraction.denominator for fraction in fractions]
        curr_lcm = 1
        for denom in denominators:
            curr_lcm = lcm(curr_lcm, denom)
        
        return [fraction.numerator * curr_lcm // fraction.denominator for fraction in fractions] + [curr_lcm]
    
        
    if sum(m[0]) == 0: # initial_state == terminal_state
        return [1] + [0]*(len(m)-1) + [1]
    else:
        mat = count2prob(m)
        R, Q = mat2RQ(mat)
        I_minus_Q = build_I_minus_Q(Q)
        F = invert(I_minus_Q)
        stationary_dist = mat_mult(F, R)
        return cast2submit_format(stationary_dist[0])


# print(solution([[0]]))
# print(solution([[0,0], [0,0]]))
# print(solution([[0,0,0], [0,0,0], [0,0,0]]))
# print(solution([[0,0,0,0,0,0,0,0,1,1], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0]]))
# print(solution([[0,1], [0,0]]))
# print(solution([[1,1,3,1], [0,0,1,0], [0,0,0,0], [0,0,0,0]]))
# print(solution([[0,1,1], [0,0,0],[0,0,0]]))
# print(solution([[0,1,1], [1,1,1], [0,0,0]]))
# print(solution([[1,1,1], [0,0,0],[0,0,0]]))
# print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]))
# print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))

# TEST 1
#m = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
#a = [7, 6, 8, 21]
# TEST 2
# m = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
# a = [0, 3, 2, 9, 14]
# TEST 3
m = [[1, 2, 3, 0, 0, 0], [4, 5, 6, 0, 0, 0], [7, 8, 9, 1, 0, 0], [0, 0, 0, 0, 1, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
#a = [1, 2, 3]
print(solution(m))
#TEST 4
m = [[0]]
#a = [1, 1]
print(solution(m))
# TEST 5
m = [[0, 0, 12, 0, 15, 0, 0, 0, 1, 8], [0, 0, 60, 0, 0, 7, 13, 0, 0, 0], [0, 15, 0, 8, 7, 0, 0, 1, 9, 0], [23, 0, 0, 0, 0, 1, 0, 0, 0, 0], [37, 35, 0, 0, 0, 0, 3, 21, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#a = [1, 2, 3, 4, 5, 15]
print(solution(m))
# TEST 6
m = [[ 0,  7,  0, 17,  0,  1,  0,  5,  0,  2], [ 0,  0, 29,  0, 28,  0,  3,  0, 16,  0], [ 0,  3,  0,  0,  0,  1,  0,  0,  0,  0], [48,  0,  3,  0,  0,  0, 17,  0,  0,  0], [ 0,  6,  0,  0,  0,  1,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0], [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]
#a = [4, 5, 5, 4, 2, 20]
print(solution(m))
# TEST 7
m = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#a = [1, 1, 1, 1, 1, 5]
print(solution(m))
# TEST 8
m = [[1, 1, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 1, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 1, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#a = [2, 1, 1, 1, 1, 6]
print(solution(m))
# TEST 9
m = [[0, 86, 61, 189, 0, 18, 12, 33, 66, 39], [0, 0, 2, 0, 0, 1, 0, 0, 0, 0], [15, 187, 0, 0, 18, 23, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#a = [6, 44, 4, 11, 22, 13, 100]
print(solution(m))
# TEST 10
m = [[0, 0, 0, 0, 3, 5, 0, 0, 0, 2], [0, 0, 4, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 4, 4, 0, 0, 0, 1, 1], [13, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 1, 8, 7, 0, 0, 0, 1, 3, 0], [1, 7, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#a = [1, 1, 1, 2, 5]
print(solution(m))