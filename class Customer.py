class Customer:
    def __init__(self, x, y):
            self.x, self.y = x,y
    
    def moveCustomer(self,x,y, app):
         startRow, startCol=3,13
         targetRow, targetCol=solve(self, app, startRow, startCol)
         self.x=#coordinate of targetRow
         self.y=#coordinate of targetCol
    
    def isLegal(targetRow, targetCol, board):  
         rows, col=len(board), len(board[0])
         return (0<=targetRow<rows and 0<=targetCol<cols
             and board[targetRow][targetCol]==0)
    
    def solve(self, board, row, col):
        if board[targetRow][targetCol]==2:
             return targetRow, targetCol
        else:
            for drow, dcol in [(-1,0),(0,1),(0,-1),(1,0),(1,1),(-1,-1)]:
                    targetRow, targetCol=row+drow, col+dcol
                    if isLegal(targetRow, targetCol, board):
                        board[targetRow][targetCol]==1
                        solution=solve(board)
                        if solution!=None:
                            return solution
                        board[targetRow][targetCol]==0
            return None
    
    
    
                    
                    