import sys
import time
import copy

THINKING_TIME = 10
# This file will contains all the implementation of the minimax algorithm and aplha-beta pruning. (subject to change)

class Node:
    def __init__(self, board, colour_to_move='B', action ="", parent=None):
      self.parent = parent
      self.board = board
      self.colours_turn = colour_to_move
      self.action = action
      self.successors = []

    def get_successors(self, state):
        return

    def preprocess_first_moves(self):
        # 4 possible moves for Black - remove piece at A8, D5, E4 or H1
        self.board.print()
        self.insert_successor("A8", "W")
        self.insert_successor("D5", "W")
        self.insert_successor("E4", "W")
        self.insert_successor("H1", "W")
        print('wrvw')
        white_moves = [["B8", "A7"], ["D6", "C5", "E5", "D4"], ["E5", "D4", "F4", "E3"], ["H2", "G1"]]
        for i in range(len(white_moves)):
            move = self.successors[i]
            for j in white_moves[i]:
                print('wrvw')
                move.insert_successor(j, "B")
                move.successors[-1].board.print()
        
    def insert_successor(self, move, colour):
        successor = KonaneBoard(self.board.get_board())
        successor.update_by_move(move)
        self.successors.append(Node(successor, colour, move, self))

# Implements the minimax algorithm
class KonaneAI:
    def __init__(self, colour, state = None):
        self.total_moves = 0
        self.stae = state
        self.best_moves = []
        self.olour = colour

    #actions -> move piece, wait, remove piece
    def action(self, state):
        if self.total_moves == 0 and self.colour == 'W':
            print()
        elif self.total_moves == 0 and self.colour == 'B':
            print()
        else:
            print()

        return self.__actions.pop()
        

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

    def get_board(self):
        return copy.deepcopy(self.board)

def main():
    argv = sys.argv
    agent = KonaneAI('B')

    n = Node(KonaneBoard())
    n.preprocess_first_moves()

   # while True():
    #    agent.action()
     #   opp_move = input()

    return

if __name__ == "__main__":
    main()