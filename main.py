'''
        Authors:
    - Hope Oberez, Brandon Funk and Tyler Hardy

        Purpose: 
    - This main.py file implements a Konane AI playing agent capable of strategic gameplay
    using alpha-beta pruning in conjunction with minimax tree search and evaluation functions to optimize 
    efficiency and desirability of moves for gameplay. 
'''
#!/usr/bin/env python3

import sys
import time
import copy
import random

THINKING_TIME = 9.9
''' 
Node class represents the game state for the search tree 
Contains attributes: 
    - like the game board (board) 
    - whose turn it is (colours_turn)
    - the action taken to reach this state (action)
    - list of successor nodes (successors)  
    - and the value of the node (value)
'''
class Node:
    def __init__(self, board, colours_turn="B", action ="", predecessor=None):
      self.predecessor = predecessor
      self.board = board
      self.colours_turn = colours_turn
      self.action = action
      self.successors = []
      self.value = 0 
    '''
    Purpose: Get the successor nodes.
    Return: List of successor nodes.
    '''
    def get_successors(self):
        return self.successors
    '''
    Purpose: Get the value of the node.
    Return: The value of the node.
    '''
    def get_value(self):
        return self.value
    '''
    Purpose: Get the action taken to reach this state.
    Return: The action taken to reach this state.
    '''
    def get_action(self):
        return self.action
