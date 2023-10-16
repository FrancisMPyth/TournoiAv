# Match.py
from datetime import datetime

class Match:
    def __init__(self, player1_id, player2_id):
        self.player1 = player1_id
        self.player2 = player2_id
        self.score_player1 = None
        self.score_player2 = None
        self.date_time = None

    def set_result(self, score_player1, score_player2):
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.date_time = datetime.now()

    def load(self):
        pass

    def save(self):
        pass

    def get_winner_points(self):
        if self.score_player1 > self.score_player2:
            return 1
        elif self.score_player1 < self.score_player2:
            return 0
        else:
            return 0.5

    def get_loser_points(self):
        return 1 - self.get_winner_points()
