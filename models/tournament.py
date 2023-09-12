# models/tournament.py

from datetime import datetime

class Tournament:
    def __init__(self, tournament_id, name, location, start_date, end_date, number_of_rounds, selected_players, current_round=0, players=None):
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.selected_players = selected_players
        self.players = players if players is not None else []
        self.rounds = []

    def generate_tournament_id(self, name):
        tournament_count = len(self.tournaments)
        name_with_number = f"{name}_{tournament_count + 1}"
        return name_with_number

    def start_new_round(self):
        if self.current_round < self.number_of_rounds:
            new_round_number = self.current_round + 1
            new_round = Round(new_round_number)
            
            self.rounds.append(new_round)
            self.current_round = new_round_number
        else:
            print("Le tournoi est terminé.")
    
    def get_current_round(self):
        return self.rounds[self.current_round - 1] if self.current_round > 0 else None