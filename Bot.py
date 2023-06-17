import random

class AI:
    def __init__(self, color):
        self.color = color

    def select_move(self, game):
        legal_moves = self.find_legal_moves(game)
        if legal_moves:
            legal_moves.sort(key=self.evaluate_move, reverse=True)
            best_move = legal_moves[0]
            start, end = best_move
            move_string = self.format_move_string(start, end)
            print(f"AI ({self.color}) made move: {move_string}")
            return move_string
        return None

    def format_move_string(self, start, end):
        start_pos = self._num_to_algebraic(start.get_column()) + str(8 - start.get_row())
        end_pos = self._num_to_algebraic(end.get_column()) + str(8 - end.get_row())
        return start_pos + '-' + end_pos

    def _num_to_algebraic(self, num):
        return chr(ord('a') + num)
    
    def safe_move(self, start_square, end_square, game):
        old_start_piece = start_square.get_piece()
        old_end_piece = end_square.get_piece()

        start_square.remove_piece()
        end_square.place_piece(old_start_piece)

        if game.king_in_check(self.color):
            start_square.place_piece(old_start_piece)
            end_square.place_piece(old_end_piece)
            return False
        else:
            start_square.place_piece(old_start_piece)
            end_square.place_piece(old_end_piece)
            return True
    
    def find_legal_moves(self, game):
        legal_moves = []
        for row in game.board:
            for square in row:
                piece = square.get_piece()
                if piece and piece.color == self.color:
                    start = square
                    for move in piece.legal_moves(game.board):
                        end = game.board[move[0]][move[1]]
                        if self.safe_move(start, end, game):
                            legal_moves.append((start, end))
        return legal_moves
    
    def evaluate_move(self, move):
        start, end = move
        end_piece = end.get_piece()
        if end_piece is not None:
            value = end_piece.value
        else:
            value = 0
        value += random.uniform(0, 0.01)
        
        return value
