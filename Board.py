import pygame
import pygame.freetype 
from Pieces.Pawn import *

class Chessboard:
    def __init__(self):
        pygame.init()
        self.font = pygame.freetype.Font(None, 24)

        self.window_size = (750, 750)
        self.screen = pygame.display.set_mode((1000, self.window_size[1])) 
        pygame.display.set_caption("Chessboard")

        self.square_size = self.window_size[0] // 8

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.brown = (196, 164, 132)
        self.blue = (0, 0, 255)
        self.text_color = (0, 0, 0)
        self.turn = 'W'

        self.icons = {
            'r': pygame.image.load('PNG/B.rook.png'),
            'n': pygame.image.load('PNG/B.knight.png'),
            'b': pygame.image.load('PNG/B.bishop.png'),
            'q': pygame.image.load('PNG/B.queen.png'),
            'k': pygame.image.load('PNG/B.king.png'),
            'p': pygame.image.load('PNG/B.pawn.png'),
            'R': pygame.image.load('PNG/W.rook.png'),
            'N': pygame.image.load('PNG/W.knight.png'),
            'B': pygame.image.load('PNG/W.bishop.png'),
            'Q': pygame.image.load('PNG/W.queen.png'),
            'K': pygame.image.load('PNG/W.king.png'),
            'P': pygame.image.load('PNG/W.pawn.png')
        }

        
        self.starting_order = {
            (0, 0): 'r', (1, 0): 'n', (2, 0): 'b', (3, 0): 'q', (4, 0): 'k', (5, 0): 'b', (6, 0): 'n', (7, 0): 'r',
            (0, 1): 'p', (1, 1): 'p', (2, 1): 'p', (3, 1): 'p', (4, 1): 'p', (5, 1): 'p', (6, 1): 'p', (7, 1): 'p',
            (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None, (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
            (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None, (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
            (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None, (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
            (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None, (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,
            (0, 6): 'P', (1, 6): 'P', (2, 6): 'P', (3, 6): 'P', (4, 6): 'P', (5, 6): 'P', (6, 6): 'P', (7, 6): 'P',
            (0, 7): 'R', (1, 7): 'N', (2, 7): 'B', (3, 7): 'Q', (4, 7): 'K', (5, 7): 'B', (6, 7): 'N', (7, 7): 'R'
        }

        self.input_box = pygame.Rect(820, 20, 140, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.clock = pygame.time.Clock()

    def printboard(self, game_state):
        self.screen.fill(self.white)
        for row in range(8):
            for col in range(8):
                x = col * self.square_size
                y = row * self.square_size
                color = self.white if (row + col) % 2 == 0 else self.brown
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))
                piece = game_state[row][col].get_piece()
                if piece:
                    icon = self.icons.get(piece.tag)
                    if icon:
                        icon = pygame.transform.scale(icon, (self.square_size, self.square_size))
                        self.screen.blit(icon, (x, y))
        txt_surface, _ = self.font.render(self.text, self.text_color)
        self.screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
    
    def update_board(self, new_state):
        self.starting_order = new_state

