import sys
import time
import copy
import random

THINKING_TIME = 10
# This file will contains all the implementation of the minimax algorithm and alpha-beta pruning. (subject to change)

# Implements a node (state) of a game for a tree to search and evaluate using alphabeta
class Node:
    def __init__(self, board, colours_turn="B", action =""):
      self.board = board
      self.colours_turn = colours_turn
      self.action = action
      self.successors = []
      self.value = 0

    def get_successors(self):
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
        self.t_table = [state] # not yet optimised into program

    # preprocess the first moves of the game for white and black
    def first_move_B(self, state):
        # 4 possible moves for Black - remove piece at A8, D5, E4 or H1
        state.insert_successors("A8", state)
        state.insert_successors("D5", state)
        state.insert_successors("E4", state)
        state.insert_successors("H1", state)
        return

    def first_move_W(self, state):
        if state[0][0] == 'O':
            self.insert_successors(["B8", "A7"], state)
        elif state[3][3] == 'O':
            self.insert_successors(["D6", "C5", "E5", "D4"], state)
        elif state[4][4] == 'O':
            self.insert_successors(["E5", "D4", "F4", "E3"], state)
        elif state[7][7] == 'O':
            self.insert_successors(["H2", "G1"], state)
        return  

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

            state.get_successors().append(Node(successor, colour, move))

    #actions -> move piece, remove piece etc.
    def action(self, board):
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
    
    # implementing and modifying the given code for alpha beta pruning from the Adversarial search slides
    # work in progress
    def alpha_beta_search(self):
        depth = 0
        v = self.max_value(depth, self.state,  -100, 100)
        for s in self.state.get_successors():
            if s.get_value() == v:
                return s.get_action()

        return self.state.get_successors()[0]

    # work in progress
    def max_value(self, depth, state, alpha, beta):
        if self.cutoff_test(depth, state): 
            return self.evaluation(state)
        v = -100
        for s in self.successors(state):
            v = max(v, s.min_value(depth + 1, s, alpha, beta))
            if v >= beta: return v
            alpha = max(alpha, v)
        return v

    # work in progress
    def min_value(self, depth, state, alpha, beta):
        if self.cutoff_test(depth, state): 
            return self.evaluation(state)
        v = 100
        for s in self.successors(state):
            v = min(v, s.max_value(depth + 1, s, alpha, beta))
            if v <= alpha: return v
            beta = min(beta, v)
            return v

        # work in progress
    def cutoff_test(self, depth, state):
        # reach maximum dapth for search
        if depth == self.max_depth: 
            return True
        
        # Todo - reach a terminal node 
        return False

    # work in progress
    def evaluation(self, state):
        return
    
    # • Successor function: list of (move,state) pairs specifying legal moves
    def successors(self, state):
        if state.board == KonaneBoard():
            self.first_move_B(state)
        
        elif state.action in ["A8", "D5", "E4", "H1"]:
            self.first_move_W(state)
        
        else:
            moves = self.generate_valid_moves(state)
            self.insert_successors(moves, state)
        return

    # finds possible moves in current state 
    # to-do - replace with recursive fxn to clean up
    def possible_moves(self, state):
        # determines current color for detecting moves
        if self.colour == 'B':
            colour_opp = 'W'
        else:
            colour_opp = 'B'
        
        letters = 'ABCDEFGH'
        moves = []
        board = state.get_board()

        for row_pos in range(8):
            for piece_pos in range(8): # for every piece on the board, checks if piece is a blank
                
                if board[row_pos][piece_pos] == 'O':
                    # horizontal captures - can only capture if 'O' in columns c-f
                    
                    if piece_pos >= 2 and piece_pos <= 5:
                        # checking captures from right to left
                        if board[row_pos][piece_pos-1] == colour_opp and board[row_pos][piece_pos-2] == self.colour:
                            moves.append(f'{letters[piece_pos-2]}{8-row_pos}-{letters[piece_pos]}{8-row_pos}')
                            try:
                                # protects in case of out of range
                                # double jumps
                                if board[row_pos][piece_pos+1] == colour_opp and board[row_pos][piece_pos+2] == 'O':
                                    moves.append(f'{letters[piece_pos-2]}{8-row_pos}-{letters[piece_pos+2]}{8-row_pos}')
                                    # triple jumps
                                    if board[row_pos][piece_pos+3] == colour_opp and board[row_pos][piece_pos+4] == 'O':
                                        moves.append(f'{letters[piece_pos-2]}{8-row_pos}-{letters[piece_pos+4]}{8-row_pos}')
                            except:
                                pass
                        
                        # checking captures from left to right
                        if board[row_pos][piece_pos+1] == colour_opp and board[row_pos][piece_pos+2] == self.colour:
                            moves.append(f'{letters[piece_pos+2]}{8-row_pos}-{letters[piece_pos]}{8-row_pos}') 
                            try:
                                # double jump
                                if board[row_pos][piece_pos-1] == colour_opp and board[row_pos][piece_pos-2] == 'O':
                                    moves.append(f'{letters[piece_pos+2]}{8-row_pos}-{letters[piece_pos-2]}{8-row_pos}')
                                    # triple jump
                                    if board[row_pos][piece_pos-3] == colour_opp and board[row_pos][piece_pos-4] == 'O':
                                        moves.append(f'{letters[piece_pos+2]}{8-row_pos}-{letters[piece_pos-4]}{8-row_pos}')
                            except:
                                pass                        
                    
                    # vertical captures - can only capture if 'O' in rows 3-6
                    if row_pos >= 2 and row_pos <= 5:
                        if board[row_pos-1][piece_pos] == colour_opp and board[row_pos-2][piece_pos] == self.colour:
                            moves.append(f'{letters[piece_pos]}{8-row_pos+2}-{letters[piece_pos]}{8-row_pos}') 
                            try:
                                if board[row_pos+1][piece_pos] == colour_opp and board[row_pos+2][piece_pos] == 'O':
                                    moves.append(f'{letters[piece_pos]}{8-row_pos+2}-{letters[piece_pos]}{8-row_pos-2}')
                                    if board[row_pos+3][piece_pos] == colour_opp and board[row_pos+4][piece_pos] == 'O':
                                        moves.append(f'{letters[piece_pos]}{8-row_pos+2}-{letters[piece_pos]}{8-row_pos-4}')
                            except:
                                pass

                        if board[row_pos+1][piece_pos] == colour_opp and board[row_pos+2][piece_pos] == self.colour:
                            moves.append(f'{letters[piece_pos]}{8-row_pos-2}-{letters[piece_pos]}{8-row_pos}') 
                            try:
                                if board[row_pos-1][piece_pos] == colour_opp and board[row_pos-2][piece_pos] == 'O':
                                    moves.append(f'{letters[piece_pos]}{8-row_pos-2}-{letters[piece_pos]}{8-row_pos+2}')
                                    if board[row_pos-3][piece_pos] == colour_opp and board[row_pos-4][piece_pos] == 'O':
                                        moves.append(f'{letters[piece_pos]}{8-row_pos-2}-{letters[piece_pos]}{8-row_pos+4}')
                            except:
                                pass
        if moves == []:
            moves.append('quit')
        print(f'Possible moves: {moves}')
        return moves

    def generate_valid_moves(self, state):

        if state.colours_turn == "B":
            colour_opp = "W"
        else: 
            colour_opp = "B"
        
        moves = []
        for y in range(8):
            for x in range(8):
                # found piece to move
                if state.board.get_board()[y][x] == state.colours_turn:
                    initial = self.convert_to_tile(x, y)
                    #moving left
                    for k in range(x - 1, -1, -2):
                        # out of bounds
                        if k < 0 or (k - 1) < 0:
                            break
                        # continues to look for multiple jumps as long as it stays valid
                        if state.board.get_board()[y][k] != colour_opp or state.board.get_board()[y][k - 1] != 'O': 
                            break
                        final = self.convert_to_tile(k-1, y)
                        moves.append(f"{initial}-{final}") 

                    #moving up
                    for j in range(y-1, -1, -2):
                        # out of bounds
                        if j < 0 or (j - 1) < 0:
                            break
                        # continues to look for multiple jumps as long as it stays valid
                        if state.board.get_board()[j][x] != colour_opp or state.board.get_board()[j-1][x] != 'O': 
                            break
                        final = self.convert_to_tile(x, j - 1)
                        moves.append(f"{initial}-{final}") 

                    #moving right
                    for k in range(x+1, 8, 2):
                        # out of bounds
                        if k > 7 or (k + 1) > 7:
                            break
                        # continues to look for multiple jumps as long as it stays valid
                        if state.board.get_board()[y][k] != colour_opp or state.board.get_board()[y][k + 1] != 'O': 
                            break
                        final = self.convert_to_tile(k + 1, y)
                        moves.append(f"{initial}-{final}") 

                    #moving down
                    for l in range(y+1, 8, 2):
                        # out of bounds
                        if l > 7 or (l + 1) > 7:
                            break
                        # continues to look for multiple jumps as long as it stays valid
                        if state.board.get_board()[l][x] != colour_opp or state.board.get_board()[l + 1][x] != 'O': 
                            break
                        final = self.convert_to_tile(x, l + 1)
                        moves.append(f"{initial}-{final}") 
        return moves
    
    def convert_to_tile(self, x, y):
        column = "ABCDEFGH"
        letter = column[x]
        number = str(8 - y)
        return letter + number

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

def main():
    '''
    argv = sys.argv
    agent = KonaneAI('B')

    n = Node(KonaneBoard())
    n.preprocess_first_moves('B')

    while True:
        agent.action()
        opp_move = input()

    return
    '''
    board = KonaneBoard()
    board.print_board()
    board.update_by_move("F5")
    board.update_by_move("D5")

    board.print_board()

    agent = KonaneAI("B", board)
    moves = agent.generate_valid_moves(Node(board))
    print(moves)
    #KonaneBoard().play_game()

if __name__ == "__main__":
    main()
