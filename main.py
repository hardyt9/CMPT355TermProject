# This file will contains all the implementation of the minimax algorithm and alpha-beta pruning. (subject to change)

# Implements the minimax algorithm
class KonaneAI:
    def __init__(self):
        pass

# Implements the playing board - 8x8, alternating black and white tiles
class KonaneBoard:
    def __init__(self):
        self.board = []
        self.letters = 'ABCDEFGH'
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
        print()
        for row in range(len(self.board)):
            print(8-row,end = ' ') # to be removed - aide to visualize in testing
            for letter in self.board[row]:
                print(letter, end='')
            print()
        print(f'  {self.letters}') # to be removed - aide to visualize in testing
        print()

    # Updates board based on played moves
    # to-do - implement color change of previously empty space
    def update_board(self, move):

        if len(move) == 2:
            # opening move does not require change
            removed = move
            # replaces captured piece with O
            x = self.letters.find(removed[0])
            y = 8-int(removed[1])
            captured = self.board[y][x]
            self.board[y][x] = 'O'

        else:
            removed = self.find_removed(move)
            
            # replaces captured piece with O
            x = self.letters.find(removed[0])
            y = 8-int(removed[1])
            captured = self.board[y][x]
            self.board[y][x] = 'O'

            # replaces previous location with O
            prev_x = self.letters.find(move[0])
            prev_y = 8-int(move[1])
            self.board[prev_y][prev_x] = 'O'

            # replaces new position with color
            new_x = self.letters.find(move[3])
            new_y = 8-int(move[4])
            if captured == 'B':
                self.board[new_y][new_x] = 'W'
            else:
                self.board[new_y][new_x] = 'B'

    # Finds the piece that was removed for use in update function
    # to do - fix vertical jumps
    def find_removed(self, move):
        # case if only one piece jumped
        if len(move) == 5:
            first_col = self.letters.find(move[0])
            second_col = self.letters.find(move[3])

            if first_col < second_col:
                #  piece to the left of opp, horizontal jump
                return f'{self.letters[first_col+1]}{move[1]}'
            elif first_col > second_col:
                return f'{self.letters[first_col-1]}{move[1]}'
            
            else:
                # vertical jump
                if move[1] < move[4]:
                    # piece is above opp
                    return f'{self.letters[first_col]}{move[1]+1}'
                elif move[1] > move[4]:
                    return f'{self.letters[first_col]}{[move[1]-1]}'

    # Creates and maintains a list of all possible moves in current position
    # to-do - implement double captures, better overall implementation 
    def possible_moves(self, color):
        # determines current color for detecting moves
        if color == 'B':
            color_opp = 'W'
        else:
            color_opp = 'B'
        
        moves = []

        # checks the possible moves
        for row_pos in range(8):
            for piece_pos in range(8):
                if self.board[row_pos][piece_pos] == 'O':
                    # horizontal captures - can only capture if 'O' in columns c-f
                    if piece_pos >= 2 and piece_pos <= 5:
                        if self.board[row_pos][piece_pos-1] == color_opp and self.board[row_pos][piece_pos-2] == color:
                            moves.append([piece_pos-2, row_pos, piece_pos, row_pos]) # adds list of move from capture to next location
                        if self.board[row_pos][piece_pos+1] == color_opp and self.board[row_pos][piece_pos+2] == color:
                            moves.append([piece_pos+2, row_pos, piece_pos, row_pos]) 

                    # vertical captures - can only capture if 'O' in rows 3-6
                    if row_pos >= 2 and row_pos <= 5:
                        if self.board[row_pos-1][piece_pos] == color_opp and self.board[row_pos-2][piece_pos] == color:
                            moves.append([piece_pos, row_pos-2, piece_pos, row_pos]) # adds list of move from capture to next location
                        if self.board[row_pos+1][piece_pos] == color_opp and self.board[row_pos+2][piece_pos] == color:
                            moves.append([piece_pos, row_pos+2, piece_pos, row_pos]) 

        if len(moves) != 0:
            moves = self.numbers_to_notation(moves)
        else:
            # tracks first move for each color
            if color == 'B':
                moves.append('D5')
                moves.append('E4')
            else:
                moves.append('D4')
                moves.append('E5')

        return moves 
    
    # Converts the provided moves to proper notation for display 
    def numbers_to_notation(self, moves):
        letters = 'ABCDEFGH'
        converted_moves = []

        for move in moves:
            converted_moves.append(f"{letters[move[0]]}{8-move[1]}-{letters[move[2]]}{8-move[3]}")

        return converted_moves

    # Player-controlled move for testing
    # to-do - finish implementation
    def get_input(self, color):
        self.display_board()
        player_move = input(f"Your possible moves are {self.possible_moves(color)}. Choose a move: ")
        self.update_board(player_move)
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
