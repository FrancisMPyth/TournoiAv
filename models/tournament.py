# tournament.py

import json
import os  
from datetime import datetime
from models.round import Round

class Tournament:
    def __init__(self, tournament_id, name, location, start_date, end_date, number_of_rounds, selected_players, current_round=None, players=None):
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.selected_players = selected_players
        self.players = players if players is not None else []
        self.rounds = []

        self.load_current_round()

        if current_round is not None:
            self.current_round = current_round
        else:
            self.current_round = 0

    def load_current_round(self):
        file_path = f"v:\\Projet 4\\Projet 4\\TournoiAv\\Data\\tournois\\{self.tournament_id}.json"
        
        if not os.path.exists(file_path):
            return

        with open(file_path, "r") as file:
            try:
                tournament_data = json.load(file)
                self.current_round = tournament_data.get("current_round", 0)
            except json.JSONDecodeError:
                print(f"Erreur lors du chargement des données du fichier : {file_path}")

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

    def save_to_file(self):
        data = {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.strftime("%d/%m/%Y"),
            "end_date": self.end_date.strftime("%d/%m/%Y"),
            "number_of_rounds": self.number_of_rounds,
            "players": [player.chess_id for player in self.selected_players],
            "current_round": self.current_round,
            "rounds": [
                {
                    "round_number": round_obj.round_number,
                    "matches": [],
                    "completed": round_obj.completed
                }
                for round_obj in self.rounds
            ]
        }

        file_path = f"v:\\Projet 4\\Projet 4\\TournoiAv\\Data\\tournois\\{self.tournament_id}.json"

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
