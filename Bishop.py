from Piece import *

class Bishop(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image, 3.001)
        self.tag = 'B' if self.color == 'W' else 'b'

    def legal_moves(self, board):
        x, y = self.position
        moves = []

        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            newx, newy = x + dx, y + dy
            
            while Piece.is_valid_pos(newx, newy):
                if board[newx][newy].piece is None:
                    moves.append((newx, newy))
                else:
                    if board[newx][newy].piece.color != self.color:
                        moves.append((newx, newy))
                    break

                newx += dx
                newy += dy

        return moves


    