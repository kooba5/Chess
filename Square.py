class Square:
    def __init__(self, x, y, piece=None):
        self.x = x
        self.y = y
        self.piece = piece

    def place_piece(self, piece):
        self.piece = piece

    def remove_piece(self):
        piece = self.piece
        self.piece = None
        return piece

    def get_piece(self):
        return self.piece

    def is_empty(self):
        return self.piece is None