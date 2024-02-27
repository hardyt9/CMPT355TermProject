#!/usr/bin/env python3

import sys
import time
import copy
import random

THINKING_TIME = 10
# This file will contains all the implementation of the minimax algorithm and alpha-beta pruning. (subject to change)

# Implements a node (state) of a game for a tree to search and evaluate using alphabeta
class Node:
    def __init__(self, board, colours_turn="B", action ="", predecessor=None):
      self.predecessor = predecessor
      self.board = board
      self.colours_turn = colours_turn
      self.action = action
      self.successors = []
      self.alpha = -1000
      self.beta = 1000

    def get_successors(sel0f):
        return self.successors
    
    def get_value(self):
        return self.value    
    
    def get_action(self):
        return self.action

# Implements the minimax algorithm
class KonaneAI:
    def __init__(self, colour, state = None):
        self.state = state
        self.best_moves = []
        self.colour = colour
        self.max_depth = 2
        self.t_table = [state] # not yet optimised into program, should store KonaneBoard objects

    #actions -> move piece, remove piece etc.
    def action(self, board):

        start = time.time()
        self.max_depth = 2
        best_action = []
        while time.time() - start < 9.5:
            best_action.append(self.alpha_beta_search())
            self.max_depth += 1
        
        return best_action.pop()
    
        '''
        if self.state.board == Node(KonaneBoard()):
            self.preprocess_first_move_B()
            if self.colour == 'B':
                action = "D5"
            else:
                action = "D4"

        else:
            #action = input()
            action = random.sample(self.possible_moves(board), 1)[0]
        self.total_moves += 1

        print(f'Move chosen: {action}')

        return action #self.__actions.pop()
        '''

    # insert the next possible state/node after a legal move happens from the current state/node
    def insert_successors(self, moves, state):
        if state.colours_turn == "B":
            colour = "W"
        else: 
            colour = "B"

        for move in moves:
            # create a new board with updated move
            successor = KonaneBoard(state.board.get_board())
            successor.update_by_move(move)

            state.get_successors().append(Node(successor, colour, move, state))
    
    # implementing and modifying the given code for alpha beta pruning from the Adversarial search slides
    # work in progress
    def alpha_beta_search(self):
        depth = 0
        v = self.max_value(depth, self.state)
        for s in self.state.get_successors():
            if s.get_value() == v:
                return s.get_action()

        return self.state.get_successors()[0]

    # work in progress
    def max_value(self, depth, state):
        # resets alpha beta for each node for every deep search - need to check to see if it works
        state.alpha = -1000
        state.beta = 1000

        if self.cutoff_test(depth, state): 
            return self.evaluation(state)
        v = -100
        for s in state.get_successors():
            v = max(v, s.min_value(depth + 1, s))
            if v >= state.beta: return v
            state.alpha = max(state.alpha, v)
        return v

    # work in progress
    def min_value(self, depth, state):
        # resets alpha beta for each node for every deep search - need to check to see if it works
        state.alpha = -1000
        state.beta = 1000

        if self.cutoff_test(depth, state): 
            return self.evaluation(state)
        v = 100
        for s in state.get_successors():
            v = min(v, s.max_value(depth + 1, s))
            if v <= state.alpha: return v
            state.beta = min(state.beta, v)
            return v

        # work in progress
    def cutoff_test(self, depth, state):     
        # generate valid moves for state if not yet generated
        if len(state.get_successors()) == 0:
            moves = self.generate_valid_moves(state)
            self.insert_successors(moves, state)
        
        # reach maximum depth for search
        if depth == self.max_depth: 
            return True
        
        # terminal node
        if len(state.get_successors(0)) == 0:
            return True
        
        return False

    def is_first_move_W(self, state):
        board_1 = KonaneBoard()
        board_1.update_by_move("D5")

        board_2 = KonaneBoard()
        board_2.update_by_move("E4")

        if state.board.board == board_1.board or state.board.board == board_2.board:
            return True
        else: 
            return False

    # work in progress
    def evaluation(self, state):
        # Evaluation #1: difference between total moves and opponents moves
        # agent's turn for the state
        if (state.colours_turn == 'B' and self.colour == 'B') or (state.colours_turn == 'W' and self.colour == 'W'):
            if len(state.get_successors(0)) == 0: 
                return -100 # loss - terminal node
            total_moves = len(state.get_successors())
            total_moves_opp = state.predecessor.get_successors()
        else: # opponents' turn for the state
            if len(state.get_successors(0)) == 0:
                 return 100 # win - terminal node
            total_moves_opp = len(state.get_successors())
            total_moves = state.predecessor.get_successors()
        
        # Other evaluations...
            
        evaluation = total_moves - total_moves_opp
        return evaluation


    def generate_valid_moves(self, state):
        if state.board == KonaneBoard(): return ["D5", "E4"] # first move of B - remove piece
        if self.is_first_move_W(state): return ["E5", "D4"] # first move of W - remove piece

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
    
    def convert_to_tile(self, x, y):
        column = "ABCDEFGH"
        letter = column[x]
        number = str(8 - y)
        return letter + number
    
    def reset_alpha_beta(self):
        return

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

        if prev_x == new_x: # vertical/column jump
            if new_y < prev_y: step = -1
            for i in range(prev_y, new_y, step): # can handle multiple jumps
                self.board[i][prev_x] = 'O'
            self.board[int(new_y)][new_x] = colour
        else: # horizontal/row jump
            if new_x < prev_x: step = -1
            for j in range(prev_x, new_x, step): # can handle multiple jumps
                self.board[prev_y][j] = 'O'
            self.board[new_y][new_x] = colour
    
    
    
    # letter - x, number - y Ex. E5 -> 'E', '5'
    def convert_letter(self, letter):
        return self.x.find(letter)
    
    def convert_number(self, number):
        return 8 - int(number)

    # to see if the board is correct
    def print_board(self):
        for i in range(len(self.board)):
            print(8-i, end = '')
            print(self.board[i])
        print(f' {list(self.x)}')
        print()

    def get_board(self):
        return copy.deepcopy(self.board)
    
    def play_game(self):
        count = 0
        player_1 = KonaneAI('B')
        player_2 = KonaneAI('W')
        action = ''
        while action != 'quit':
            self.print_board()
            if count % 2 == 0:
                player = player_1
            else:
                player = player_2
            action = player.action(self)
            if action != 'quit':
                self.update_by_move(action)
            count += 1

    def get_board_from_file(self, filename):
        current_board = []
        with open(filename) as file:
            for row in file:
                current_board.append(list(row.strip()))
        return current_board

def main():
    board = KonaneBoard()

    #filename = "test.txt"
    filename = sys.argv[1]
    colour = sys.argv[2]
    
    board.board = board.get_board_from_file(filename)
    agent = KonaneAI(colour, board)
    turn_count = 0
    
    if colour == "B":
        move = "D5"
        turn_count +=1
        
    else:
        move = "E5"
        turn_count += 2

    board.update_by_move(move)
    print(move)
    
    game_over = False
    while True:
        try:
            opp_move = input()
        except:
            return
        if opp_move == "You won":
            game_over = True
        board.update_by_move(opp_move)
        state = Node(board)
        if turn_count % 2 == 0:
            state.colours_turn = "W"
        else:
            state.colous_turn = "B"
        moves = agent.generate_valid_moves(state)
        if len(moves) == 0:
            move = "You won"
            game_over = True
        else:
            move = random.sample(moves, 1)[0]
            board.update_by_move(move)
        print(move)
        if game_over:
            return

    

if __name__ == "__main__":
    main()
