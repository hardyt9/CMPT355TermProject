import sys
import time
import copy
THINKING_TIME = 10
# This file will contains all the implementation of the minimax algorithm and alpha-beta pruning. (subject to change)

# Implements a node (state) of a game for a tree to search and evaluate using alphabeta
class Node:
    def __init__(self, board, colours_turn="B", action ="", parent=None):
      self.parent = parent
      self.board = board
      self.colours_turn = colours_turn
      self.action = action
      self.successors = []

    def get_successors(self, state):
        return self.successors
    
    # preprocess the first mvoes of the game for white and black
    def preprocess_first_moves(self):
        # 4 possible moves for Black - remove piece at A8, D5, E4 or H1
        self.insert_successor("A8", "W")
        self.insert_successor("D5", "W")
        self.insert_successor("E4", "W")
        self.insert_successor("H1", "W")

        #possible white moves in a list [[for A8],[for D5],[for E4],[for H1]]
        white_moves = [["B8", "A7"], ["D6", "C5", "E5", "D4"], ["E5", "D4", "F4", "E3"], ["H2", "G1"]]
        for i in range(len(white_moves)): # goes through black's first moves
            move = self.successors[i]
            for j in white_moves[i]: # inserts possible white moves 
                move.insert_successor(j, "B")
    
    # insert the next possible state/node after a legal move happens from the current state/node
    def insert_successor(self, move, colour):
        successor = KonaneBoard(self.board.get_board())
        successor.update_by_move(move)
        self.successors.append(Node(successor, colour, move, self))


# Implements the minimax algorithm
class KonaneAI:
    def __init__(self, colour, state = None):
        self.total_moves = 0
        self.state = Node(KonaneBoard())
        self.best_moves = []
        self.colour = colour

    #actions -> move piece, remove piece etc.
    def action(self, board):
        if self.total_moves == 0:
            if self.colour == 'B':
                action = "D5"
            else:
                action = "D4"
        else:
            action = input("Action:")

        self.total_moves += 1

        return action #self.__actions.pop()
    
    # implementing and modifying the given code for alpha beta pruning from the Adversarial search slides
    # work in progress
    def alpha_beta_search(self):
        depth = 0
        v = self.max_value(depth, -100, 100)
        action = self.state.get_successors.find(v)
        return action 

    # work in progress
    def max_value(self, depth, alpha , beta):
        if self.cutoff_test(depth): 
            return self.evaluation()
        v = -100
        for s in self.state.get_successors:
            v = max(v, s.min_value(depth + 1, alpha, beta))
            if v >= beta: return v
            alpha = max(alpha, v)
        return v

    # work in progress
    def min_value(self ,depth, alpha, beta):
        if self.cutoff_test(depth): 
            return self.evaluation()
        v = 100
        for s in self.state.get_successors:
            v = min(v, s.max_value(depth + 1, alpha, beta))
            if v <= alpha: return v
            beta = min(beta, v)
            return v

    
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
        return moves
    
    # work in progress
    def cutoff_test(self, depth):
        # reach maximum dapth for search
        if depth == self.max_depth: 
            return True
        
        # Todo - reach a terminal node 
        return False

    # work in progress
    def evaluation(self):
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
            print("Possible moves:", player.possible_moves(self))
            action = player.action(self)
            if action != 'quit':
                self.update_by_move(player.action(self))
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
    KonaneBoard().play_game()

if __name__ == "__main__":
    main()
