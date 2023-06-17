class Piece:
    def __init__(self, color, position, image, value):
        self.color = color
        self.position = position
        self.image = image
        self.value = value

    def move(self, new_position):
        self.position = new_position
 
    @staticmethod
    def is_valid_pos(x, y):
        return 0 <= x < 8 and 0 <= y < 8