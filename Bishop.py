from Piece import *

class Bishop(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)
        self.tag = 'B' if self.color == 'W' else 'b'