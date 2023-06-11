import pygame

from Game import *
from Board import *
from Bishop import *
from King import *
from Pawn import *
from Piece import *
from Queen import *
from Rook import *
from Square import *
from GameControl import *

if __name__ == "__main__":
    controller = GameController()
    controller.main_loop()
