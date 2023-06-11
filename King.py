from Piece import *

class King(Piece):
    def __init__(self, color, position, image):
        super().__init__(color, position, image)
        self.first_move = True