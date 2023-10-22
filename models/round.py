# round.py
from .match import Match
from datetime import datetime

class Round:
    def __init__(self, round_number, start_time=None):
        self.round_number = round_number
        self.matches = []
        self.start_time = start_time
        self.end_time = None

    def add_match(self, match):
        self.matches.append(match)

    def set_result(self, match_index, score_player1, score_player2):
        match = self.matches[match_index]
        match.set_result(score_player1, score_player2)

    
    
