from .Piece import *

class Knight(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image, 3.000)
        self.tag = 'N' if self.color == 'W' else 'n'
        
    def legal_moves(self, board):
        x, y = self.position
        moves = []

        move_options = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for dx, dy in move_options:
            newx, newy = x + dx, y + dy
            if Piece.is_valid_pos(newx, newy):
                end_square = board[newx][newy]
                if end_square.get_piece() is None or end_square.get_piece().color != self.color: 
                    moves.append((newx, newy))

        return moves
