import pygame
from Square import *
from pieces.Pawn import *
from pieces.Rook import *
from pieces.Knight import *
from pieces.Bishop import *
from pieces.Queen import *
from pieces.King import *
from Board import *

class ChessGame:
    def __init__(self):
        self.turn = 'W'
        self.game_over = False
        self.last_move = None
        self.starting_pos()

    def parse_move(self, text):
        start_col = ord(text[0]) - ord('a')
        start_row = 8 - int(text[1])
        end_col = ord(text[3]) - ord('a')
        end_row = 8 - int(text[4]) 

        return ((start_row, start_col), (end_row, end_col))
    
    def move_piece(self, text):
        #castling
        if text == 'O-O' or text == 'O-O-O':
            if self.turn == 'W':
                king = self.board[7][4].get_piece()
                rook_file = 7 if text == 'O-O' else 0
                rook = self.board[7][rook_file].get_piece()
            else:
                king = self.board[0][4].get_piece()
                rook_file = 7 if text == 'O-O' else 0
                rook = self.board[0][rook_file].get_piece()   

            self.castle(king, rook)
        if not self.validate_move(text):
            return
        
        start, end = self.parse_move(text)
        start_square = self.board[start[0]][start[1]]
        end_square = self.board[end[0]][end[1]]

        piece = start_square.get_piece()

        #en passant
        if self.can_en_passant(start_square, end_square):
            piece.en_passant = True
        self.perform_en_passant(start_square, end_square, piece)

        #standard move
        piece = start_square.remove_piece()
        end_square.place_piece(piece)
        piece.first_move = False

        if self.king_in_check(self.turn):
            print('That move would put your king in check.')
            self.undo_move(start_square, end_square)
            return 
        
        #promotion
        piece = end_square.get_piece()
        if piece.tag in ('P', 'p') and piece.can_promote():
            self.promote_pawn(end_square, piece.color)

        self.last_move = (start_square, piece, end_square)
        self.turn = 'B' if self.turn == 'W' else 'W'

        #game end
        winning_color = 'White' if self.turn == 'B' else 'Black'
        if self.is_checkmate(winning_color):
            self.game_over = True
        if self.is_stalemate():
            self.game_over = True

        return

    def validate_move(self, text):
        if len(text) != 5 or text[2] != '-' or not text[0] in 'abcdefgh' or not text[3] in 'abcdefgh' or not text[1].isdigit() or not text[4].isdigit():
            print("Invalid move format. Use 'e2-e4'")
            return False

        start, end = self.parse_move(text)
        start_square = self.board[start[0]][start[1]]

        if start_square.get_piece() is None:
            print("There is no piece on the start square.")
            return False

        if start_square.get_piece().color != self.turn:
            print("You must move a piece of your own color.")
            return False

        legal_moves = start_square.get_piece().legal_moves(self.board)
        if end not in legal_moves:
            print('Invalid move')
            return False

        return True    

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

        if self.king_in_check(self.turn) or any(self.is_square_under_attack(king.position[0], i, self.turn) for i in range(king.position[1] + step, new_king_position[1] + 1, step)):
            print('Invalid castling move - would put your king in check.')
            return 
        
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
        position.place_piece(queen)

    def can_en_passant(self, start, end):
        if abs(start.get_row() - end.get_row()) == 2:
            left_square = self.board[start.get_row()][start.get_column() - 1] if start.get_column() - 1 >= 0 else None
            right_square = self.board[start.get_row()][start.get_column() + 1] if start.get_column() + 1 <= 7 else None
            if left_square and left_square.get_piece():
                return True
            if right_square and right_square.get_piece():
                return True
        return False
    
    def perform_en_passant(self, start, end, piece):
        start_square = start
        end_square = end
        if piece.tag in ('P', 'p') and abs(start_square.get_row() - end_square.get_row()) == 1 and start_square.get_column() != end_square.get_column() and end_square.get_piece() is None:
            self.board[start_square.get_row()][end_square.get_column()].remove_piece()        
    
    def is_checkmate(self, color):
        winning_color = color
        if not self.king_in_check(self.turn):
            return False

        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].get_piece()
                if piece is not None and piece.color == self.turn:
                    for move in piece.legal_moves(self.board):
                        start_square = self.board[i][j]
                        end_square = self.board[move[0]][move[1]]
                        
                        old_start_piece = start_square.get_piece()
                        old_end_piece = end_square.get_piece()
                        
                        piece_to_move = start_square.remove_piece()
                        end_square.place_piece(piece_to_move)
                        
                        still_in_check = self.king_in_check(self.turn)
                        
                        start_square.place_piece(old_start_piece)
                        end_square.place_piece(old_end_piece)
                        
                        if not still_in_check:
                            return False 
        print(f"Checkmate! The player with {winning_color} pieces won!")
        return True
    
    def is_stalemate(self):
        if self.king_in_check(self.turn):
            return False

        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].get_piece()
                if piece and piece.color == self.turn:
                    original_position = piece.position
                    for move in piece.legal_moves(self.board):
                        captured_piece = self.board[move[0]][move[1]].get_piece()
                        self.board[move[0]][move[1]].place_piece(self.board[original_position[0]][original_position[1]].remove_piece())
                        piece.position = move
                        if not self.king_in_check(self.turn):
                            self.board[original_position[0]][original_position[1]].place_piece(self.board[move[0]][move[1]].remove_piece())
                            piece.position = original_position
                            if captured_piece:
                                self.board[move[0]][move[1]].place_piece(captured_piece)
                            return False
                        self.board[original_position[0]][original_position[1]].place_piece(self.board[move[0]][move[1]].remove_piece())
                        piece.position = original_position
                        if captured_piece:
                            self.board[move[0]][move[1]].place_piece(captured_piece)
        print(f"Stalemate...Ooops")
        return True

    def starting_pos(self):
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
            self.board[1][i].place_piece(Pawn('B', (1, i), pygame.image.load('PNG/B.pawn.png'), self))
        for i in range(8):
            self.board[6][i].place_piece(Pawn('W', (6, i), pygame.image.load('PNG/W.pawn.png'), self))
        self.board[7][0].place_piece(Rook('W', (7,0), pygame.image.load('PNG/W.rook.png')))
        self.board[7][1].place_piece(Knight('W', (7,1), pygame.image.load('PNG/W.knight.png')))
        self.board[7][2].place_piece(Bishop('W', (7,2), pygame.image.load('PNG/W.bishop.png')))
        self.board[7][3].place_piece(Queen('W', (7,3), pygame.image.load('PNG/W.queen.png')))
        self.board[7][4].place_piece(King('W', (7,4), pygame.image.load('PNG/W.king.png')))
        self.board[7][5].place_piece(Bishop('W', (7,5), pygame.image.load('PNG/W.bishop.png')))
        self.board[7][6].place_piece(Knight('W', (7,6), pygame.image.load('PNG/W.knight.png')))
        self.board[7][7].place_piece(Rook('W', (7,7), pygame.image.load('PNG/W.rook.png')))

    def undo_move(self, start, end):
        start_square = start
        end_square = end
        piece = end_square.remove_piece()
        start_square.place_piece(piece)

