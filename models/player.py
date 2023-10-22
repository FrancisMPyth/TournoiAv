# player.py

from datetime import datetime

class Player:
    def __init__(self, first_name, last_name, date_of_birth, chess_id, national_chess_id):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.chess_id = chess_id
        self.national_chess_id = national_chess_id
        self.score = 0

    