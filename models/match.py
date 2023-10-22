
# match.py
from datetime import datetime

class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score_player1 = None
        self.score_player2 = None
        self.date_time = None

    def set_result(self, score_player1, score_player2):
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.date_time = datetime.now()

    