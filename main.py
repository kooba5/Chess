import pygame

from Game import *
from Board import *
from Pieces.Bishop import *
from Pieces.King import *
from Pieces.Pawn import *
from Piece import *
from Pieces.Queen import *
from Pieces.Rook import *
from Square import *
from GameControl import *

if __name__ == "__main__":
    controller = GameController()
    controller.main_loop()
