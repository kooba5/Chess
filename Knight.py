from Piece import *

class Knight(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)
        self.tag = 'N' if self.color == 'W' else 'n'