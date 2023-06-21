from .Piece import *

class King(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image, 10000.0)
        self.tag = 'K' if self.color == 'W' else 'k'
        self.moved = False

    def legal_moves(self, board):
        x, y = self.position
        moves = []

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            newx, newy = x + dx, y + dy

            if Piece.is_valid_pos(newx, newy):  
                end_square = board[newx][newy]
                if end_square.get_piece() is None or end_square.get_piece().color != self.color:
                    moves.append((newx, newy))

        return moves 
    
    def move(self, new_position):
        self.position = new_position
        self.moved = True
