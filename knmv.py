#!/usr/bin/env python3

import sys
import copy
import random

class Node:
    def __init__(self, board, colours_turn="B", move =""):
        self.board = board
        self.colours_turn = colours_turn

''' 
This class creates and modfies a playing board for the 8x8 Konane game using alternating black and white tiles.
Uses the data structure list containing lists of characters either 'W', 'B', or 'O' for formatting the board.
'W' for white, 'B' for black, and 'O' for empety tiles.
'''
class KonaneBoard:
    '''
    Purpose: Initializes a new instance of the KonaneBoard class.
    Parameters:
        - board: An optional parameter representing the initial configuration of the board. If none, creates an empty board.
    '''
    def __init__(self, board=[]):
        # represents the current state of the board Starts as an empty list.  
        self.board = []
        # represent a string containing the column labels ('A' - 'H') used for referencing the board positions. 
        self.x = "ABCDEFGH"
        # if no initial board configuration is provided, the create_board() function is called to set up the board. 
        if board == []: 
            self.create_board()
        else: 
            self.board = board
    '''
    Purpose: Creates the initial configuration of the game board. Alternates between the two colors ('B' or 'W') to fill the board with checkerboard pattern.
    '''
    def create_board(self):
        #iterate throught each of the 8 columns since it is an 8x8 board.
        for i in range(8):
            # even columns get certain color pattern starting with black 'B'
            if i % 2 == 0:
                self.board.append(self.create_row('B','W'))
            # odd columns get oppsosite pattern starting with 'W'
            else:
                self.board.append(self.create_row('W','B'))
    '''
    Purpose: Creates a single row of the game board, alternating between colors.
    Parameters:
        - color1: First color to alternate.
        - color2: Second color to alternate.
    Return: List representing a single row of the board.
    '''
    def create_row(self, color1, color2):
        row = []
        for i in range(8):
            #Even spots append color1 to list
            if i%2 == 0:
                row.append(color1)
            #Odd spots append color2 to list
            else:
                row.append(color2)
        return row
        
    '''
    Purpose: This method updates the game board based on a given move. The move can either be a piece removal or a jump move. 
    The method updates the board based off of the rules of the Konane game. 
        - If the move is a stone piece removal, the corresponding board position is marked as empty ('O').
        - If the move is a jump, stone pieces are removed and moved to a new postition as necessary to execute the jump. 
            - moves in between the initial and new position are marked empty ('O').
    Parameters:
            - move: The move to be executed.
    '''
    def update_by_move(self, move):
        # Convert tile piece to match its placement in a list of list
        prev_x = self.convert_letter(move[0])
        prev_y = self.convert_number(move[1])
        # color of moving piece
        colour = self.board[prev_y][prev_x]
        #if the len(move) is greater then 2 it means that it is a jump move otherwise normal move.
        if len(move) == 2: # remove piece case
            self.board[prev_y][prev_x] = 'O'
            return
        # Convert second tile piece to match its placement in a list of list
        new_x = self.convert_letter(move[3])
        new_y = self.convert_number(move[4])
        step = 1 
        if prev_x == new_x: # vertical/column jump
            if new_y < prev_y: step = -1 # going up
            for i in range(prev_y, new_y, step): # can handle multiple jumps
                self.board[i][prev_x] = 'O'
            self.board[new_y][new_x] = colour
        else: # horizontal/row jump
            if new_x < prev_x: step = -1 # going left
            for j in range(prev_x, new_x, step): # can handle multiple jumps
                self.board[prev_y][j] = 'O'
            self.board[new_y][new_x] = colour
    '''
    Purpose: Converts a letter coordinate to an integer.
    Parameters:
        - letter: The letter coordinate.
    Return: Integer representation of the letter coordinate.
    '''
    def convert_letter(self, letter):
        return self.x.find(letter)
    '''
    Purpose: Converts a numerical coordinate to an integer.
    Parameters:
        - number: The numerical coordinate.
    Return: Integer representation of the numerical coordinate.
    '''
    def convert_number(self, number):
        return 8 - int(number)
    '''
    Purpose: Print the current state of the game board.
    '''
    def print_board(self):
        for i in range(len(self.board)):
            print(8-i, end = '')
            print(self.board[i])
        print(f' {list(self.x)}')
        print()
    '''
    Purpose: Creates deep copy of game board so that no unintended changes occur to original board.
    Return: deep copy of board.
    '''
    def get_board(self):
        return copy.deepcopy(self.board)

