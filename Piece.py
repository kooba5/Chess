

class Piece:
    def __init__(self, color, position, image):
        self.color = color
        self.position = position
        self.image = image

    def move(self, new_position):
        self.position = new_position

    def legal_moves(self, board):
        pass
    
    @staticmethod
    def is_valid_pos(x, y):
        return 0 <= x < 8 and 0 <= y < 8