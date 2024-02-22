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

    def create_board(self):
        for i in range(8):
            if i % 2 == 0:
                self.board.append(self.create_row('B','W'))
            else:
                self.board.append(self.create_row('W','B'))
        for row in self.board:
            print(row)

    def create_row(self, color1, color2):
        row = []
        for i in range(8):
            if i%2 == 0:
                row.append(color1)
            else:
                row.append(color2)
        return row

