
# Match

class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score_player1 = None
        self.score_player2 = None
        self.result_set = False

    def set_result(self, score_player1, score_player2):
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.result_set = True

    def is_completed(self):
        return self.result_set

    def to_dict(self):
        return {
            "player1": self.player1,
            "player2": self.player2,
            "score_player1": self.score_player1,
            "score_player2": self.score_player2,
            "result_set": self.result_set,
        }

    @classmethod
    def from_dict(cls, data):
        match = cls(data["player1"], data["player2"])
        match.score_player1 = data["score_player1"]
        match.score_player2 = data["score_player2"]
        match.result_set = data["result_set"]
        return match
