
# Match

from datetime import datetime

class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score_player1 = None
        self.score_player2 = None
        self.result_set = False
        self.date_time = None

    def set_result(self, score_player1, score_player2):
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.result_set = True
        self.date_time = datetime.now()


    def is_completed(self):
        return self.result_set

    def to_dict(self):
        return {
            "player1": self.player1,
            "player2": self.player2,
            "score_player1": self.score_player1,
            "score_player2": self.score_player2,
            "result_set": self.result_set,
            "match_datetime": str(self.date_time) if self.date_time else None
        }


