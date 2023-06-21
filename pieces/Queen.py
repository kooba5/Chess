from Piece import *

class Queen(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image, 9.0)
        self.tag = 'Q' if self.color == 'W' else 'q'

    def legal_moves(self, board):
        x, y = self.position
        moves = []

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            newx, newy = x + dx, y + dy

            while Piece.is_valid_pos(newx, newy): 
                end_square = board[newx][newy]
                if end_square.get_piece() is None:
                    moves.append((newx, newy))
                elif end_square.get_piece().color != self.color: 
                    moves.append((newx, newy))
                    break
                else: 
                    break

                newx, newy = newx + dx, newy + dy

        return moves
