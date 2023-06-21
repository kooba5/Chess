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
from GameControl import *

if __name__ == "__main__":
    controller = GameController()
    controller.main_loop()