'''
This class represents the Konane playing AI agent. 
Stores the information about the agent's current:
    - state: represents the current state of the game board. Allows AI to analyze and make decisions based on board configuration. 
    - color: Indicates the color of the AI agent. ('B' or 'W'). So that the AI knows which peices it controls. 
    - best moves: stores its best moves (optimal moves) determined by the AI based on eval function(s) and search algo. Makes AI efficent player.
    - and a transpositional table: Used to prevent evaluation of previously evaluated game states (symmetry). 
'''
class KonaneAI:
    '''
    Purpose: Represents a node (state) of a game for the search tree.
    '''
    def __init__(self, colour, state = None):
        self.state = state
        self.best_moves = []
        self.colour = colour
        self.max_depth = 2
        self.t_table = [state] # not yet optimised into program, should store KonaneBoard objects
        self.start = 0
    '''
    Purpose: Reset Konane agent values for max_depth, start (timer), and best_moves for newly updated state.
    '''
    def reset(self):
        self.start = time.time()
        self.best_moves = []
        self.max_depth = 2
    '''
    Purpose: Update the current KonaneAI state by the state with self.action == to the input.
    Parameters:
        - move: The move to update the state.
    '''
    def update_state(self, move):
        for i in self.state.get_successors():
            if i.get_action() == move:
                self.state = i
                return
        # create a new state if state was not found as a successor of the previous state
        self.state.board.update_by_move(move)
        self.state = Node(self.state.board, self.colour, move)
        return
    '''
    Purpose: Choose the best action based on current state. #ie:actions -> move piece, remove piece etc.
    Return: The chosen action.
    '''
    def action(self):
        while time.time() - self.start < THINKING_TIME:
            best_state = self.alpha_beta_search()
            if best_state == None: # thinking time limit is reached
                break
            self.best_moves.append(best_state)
            self.max_depth += 1
        
        self.state = self.best_moves.pop()
        return self.state.get_action()
    '''
    Purpose: Insert the next possible state/node after a legal move happens from the current state/node.
    Parameters:
        - moves: List of valid moves.
        - state: Current state/node.
    '''
    def insert_successors(self, moves, state):
        # the next state of the game will be the opposite colour's turn, assign that colour to successors
        if state.colours_turn == "B":
            colour = "W"
        else: 
            colour = "B"
        # go through all generated valid moves and create successor states
        for move in moves:
            # create a new board with updated move
            successor = KonaneBoard(state.board.get_board())
            successor.update_by_move(move)
            state.get_successors().append(Node(successor, colour, move, state))
    
    # implementing and modifying the given code for alpha beta pruning from the Adversarial search slides
    # modified to return a Node instead of an action
    '''
    Purpose: Implement the alpha-beta search algorithm.
    Return: The best state found, s.
    '''
    def alpha_beta_search(self):
        depth = 0
        v = self.max_value(depth, self.state, -1000, 1000)
        if v == None: return None # thinking time reached, terminate current search
        for s in self.state.get_successors():
            if s.get_value() == v:
                return s
    '''
    Purpose: Implement the max value function for alpha-beta search.
    Parameters:
        - depth: The current depth in the search tree.
        - state: Current state/node.
        - alpha: Alpha value.
        - beta: Beta value.
    Return: The maximum value, v.
    '''
    def max_value(self, depth, state, alpha, beta):
        # terminate current search, if it goes over thinking time
        if time.time() - self.start > THINKING_TIME: return None
        # cutoff/terminal node found
        if self.cutoff_test(depth, state): return self.evaluation(state)
        v = -1000
        # recursive
        for s in state.get_successors():
            s.value = self.min_value(depth + 1, s, alpha, beta)
            if s.value == None: return None # terminate current search: thinking time limit reached
            v = max(v, s.value)
            if v >= beta: return v
            alpha = max(alpha, v)

        return v
    '''
    Purpose: Implement the min value function for alpha-beta search.
    Parameters:
        - depth: The current depth in the search tree.
        - state: Current state/node.
        - alpha: Alpha value.
        - beta: Beta value.
    Return: The minimum value, v.
    '''
    def min_value(self, depth, state, alpha, beta):
         # terminate current search, if it goes over thinking time
        if time.time() - self.start > THINKING_TIME: return None   
        # cutoff/terminale node found
        if self.cutoff_test(depth, state): return self.evaluation(state)
        v = 1000
        # recursive
        for s in state.get_successors():
            s.value = self.max_value(depth + 1, s, alpha, beta)
            if s.value == None: return None # thinking time reached, terminate current search
            v = min(v, s.value)
            if v <= alpha: return v
            beta = min(beta, v)
        return v
    '''
    Purpose: Check if a cutoff condition is met.
    Parameters:
        - depth: The current depth in the search tree.
        - state: Current state/node.
    Return: True if cutoff condition is met, False otherwise.
    '''
    def cutoff_test(self, depth, state):     
        # generate valid moves for state if not yet generated
        if len(state.get_successors()) == 0:
            moves = self.generate_valid_moves(state)
            self.insert_successors(moves, state)
        # reach maximum depth for search
        if depth == self.max_depth: 
            return True
        # terminal node
        if len(state.get_successors()) == 0:
            return True
        return False
    '''
    Purpose: Check if the current state is a first move for W.
    Parameters:
        - state: Current state/node.
    Return: True if it is the first move for W, False otherwise.
    '''
    def is_first_move_W(self, state):
        # board with D5 removed
        board_1 = KonaneBoard()
        board_1.update_by_move("D5")
        # board with E4 removed
        board_2 = KonaneBoard()
        board_2.update_by_move("E4")
        # check if current state is a first move for W case
        if state.board.board == board_1.board or state.board.board == board_2.board: return True
        else: return False
    '''
    Purpose: Advanced evaluation function(s) that considers board control, piece mobility, and potential future moves.
    Parameters:
        - state: Current state/node.
    Return: A numerical score representing the desirability of the current game state for the AI.
    '''
    def evaluation(self, state):
        # Evaluation #1: difference between total moves and opponents moves
        # agent's turn for the given state
        
        if (state.colours_turn == 'B' and self.colour == 'B') or (state.colours_turn == 'W' and self.colour == 'W'):
            if len(state.get_successors()) == 0: return -100 # loss - terminal node
            total_moves = len(state.get_successors())
            total_moves_opp = len(state.predecessor.get_successors())

        else: # opponent's turn for the given state
            if len(state.get_successors()) == 0: return 100 # win - terminal node
            total_moves_opp = len(state.get_successors())
            total_moves = len(state.predecessor.get_successors())
        
        # Other evaluations...
        evaluation = total_moves - total_moves_opp
        return evaluation
    '''
    Purpose: Generate valid moves for the current state.
    Parameters:
        - state: Current state/node.
    Return: List of valid moves, moves.
    '''
    def generate_valid_moves(self, state):
        # first moves of W and B are unimportant since they are diagonally symmetric
        # randomly choose only one node to search through so it doesn't go through nodes of its diagonally symmetric counterpart
        if state.board.board == KonaneBoard().board: 
            return random.choice([["D5"], ["E4"]]) # first move of B - remove piece 
        if self.is_first_move_W(state): 
            if state.predecessor == None: # first move of W - remove piece
                return random.choice([["E5"], ["D4"]] )
            return ["E5", "D4"] # if agent is B, must go through both possible states for the first more of W
          
        # identify opponent's colour
        if state.colours_turn == "B": colour_opp = "W"
        else: colour_opp = "B"
        
        moves = []
        for y in range(8):
            for x in range(8):
                # found piece to move
                if state.board.get_board()[y][x] == state.colours_turn:
                    initial = self.convert_to_tile(x, y)
                    #moving left
                    for k in range(x - 1, -1, -2):
                        # case 1: break if out of bounds
                        if k < 0 or (k - 1) < 0: break 
                        # case 2: break if piece cannot jump over a piece anymore
                        if state.board.get_board()[y][k] != colour_opp or state.board.get_board()[y][k - 1] != 'O': break 
                        # add to moves if both cases above are true
                        final = self.convert_to_tile(k-1, y)
                        moves.append(f"{initial}-{final}") 

                    #moving up
                    for j in range(y-1, -1, -2):
                        # case 1: break if out of bounds
                        if j < 0 or (j - 1) < 0: break
                        # case 2: break if piece cannot jump over a piece anymore
                        if state.board.get_board()[j][x] != colour_opp or state.board.get_board()[j-1][x] != 'O': break
                        # add to moves if both cases above are true
                        final = self.convert_to_tile(x, j - 1)
                        moves.append(f"{initial}-{final}") 

                    #moving right
                    for k in range(x+1, 8, 2):
                        # case 1: break if out of bounds
                        if k > 7 or (k + 1) > 7: break
                        # case 2: break if piece cannot jump over a piece anymore
                        if state.board.get_board()[y][k] != colour_opp or state.board.get_board()[y][k + 1] != 'O': break
                        # add to moves if both cases above are true
                        final = self.convert_to_tile(k + 1, y)
                        moves.append(f"{initial}-{final}") 

                    #moving down
                    for l in range(y+1, 8, 2):
                        # case 1: break if out of bounds
                        if l > 7 or (l + 1) > 7: break
                        # case 2: break if piece cannot jump over a piece anymore
                        if state.board.get_board()[l][x] != colour_opp or state.board.get_board()[l + 1][x] != 'O': break
                        # add to moves if both cases above are true
                        final = self.convert_to_tile(x, l + 1)
                        moves.append(f"{initial}-{final}") 
        return moves
    '''
    Purpose: Convert coordinates to tile format.
    Parameters:
        - x: X-coordinate.
        - y: Y-coordinate.
    Return: Tile format.
    '''
    def convert_to_tile(self, x, y):
        column = "ABCDEFGH"
        letter = column[x]
        number = str(8 - y)
        return letter + number

