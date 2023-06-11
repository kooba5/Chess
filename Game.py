import pygame
from Square import *
from Pawn import *
from Rook import *
from Knight import *
from Bishop import *
from Queen import *
from King import *

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

        end_square.place_piece(start_square.get_piece())
        start_square.remove_piece()

        self.turn = 'B' if self.turn == 'W' else 'W'         




        
