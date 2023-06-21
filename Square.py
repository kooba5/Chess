class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.piece = None

    def place_piece(self, piece):
        self.piece = piece
        if self.piece is not None:
            self.piece.position = (self.x, self.y)

    def remove_piece(self):
        piece = self.piece
        self.piece = None
        return piece

    def get_piece(self):
        return self.piece

    def has_piece(self):
        return self.piece is not None

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def get_row(self):
        return self.x
    
    def get_column(self):
        return self.y