''' 
This class creates the playing board for the 8x8 Konane game using alternating black and white tiles. 
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
    Purpose: This method updates the game board based on a given move. The move can either be a peice removal or a jump move. 
    The method updates the board based off of the rules of the Konane game. 
        - If the move is a stone peice removal, the corresponding board position is marked as empty ('O').
        - If the move is a jump, stone peices are removed and moved to a new postition as necessary to execute the jump. 
    Parameters:
            - move: The move to be executed.
    '''
    def update_by_move(self, move):
        # Convert tile piece to match list of list format
        prev_x = self.convert_letter(move[0])
        prev_y = self.convert_number(move[1])
        # color of moving piece
        colour = self.board[prev_y][prev_x]
        #if the len(move) is greater then 2 it means that it is a jump move otherwise normal move.
        if len(move) == 2: # remove piece
            self.board[prev_y][prev_x] = 'O'
            return
        # Convert second tile piece to match list of list format
        new_x = self.convert_letter(move[3])
        new_y = self.convert_number(move[4])
        step = 1

        if prev_x == new_x: # vertical/column jump
            if new_y < prev_y: step = -1
            for i in range(prev_y, new_y, step): # can handle multiple jumps
                self.board[i][prev_x] = 'O'
            self.board[new_y][new_x] = colour
        else: # horizontal/row jump
            if new_x < prev_x: step = -1
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

# convert text file into a list of lists
def convert_file_to_board(filename):
    board = []
    fh = open(filename, "r")
    line = fh.readline()
    while line != "":
        row = []
        line = line.strip("\n")
        for letter in line:
            row.append(letter)
        board.append(row)
        line = fh.readline()
    fh.close()
    return board

def main():
    ''' ~~~Uses Alpha Beta Pruning - need to integrate into drivercheck~~~
    filename = sys.argv[1]
    colour = sys.argv[2]
    board = KonaneBoard(convert_file_to_board(filename))
    agent = KonaneAI(colour, Node(board))
    # use algo for first moves to expand nodes to maximise thinking time
    agent.reset()
    print(agent.action())
    while True:
        opp_action = input()
        agent.reset()
        agent.update_state(opp_action) # update state by by using opponent's input
        print(agent.action())
        #print(time.time() - agent.start) - check to see if its within time
    '''

    filename = sys.argv[1]
    colour = sys.argv[2]

    board = KonaneBoard(get_board_from_file(filename))
    agent = KonaneAI(colour, board)
    state = Node(board, colour)

    while True:
        moves = agent.generate_valid_moves(state)
        
        if len(moves) == 0:
            print("You won")
            return
        else:
            move = random.sample(moves, 1)[0]
            board.update_by_move(move)
            print(move)
        
        try:
            opp_move = input()
        except:
            return

        board.update_by_move(opp_move)

if __name__ == "__main__":
    main()
