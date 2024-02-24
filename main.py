import sys
# This file will contains all the implementation of the minimax algorithm and aplha-beta pruning. (subject to change)

# Implements the minimax algorithm
class KonaneAI:
    def __init__(self, state=[]):
        self.__curr_board_state = state
        self.__action = []
    
    def first_move_W(self, board_file):
        fh = open(board_file, "r")
        line = fh.readline()
        row = 0
        while line != "":
            if 'O' in line:
                break
            row += 1
            line = fh.readline()
        
        if row == 0:
            return ""
            

    def first_move_B(self, board_file):
        
        return
    
    def successors(state):

        return

class Node:
   def __init__(self, parent, board, colour):
      self.__parent = parent
      self.__board = board
      self.__colour = colour
      self.__action = ""
      self.__successors = []

# Implements the playing board - 8x8, alternating black and white tiles
class KonaneBoard:
    def __init__(self, board=[]):
        self.board = []
        self.x = "ABCDEFGH"
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

    def create_row(self, color1, color2):
        row = []
        for i in range(8):
            if i%2 == 0:
                row.append(color1)
            else:
                row.append(color2)
        return row
    
    def update_by_move(self, move):
        # Convert tile piece to match list of list format
        prev_x = self.convert_letter(move[0])
        prev_y = self.convert_number(move[1])
        # color of moving piece
        colour = self.board[prev_y][prev_x]
        if len(move) == 2: # remove piece
            self.board[prev_y][prev_x] = 'O'
            return
        # Convert second tile piece to match list of list format
        new_x = self.convert_letter(move[3])
        new_y = self.convert_number(move[4])
        step = 1

        if  prev_x == new_x: # vertical/column jump
            if new_y < prev_y: step = -1
            for i in range(prev_y, new_y, step): # can handle multiple jumps
                self.board[i][prev_x] = 'O'
            self.board[int(new_y)][new_x] = colour
        else: # horizontal/row jump
            print('wru')
            if new_x < prev_x: step = -1
            for j in range(prev_x, new_x, step): # can handle multiple jumps
                print('ddd')
                self.board[prev_y][j] = 'O'
            self.board[new_y][new_x] = colour
    
    
    # letter - x, number - y Ex. E5 -> 'E', '5'
    def convert_letter(self, letter):
        return self.x.find(letter)
    
    def convert_number(self, number):
        return 8 - int(number)

    # to see if the board is correct
    def print(self):
        for i in self.board:
            print(i)

    
def main():
    argv = sys.argv
    board = KonaneBoard()
    agent = KonaneAI()
    board.print()
    print('\n')
    board.update_by_move('E5')
    board.update_by_move('G3-E3')
    board.update_by_move('G6-E6')
    board.update_by_move('A1-A6')


    board.print()
    #board.convert_file_to_board("test_file.txt")

    #if argv[2] == 'W':
    #    print()
    #else:
    #    print()

    return

if __name__ == "__main__":
    main()