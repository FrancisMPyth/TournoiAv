# tournament.py

import json
import os
from datetime import datetime
from models.round import Round

TOURNAMENT_DATA_DIR = "v:\\Projet 4\\Projet 4\\TournoiAv\\Data\\tournois"

class Tournament:
    def __init__(self, tournament_id, name, location, start_date, end_date, number_of_rounds, selected_players, current_round=None, players=None, first_round_launched=False):  # Assurez-vous que first_round_launched est initialisé à False
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.selected_players = selected_players
        self.players = players if players is not None else []
        self.rounds = []
        self.first_round_launched = first_round_launched  
        self.load_current_round()

        if current_round is not None:
            self.current_round = current_round
        else:
            self.current_round = 0


    def load_current_round(self):
        file_path = os.path.join(TOURNAMENT_DATA_DIR, f"{self.tournament_id}.json")

        if not os.path.exists(file_path):
            return

        with open(file_path, "r") as file:
            try:
                tournament_data = json.load(file)
                self.current_round = tournament_data.get("current_round", 0)

                self.first_round_launched = tournament_data.get("first_round_launched", False)

            except json.JSONDecodeError as e:
                print(f"Erreur lors du chargement des données du fichier : {file_path}")
                raise e


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
            "first_round_launched": self.first_round_launched,  
            "rounds": [
                {
                    "round_number": round_obj.round_number,
                    "completed": round_obj.completed
                }
                for round_obj in self.rounds
            ]
        }

        file_path = os.path.join(TOURNAMENT_DATA_DIR, f"{self.tournament_id}.json")

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
