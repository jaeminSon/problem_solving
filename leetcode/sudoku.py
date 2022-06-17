from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j] = int(board[i][j]) if board[i][j]!="." else 0
        Solution.sudoku(board)
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j] = str(board[i][j])
        

    @staticmethod
    def sudoku(arr):
        loc = Solution.get_empty_location(arr)
        if loc is None:
            return True
        else: 
            row, col = loc
            for num in range(1, 10):
                if Solution.available(arr, row, col, num):
                    arr[row][col]= num
                    if Solution.sudoku(arr):
                        return True
                    # backtrack
                    arr[row][col] = 0
            return False
        
    @staticmethod
    def get_empty_location(arr):
        for row in range(9):
            for col in range(9):
                if(arr[row][col]== 0):
                    return row, col
        return None
    
    @staticmethod
    def used_in_row(arr, row, num):
        for i in range(9):
            if(arr[row][i] == num):
                return True
        return False
    
    @staticmethod
    def used_in_col(arr, col, num):
        for i in range(9):
            if(arr[i][col] == num):
                return True
        return False
    
    @staticmethod
    def used_in_box(arr, row, col, num):
        row_start = 3 * (row // 3)
        col_start = 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if(arr[i + row_start][j + col_start] == num):
                    return True
        return False
    
    @staticmethod
    def available(arr, row, col, num):
        return not Solution.used_in_row(arr, row, num) and not Solution.used_in_col(arr, col, num) and not Solution.used_in_box(arr, row, col, num)
 
arr = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
Solution().solveSudoku(arr)
print(arr)