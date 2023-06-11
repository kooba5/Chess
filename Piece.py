

class Piece:
    def __init__(self, color, position, image):
        self.color = color
        self.position = position
        self.image = image

    def move(self, new_position):
        self.position = new_position

    def legal_moves(self, board):
        pass