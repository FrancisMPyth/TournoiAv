# round.py

from .match import Match
from datetime import datetime

class Round:
    def __init__(self, round_number, start_time=None):
        self.round_number = round_number
        self.matches = []
        self.start_time = None
        self.end_time = None

    def create(self):
        pass
    
    def load(self):
        pass
    
    def save(self):
        pass


    def add_match(self, match):
        self.matches.append(match)
    
    def set_result(self, match_index, score_player1, score_player2):
        match = self.matches[match_index]
        match.set_result(score_player1, score_player2)


    def serialize(self):
        return self.to_dict()
