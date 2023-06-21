import pygame

from Game import *
from Board import *
from pieces.Bishop import *
from pieces.King import *
from pieces.Pawn import *
from pieces.Piece import *
from pieces.Queen import *
from pieces.Rook import *
from Square import *
from Bot import *

class GameController:
    def __init__(self):
        self.game = ChessGame()
        self.board = Chessboard()
        self.ai = AI('B')

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.board.input_box.collidepoint(event.pos):
                        self.board.active = not self.board.active
                    else:
                        self.board.active = False
                    self.board.color = self.board.color_active if self.board.active else self.board.color_inactive
                if event.type == pygame.KEYDOWN:
                    if self.board.active:
                        if event.key == pygame.K_RETURN:
                            print(self.board.text)
                            new_state = self.game.move_piece(self.board.text) 
                            self.board.update_board(new_state)  
                            self.board.text = ''
                            if self.game.game_over:
                                running = False
                            #else:
                                # ai_move = self.ai.select_move(self.game)
                                # if ai_move is not None:
                                #     self.game.move_piece(ai_move)
                                #     game_state = self.game.get_current_state() 
                                #     self.board.update_board(game_state) 
                        elif event.key == pygame.K_BACKSPACE:
                            self.board.text = self.board.text[:-1]
                        else:
                            self.board.text += event.unicode
                        

            game_state = self.game.get_current_state() 
            self.board.printboard(game_state) 
            pygame.display.flip()
            self.board.clock.tick(30)
        print('Game over')
        pygame.quit()