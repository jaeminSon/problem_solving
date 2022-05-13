def print_grid(arr):
    for i in range(9):
        print(" ".join([str(arr[i][j]) for j in range(9)]))
 
def get_empty_location(arr):
    for row in range(9):
        for col in range(9):
            if(arr[row][col]== 0):
                return row, col
    return None
 
def used_in_row(arr, row, num):
    for i in range(9):
        if(arr[row][i] == num):
            return True
    return False
 
def used_in_col(arr, col, num):
    for i in range(9):
        if(arr[i][col] == num):
            return True
    return False
 
def used_in_box(arr, row, col, num):
    row_start = 3 * (row // 3)
    col_start = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if(arr[i + row_start][j + col_start] == num):
                return True
    return False
 
def available(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row, col, num)
 
def solve(arr):
    loc = get_empty_location(arr)
    if loc is None:
        return True
    else: 
        row, col = loc
        for num in range(1, 10):
            if available(arr, row, col, num):
                arr[row][col]= num
                if solve(arr):
                    return True
                # backtrack
                arr[row][col] = 0
        return False
 
if __name__=="__main__":
     
    grid =[[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]
     
    if(solve(grid)):
        print_grid(grid)
    else:
        print("No solution exists")