import sys
# This file will contains all the implementation of the minimax algorithm and aplha-beta pruning. (subject to change)

# Implements the minimax algorithm
class KonaneAI:
    def __init__(self):
        pass

# Implements the playing board - 8x8, alternating black and white tiles
class KonaneBoard:
    def __init__(self, board=[]):
        self.board = []
        if board == []: 
            self.create_board()
        else: 
            self.board = board

    def create_board(self):
        for i in range(8):
            if i % 2 == 0:
                self.board.append(self.create_row('B','W'))
            else:
                self.board.append(self.create_row('W','B'))
        for row in self.board:
            print(row)

    def create_row(self, color1, color2):
        row = []
        for i in range(8):
            if i%2 == 0:
                row.append(color1)
            else:
                row.append(color2)
        return row
    
    def update(self, action, colour):
        column = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7} 
        tile_row_1 = int(action[1]) - 1
        tile_col_1 = column[action[0]]
        if len(action) == 2: # remove piece
            self.board[tile_row_1][tile_col_1] = 'O'
            return
        
        tile_row_2 = int(action[4]) - 1
        tile_col_2 = column[action[3]]
        if  tile_col_1 == tile_col_2: # vertical/column jump
            for i in range(int(tile_row_1), tile_row_2):
                self.board[i][tile_col_1] = 'O'
            self.board[int(tile_row_2)][tile_col_2] = colour
        else: # horizontal/row jump
            for j in range(tile_col_1, tile_col_2):
                self.board[j][tile_col_1] = 'O'
            self.board[tile_row_2][tile_col_2] = colour

    
    # to see if the board is correct
    def print(self):
        for i in self.board:
            print(i)

        #    for j in range(len(self.board[0])):
        #        print(self.board[i][j], end="")
            #print('\n')


def main():
    argv = sys.argv
    board = KonaneBoard()
    agent = KonaneAI()
    print('\n')
    board.print()
    board.update('E5', 'B')
    board.update('G5', 'W')
    print('\n')
    board.print()
        
    return

if __name__ == "__main__":
    main()