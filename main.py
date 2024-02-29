import sys
import time
import copy
import random

THINKING_TIME = 9.9
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
        self.max_depth = 2
        self.t_table = [state] # not yet optimised into program, should store KonaneBoard objects
        self.start = 0

    # reset konane agent values for max_depth, start (timer), and best_moves for newly updated state
    def reset(self):
        self.start = time.time()
        self.best_moves = []
        self.max_depth = 2

    # update current KonaneAI state by the state with self.action == to the input()
    def update_state(self, move):
        for i in self.state.get_successors():
            if i.get_action() == move:
                self.state = i
                print('YES')
                return
        # create a new state if state was not found as a successor of the previous state
        print('NO')
        self.state.board.update_by_move(move)
        self.state = Node(self.state.board, self.colour, move)
        return

    #actions -> move piece, remove piece etc.
    def action(self):
        while time.time() - self.start < THINKING_TIME:
            best_state = self.alpha_beta_search()
            if best_state == None: # thinking time limit is reached
                break
            self.best_moves.append(best_state)
            self.max_depth += 1
            print(best_state.get_action(), self.max_depth, best_state.get_value())
        
        self.state = self.best_moves.pop()
        return self.state.get_action()

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
    # modified to return a Node instead of an action
    def alpha_beta_search(self):
        depth = 0
        v = self.max_value(depth, self.state, -1000, 1000)
        if v == None: return None # thinking time reached, terminate current search
        for s in self.state.get_successors():
            if s.get_value() == v:
                return s

    def max_value(self, depth, state, alpha, beta):
        if time.time() - self.start > THINKING_TIME:
            return None

        if self.cutoff_test(depth, state): 
            x =  self.evaluation(state)
            return x
        
        v = -1000
        for s in state.get_successors():
            s.value = self.min_value(depth + 1, s, alpha, beta)
            if s.value == None: return None # thinking time reached, terminate current search
            v = max(v, s.value)
            if v >= beta: return v
            alpha = max(alpha, v)

        return v

    def min_value(self, depth, state, alpha, beta):
        if time.time() - self.start > THINKING_TIME:
            return None   

        if self.cutoff_test(depth, state): 
            x =  self.evaluation(state)
            return x
        v = 1000
        for s in state.get_successors():
            s.value = self.max_value(depth + 1, s, alpha, beta)
            if s.value == None: return None # thinking time reached, terminate current search
            v = min(v, s.value)
            if v <= alpha: return v
            beta = min(beta, v)
        return v

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
    
    # check if its W's first move, special case - remove a piece
    def is_first_move_W(self, state):
        board_1 = KonaneBoard()
        board_1.update_by_move("D5")

        board_2 = KonaneBoard()
        board_2.update_by_move("E4")

        if state.board.board == board_1.board or state.board.board == board_2.board:
            return True
        else: 
            return False

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

    def generate_valid_moves(self, state):
        # diagonally symmetric - choose one to so for first moves, algo goes through less nodes
        if state.board.board == KonaneBoard().board: 
            return random.choice([["D5"], ["E4"]]) # first move of B - remove piece 
        if self.is_first_move_W(state): 
            if state.predecessor == None: # if agent is W and first move, need only one since symmetric
                return random.choice([["E5"], ["D4"]] )
            return ["E5", "D4"] # first move of W - remove piece
    
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
            self.board[new_y][new_x] = colour
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
    #board = KonaneBoard()
    filename = sys.argv[1]
    colour = sys.argv[2]
    board = KonaneBoard(convert_file_to_board(filename))
    board.print_board()
    agent = KonaneAI(colour, Node(board))
    # use algo for first moves to expand nodes to maximise thinking time
    agent.reset()
    print(agent.action())
    while True:
        #print(time.time() - agent.start) - check time to see if within thinking time
        agent.state.board.print_board()
        opp_action = input()
        agent.reset()
        agent.update_state(opp_action) # update state by by using opponent's input
        agent.state.board.print_board()
        print(agent.generate_valid_moves(agent.state))
        print(agent.action())
        print(time.time() - agent.start)
        print(agent.generate_valid_moves(agent.state))

if __name__ == "__main__":
    main()