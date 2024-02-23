# This file will contains all the implementation of the minimax algorithm and aplha-beta pruning. (subject to change)

# Implements the minimax algorithm
class KonaneAI:
    def __init__(self):
        pass

# Implements the playing board - 8x8, alternating black and white tiles
class KonaneBoard:
    def __init__(self):
        self.board = []
        self.create_board()

    # Creates the initial playing board state
    def create_board(self):
        for i in range(8):
            if i % 2 == 0:
                self.board.append(self.create_row('B','W'))
            else:
                self.board.append(self.create_row('W','B'))

    # Creates basic alternating rows for initial board creation
    def create_row(self, color1, color2):
        row = []
        for i in range(8):
            if i%2 == 0:
                row.append(color1)
            else:
                row.append(color2)
        return row
    
    # Displays the current board state
    def display_board(self):
        for row in self.board:
            for letter in row:
                print(letter, end='')
            print()
        print()

    # Updates board based on played moves
    # to-do - finish implementation
    def update_board(self, move):
        # initial move hard-code to test for time being
        if move == 'D5':
            self.board[3][3] = 'O'
        if move == 'E4':
            self.board[3][4] = 'O'
        if move == 'D4':
            self.board[4][3] = 'O'
        if move == 'E5':
            self.board[3][4] = 'O'

    # Creates and maintains a list of all possible moves in current position
    # to-do - rearrange, finish implementation
    def possible_moves(self, color):
        moves = []
        if color == 'B':
            for row_pos in range(8):
                for piece_pos in range(8):
                    if self.board[row_pos][piece_pos] == 'O':
                        # horizontal captures - can only capture if 'O' in columns c-f
                        if piece_pos >= 2 and piece_pos <= 5:
                            if self.board[row_pos][piece_pos-1] == 'W' and self.board[row_pos][piece_pos-2] == 'B':
                                moves.append(f'{row_pos}{piece_pos-2}-{row_pos}{piece_pos}')


            if len(moves) == 0:
                # tracks first move for black
                moves.append('D5')
                moves.append('E4')

        else:
            count = 0
            for row_pos in range(8):
                for piece_pos in (range(8)):
                    if self.board[row_pos][piece_pos] == 'O':
                        count += 1

            if count == 1:
                # tracks first move for white
                moves = []
                moves.append('D4')
                moves.append('E5')
            
        return moves
    
    # Player-controlled move for testing
    # to-do - finish implementation
    def get_input(self, color):
        self.display_board()
        player_move = input(f"Your possible moves are {self.possible_moves(color)}. Choose a move: ")
        self.update_board(player_move)
        self.display_board()
        return player_move 

    # Receives inputs from both players until game is quit 
    def play_game(self):
        move = True
        count = 0
        while move != 'quit':
            if count % 2 == 0:
                move = self.get_input('B')
            else:
                move = self.get_input('W')
            count += 1


if __name__ == "__main__":
    KonaneBoard().play_game()
