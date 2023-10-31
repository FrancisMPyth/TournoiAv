
# match.py

class Match:
    def __init__(self, player1_id, player2_id, start_time=None):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score_player1 = 0
        self.score_player2 = 0
        self.start_time = start_time 

    def set_score(self, score_player1, score_player2):
        self.score_player1 = score_player1
        self.score_player2 = score_player2
