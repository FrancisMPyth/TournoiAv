# round.py

from .match import Match
from datetime import datetime

class Round:
    def __init__(self, round_number, start_time=None):
        self.round_number = round_number
        self.matches = []
        self.completed = False
        self.start_time = start_time if start_time is not None else datetime.now()
        self.director_notes = ""  

    def add_match(self, match):
        self.matches.append(match)
    
    def set_result(self, match_index, score_player1, score_player2):
        match = self.matches[match_index]
        match.set_result(score_player1, score_player2)

    def is_completed(self):
        return all(match.result_set for match in self.matches)

    def get_matches(self):
        return self.matches

    def to_dict(self):
        return {
            "round_number": self.round_number,
            "matches": [match.to_dict() for match in self.matches],
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        round_number = data["round_number"]
        round_obj = cls(round_number)
        round_obj.completed = data["completed"]

        for match_data in data["matches"]:
            match = Match.from_dict(match_data)
            round_obj.matches.append(match)

        return round_obj
