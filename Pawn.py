from Piece import *
from Square import *

class Pawn(Piece):
    def __init__(self, color, position, image, game):
        super().__init__(color, position, image)
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
            print(f"Last piece moved: {last_piece_moved.tag}, Position: {last_end}")
            if last_piece_moved.tag in('P', 'p') and not last_piece_moved.first_move:
                print("Last piece moved was a Pawn on its first move.")
                if abs(last_end.get_column() - y) == 1:
                    print("The Pawn moved to a column next to the current piece.")
                    if x == r:
                        print("The current piece is on the correct row for en passant.")
                        moves.append((last_end.get_row() + self.direction, last_end.get_column()))
                    else:
                        print("The current piece is NOT on the correct row for en passant.")
                else:
                    print("The Pawn did NOT move to a column next to the current piece.")
            else:
                print("Last piece moved was NOT a Pawn on its first move.")
        else:
            print("There was no last move.")
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
                self.game.board[self.position[0]][new_position[1]].remove_piece()

