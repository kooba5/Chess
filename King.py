from Piece import *

class King(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)
        self.tag = 'K' if self.color == 'W' else 'k'
        self.first_move = True