def is_first_move_W(state):
    # board with D5 removed
    board_1 = KonaneBoard()
    board_1.update_by_move("D5")
    # board with E4 removed
    board_2 = KonaneBoard()
    board_2.update_by_move("E4")
    # check if current state is a first move for W case
    if state.board.board == board_1.board or state.board.board == board_2.board: return True
    else: return False

def generate_valid_moves(state):
        # first moves of W and B are unimportant since they are diagonally symmetric
        # randomly choose only one node to search through so it doesn't go through nodes of its diagonally symmetric counterpart
        if state.board.board == KonaneBoard().board: 
            return ["D5", "E4"]
        if is_first_move_W(state): 
            return ["E5", "D4"]
          
        # identify opponent's colour
        if state.colours_turn == "B": colour_opp = "W"
        else: colour_opp = "B"
        
        moves = [] # list of valid moves
        # go through all tiles in board
        for y in range(8):
            for x in range(8):
                # found piece to move
                if state.board.get_board()[y][x] == state.colours_turn:
                    initial = convert_to_tile(x, y)
                    #moving left
                    for k in range(x - 1, -1, -2):
                        # case 1: break if out of bounds
                        if k < 0 or (k - 1) < 0: break 
                        # case 2: break if piece cannot jump over a piece anymore
                        if state.board.get_board()[y][k] != colour_opp or state.board.get_board()[y][k - 1] != 'O': break 
                        # add to moves if both cases above are true
                        final = convert_to_tile(k-1, y)
                        moves.append(f"{initial}-{final}") 

                    #moving up
                    for j in range(y-1, -1, -2):
                        # case 1: break if out of bounds
                        if j < 0 or (j - 1) < 0: break
                        # case 2: break if piece cannot jump over a piece anymore
                        if state.board.get_board()[j][x] != colour_opp or state.board.get_board()[j-1][x] != 'O': break
                        # add to moves if both cases above are true
                        final = convert_to_tile(x, j - 1)
                        moves.append(f"{initial}-{final}") 

                    #moving right
                    for k in range(x+1, 8, 2):
                        # case 1: break if out of bounds
                        if k > 7 or (k + 1) > 7: break
                        # case 2: break if piece cannot jump over a piece anymore
                        if state.board.get_board()[y][k] != colour_opp or state.board.get_board()[y][k + 1] != 'O': break
                        # add to moves if both cases above are true
                        final = convert_to_tile(k + 1, y)
                        moves.append(f"{initial}-{final}") 

                    #moving down
                    for l in range(y+1, 8, 2):
                        # case 1: break if out of bounds
                        if l > 7 or (l + 1) > 7: break
                        # case 2: break if piece cannot jump over a piece anymore
                        if state.board.get_board()[l][x] != colour_opp or state.board.get_board()[l + 1][x] != 'O': break
                        # add to moves if both cases above are true
                        final = convert_to_tile(x, l + 1)
                        moves.append(f"{initial}-{final}") 
        return moves


def convert_to_tile(x, y):
    column = "ABCDEFGH"
    letter = column[x]
    number = str(8 - y)
    return letter + number
    '''
    Purpose: This method reads in the intial congfiguration of the game board from a text file. 
    Parameters: It takes a 'filename' parameter, specifying the name of the file containing the board configuration. 
    The methods opens the file and reads in the data from each row, appending the contents to a list representing the intial game configuration. 
    '''
def get_board_from_file(filename):
    current_board = []
    with open(filename) as file:
        for row in file:
            current_board.append(list(row.strip()))
    return current_board

def convert_board_to_file(board, filename):
    fh = open(filename, "w")
    for row in board:
        x = ""
        for ch in row:
            x = x + ch
        fh.write(x + "\n")
    fh.close()



# use to play agent, displaying the board after each move, possible moves and time used by agent
def main():
    # get arguments 'python3 main.py filename colour'
    filename = sys.argv[1]
    colour = sys.argv[2]
    move = sys.argv[3]
    # create agent and current board from the given file
    board = KonaneBoard(get_board_from_file(filename))
    state = Node(board, colour)
    moves = generate_valid_moves(state)

    if move in moves:
        board.update_by_move(move)
        board.print_board()
        convert_board_to_file(board.board, filename)
    else:
        print(f"{colour}: INVALID MOVE!!!")
        sys.exit(1)

    
    if colour == "W":
        colour_2 = "B"
    else: colour_2 = "W"
    state = Node(state.board, colour_2)
    opp_moves = generate_valid_moves(state)
    print(opp_moves)
    if len(opp_moves) == 0:
        print(f"{colour}: WINS")
        sys.exit(1)
        

if __name__ == "__main__":
    main()