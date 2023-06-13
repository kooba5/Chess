from Piece import *
from Square import *

class Pawn(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)
        self.tag = 'P' if self.color == 'W' else 'p'
        self.first_move = True
        self.direction = -1 if self.color == 'W' else 1 

    def legal_moves(self, board):
        x, y = self.position
        moves = []

        if Piece.is_valid_pos(x + self.direction, y) and board[x + self.direction][y].piece is None:
            moves.append((x + self.direction, y))

        if self.first_move and Piece.is_valid_pos(x + 2*self.direction, y) and board[x + 2*self.direction][y].piece is None and board[x + self.direction][y].piece is None:
            moves.append((x + 2*self.direction, y))

        if Piece.is_valid_pos(x + self.direction, y + 1) and board[x + self.direction][y + 1].has_enemy_piece(self.color):
            moves.append((x + self.direction, y + 1))
        if Piece.is_valid_pos(x + self.direction, y - 1) and board[x + self.direction][y - 1].has_enemy_piece(self.color):
            moves.append((x + self.direction, y - 1))

        return moves
    
    def can_promote(self):
         if self.color == 'W' and self.position[0] == 0:
             return True
         if self.color == 'B' and self.position[0] == 7:
             return True
         return False

    def move(self, new_position):
        self.position - new_position
        self.first_move = False



