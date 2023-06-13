from Square import *

class Consoleboard:
    def __init__(self):
        self.tiles = [[0,0,0,0,0,0,0,0] for col in range(8)]

    def fill(self):
        for row in range(8):
            for col in range(8):
                self.tiles[row][col] = Square(row, col)




    def move_piece(self):
        if len(self.text) != 5 or self.text[2] != '-' or not self.text[0] in 'abcdefgh' or not self.text[3] in 'abcdefgh' or not self.text[1].isnumeric() or not self.text[4].isnumeric():
            print("Invalid move format. Use 'e2-e4'")
            return

        start_col = ord(self.text[0]) - ord('a') 
        start_row = 8 - int(self.text[1]) # Corrected here
        end_col = ord(self.text[3]) - ord('a') 
        end_row = 8 - int(self.text[4]) # Corrected here

        start = (start_col, start_row)
        end = (end_col, end_row)

        piece = self.starting_order.get(start)

        if piece is None:
            print(f"No piece at position {start}")
            return

        if (piece.isupper() and self.turn != 'W') or (piece.islower() and self.turn != 'B'):
            print("It's not your turn!")
            return
        
        if piece.lower() == 'p': # If the piece is a pawn
            pawn = Pawn(self.turn)
            if not pawn.validate_move(start, end): # Validate the pawn's move
                print("Invalid pawn move.")
                return

        self.starting_order[end], self.starting_order[start] = self.starting_order[start], None

        self.turn = 'B' if self.turn == 'W' else 'W' 