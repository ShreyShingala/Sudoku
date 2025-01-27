def print_board_terminal(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("---------------------")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")
                
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return (i, j)
            
    return None
         
def valid_checker(board, number, position):
    valuey, valuex = position
    # Determine column
    for i in range(len(board)):
        if board[i][valuex] == number and valuey != i:
            return False
    # Determine row
    for i in range(len(board[0])):
        if board[valuey][i] == number and valuex != i:
            return False
        
    # Determine box
    boxx = valuex // 3
    boxy = valuey // 3
    
    for i in range(boxy*3, boxy*3+3):
        for j in range(boxx*3, boxx*3+3):  # Fix the range here
            if board[i][j] == number and (i, j) != position:
                return False
            
    return True

def solve(board):
    position = find_empty(board)
    if not position:
        return True #solution has been found
    else:
        row, col = position
        
    for i in range(1, 10):
        if valid_checker(board, i, (row, col)):
            board[row][col] = i
            
            if solve(board):
                return True
            
            board[row][col] = 0
            
    return False