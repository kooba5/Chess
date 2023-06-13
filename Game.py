import pygame
from Square import *
from Pawn import *
from Rook import *
from Knight import *
from Bishop import *
from Queen import *
from King import *
from Board import *

class ChessGame:
    def __init__(self):
        self.turn = 'W'
        self.board = [[Square(x, y) for y in range(8)] for x in range(8)]
        self.board[0][0].place_piece(Rook('B', (0,0), pygame.image.load('PNG/B.rook.png')))
        self.board[0][1].place_piece(Knight('B', (0,1), pygame.image.load('PNG/B.knight.png')))
        self.board[0][2].place_piece(Bishop('B', (0,2), pygame.image.load('PNG/B.bishop.png')))
        self.board[0][3].place_piece(Queen('B', (0,3), pygame.image.load('PNG/B.queen.png')))
        self.board[0][4].place_piece(King('B', (0,4), pygame.image.load('PNG/B.king.png')))
        self.board[0][5].place_piece(Bishop('B', (0,5), pygame.image.load('PNG/B.bishop.png')))
        self.board[0][6].place_piece(Knight('B', (0,6), pygame.image.load('PNG/B.knight.png')))
        self.board[0][7].place_piece(Rook('B', (0,7), pygame.image.load('PNG/B.rook.png')))
        for i in range(8):
            self.board[1][i].place_piece(Pawn('B', (1, i), pygame.image.load('PNG/B.pawn.png')))
        for i in range(8):
            self.board[6][i].place_piece(Pawn('W', (6, i), pygame.image.load('PNG/W.pawn.png')))
        self.board[7][0].place_piece(Rook('W', (7,0), pygame.image.load('PNG/W.rook.png')))
        self.board[7][1].place_piece(Knight('W', (7,1), pygame.image.load('PNG/W.knight.png')))
        self.board[7][2].place_piece(Bishop('W', (7,2), pygame.image.load('PNG/W.bishop.png')))
        self.board[7][3].place_piece(Queen('W', (7,3), pygame.image.load('PNG/W.queen.png')))
        self.board[7][4].place_piece(King('W', (7,4), pygame.image.load('PNG/W.king.png')))
        self.board[7][5].place_piece(Bishop('W', (7,5), pygame.image.load('PNG/W.bishop.png')))
        self.board[7][6].place_piece(Knight('W', (7,6), pygame.image.load('PNG/W.knight.png')))
        self.board[7][7].place_piece(Rook('W', (7,7), pygame.image.load('PNG/W.rook.png')))

    def parse_move(self, text):
        start_col = ord(text[0]) - ord('a')
        start_row = 8 - int(text[1])
        end_col = ord(text[3]) - ord('a')
        end_row = 8 - int(text[4]) 

        return ((start_row, start_col), (end_row, end_col))
    
    def move_piece(self, text):
        
        if text == 'O-O' or text == 'O-O-O':
            if self.turn == 'W':
                king = self.board[7][4].get_piece()
                rook_file = 7 if text == 'O-O' else 0
                rook = self.board[7][rook_file].get_piece()
            else:
                king = self.board[0][4].get_piece()
                rook_file = 7 if text == 'O-O' else 0
                rook = self.board[0][rook_file].get_piece()
            if king is None or rook is None:
                print('Invalid castling move.')
                return              
            if king.moved == True or rook.moved == True:
                print('Invalid castling move - pieces already moved.')
                return               
            if king.tag == 'K' and rook.tag != 'R':
                print('Invalid castling move.')
                return
            if king.tag == 'k' and rook.tag != 'r':
                print('Invalid castling move.')
                return
            
            step = 1 if king.position[1] < rook.position[1] else -1
            king_final_position = (king.position[0], king.position[1] + 2 * step)
            king_final_position = (king_final_position[0], king_final_position[1] if text == 'O-O' else king_final_position[1] - step)

            if self.king_in_check(self.turn) or any(self.is_square_under_attack(king.position[0], i, self.turn) for i in range(king.position[1] + step, king_final_position[1] + 1, step)):
                print('Invalid castling move - would put your king in check.')
                return
            
            self.castle(king, rook)

        if len(text) != 5 or text[2] != '-' or not text[0] in 'abcdefgh' or not text[3] in 'abcdefgh' or not text[1].isdigit() or not text[4].isdigit():
            print("Invalid move format. Use 'e2-e4'")
            return

        start, end = self.parse_move(text)

        start_square = self.board[start[0]][start[1]]
        end_square = self.board[end[0]][end[1]]

        if start_square.get_piece() is None:
            print("There is no piece on the start square.")
            return

        if start_square.get_piece().color != self.turn:
            print("You must move a piece of your own color.")
            return
        
        legal_moves = start_square.get_piece().legal_moves(self.board) 
        if end not in legal_moves: 
            print('Invalid move')
            return

        old_start_piece = start_square.get_piece()
        old_end_piece = end_square.get_piece()

        piece = start_square.remove_piece()
        end_square.place_piece(piece)

        if self.king_in_check(self.turn):
            print('That move would put your king in check.')
            start_square.place_piece(piece)
            end_square.place_piece(old_end_piece)
            return        
        piece = end_square.get_piece()
        pawn_tag = 'P' if self.turn == 'W' else 'p'
        if piece.tag == pawn_tag and piece.can_promote():
            self.promote_pawn(end, piece.color)
        
        self.turn = 'B' if self.turn == 'W' else 'W'
        return

   
    def get_current_state(self):
        return self.board
    
    def king_in_check(self, color):
        king_tag = 'K' if color == 'W' else 'k'

        king_position = None
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].get_piece()
                if piece and piece.color == color and piece.tag == king_tag:
                    king_position = (i, j)
                    break
            if king_position:
                break

        opposing_color = 'B' if color == 'W' else 'W'
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].get_piece()
                if piece and piece.color == opposing_color:
                    if king_position in piece.legal_moves(self.board):
                        return True

        return False    
    
    def is_square_under_attack(self, row, col, color):
        opposing_color = 'B' if color == 'W' else 'W'
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].get_piece()
                if piece and piece.color == opposing_color:
                    if (row, col) in piece.legal_moves(self.board):
                        return True
        return False
    
    def castle(self, king, rook):
        step = 1 if king.position[1] < rook.position[1] else -1
        for file in range(king.position[1] + step, rook.position[1], step):
            if self.board[king.position[0]][file].piece is not None:
                print('Path not clear for castling.')
                return
        if step == 1:
            new_king_position = (king.position[0], king.position[1] + 2)
            new_rook_position = (rook.position[0], rook.position[1] - 2)
        else:
            new_king_position = (king.position[0], king.position[1] - 2)
            new_rook_position = (rook.position[0], rook.position[1] + 3)

        self.board[king.position[0]][king.position[1]].remove_piece()
        self.board[rook.position[0]][rook.position[1]].remove_piece()
        self.board[new_king_position[0]][new_king_position[1]].place_piece(king)
        self.board[new_rook_position[0]][new_rook_position[1]].place_piece(rook)

        king.position = new_king_position  
        rook.position = new_rook_position  

        king.moved = True
        rook.moved = True
        self.turn = 'B' if self.turn == 'W' else 'W'

    def promote_pawn(self, position, color):
        queen_image = pygame.image.load('PNG/W.queen.png') if color == 'W' else pygame.image.load('PNG/B.queen.png')
        queen = Queen(color, position, queen_image)
        self.board[position[0]][position[1]].place_piece(queen)
