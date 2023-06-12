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

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)