from Piece import *

class Pawn(Piece):
    def __init__(self, color, position, image,):
        super().__init__(color, position, image)
        self.tag = 'P' if self.color == 'W' else 'p'
        self.first_move = True

    def legal_moves(self, board):
        x,y = self.position
        moves = []

        if self.color == 'W':
            if board[x-1][y].piece is None:
                moves.append((x-1, y))
                if self.first_move and board[x][y-2].piece is None:
                    moves.append((x, y-2))

            if x > 0 and board[x-1][y-1].piece and board[x-1][y-1].piece.color == 'B':
                moves.append((x-1, y-1))
            if x < 7 and board[x+1][y-1].piece and board[x+1][y-1].piece.color == 'B':
                moves.append((x+1, y-1))

        else:
            if board[x+1][y].piece is None:
                moves.append((x+1, y))
                if self.first_move and board[x][y+2].piece is None:
                    moves.append((x, y+2))

            if x > 0 and board[x-1][y+1].piece and board[x-1][y+1].piece.color == 'W':
                moves.append((x-1, y+1))
            if x < 7 and board[x+1][y+1].piece and board[x+1][y+1].piece.color == 'W':
                moves.append((x+1, y+1))

        return moves
            
    def move(new_position):
        pass
