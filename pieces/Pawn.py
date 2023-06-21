from .Piece import *
from Square import *

class Pawn(Piece):
    def __init__(self, color, position, image, game):
        super().__init__(color, position, image, 1.0)
        self.tag = 'P' if self.color == 'W' else 'p'
        self.first_move = True
        self.direction = -1 if self.color == 'W' else 1 
        self.en_passant = False
        self.game = game

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
        r = 3 if self.color == 'W' else 4
        if self.game.last_move is not None:
            last_start, last_piece_moved, last_end = self.game.last_move
            if last_piece_moved.tag in('P', 'p') and not last_piece_moved.first_move:
                if abs(last_end.get_column() - y) == 1:
                    if x == r:
                        moves.append((last_end.get_row() + self.direction, last_end.get_column()))
        return moves

    def can_promote(self):
         if self.color == 'W' and self.position[0] == 0:
             return True
         if self.color == 'B' and self.position[0] == 7:
             return True
         return False

    def move(self, new_position):
        self.position = new_position
        if new_position in self.legal_moves(self.game.board):
            if new_position[0] - self.position[0] == self.direction and abs(new_position[1] - self.position[1]) == 1:
                if self.game.board[new_position[0]][new_position[1]].get_piece() is None:
                    self.game.board[self.position[0]][new_position[1]].remove_piece()
                else:
                    self.game.board[new_position[0]][new_position[1]].remove_piece()

