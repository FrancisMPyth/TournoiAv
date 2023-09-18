# tournament_controller.py

import os
import json
import re
from datetime import datetime
from models.tournament import Tournament, Round  
from config import DATA_DIR, TOURNOIS_DIR

def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

class TournamentController:
    def __init__(self, player_controller):
        self.player_controller = player_controller
        self.tournaments = self.load_tournaments_from_file()

    def generate_tournament_id(self, name):
        tournament_count = len(self.tournaments)
        name_with_number = f"{name}_{tournament_count + 1}"
        return name_with_number

    def create_tournament(self, name, location, start_date_str, end_date_str, number_of_rounds, selected_players):
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

        tournament_id = self.generate_tournament_id(name)

        tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds, selected_players, current_round=0, players=selected_players)
        
        self.tournaments.append(tournament)
        self.save_tournaments_to_file()
        return tournament

    def get_tournaments(self):
        return self.tournaments

    def load_tournaments_from_file(self):
        tournaments = []
        for root, _, files in os.walk(os.path.join(DATA_DIR, TOURNOIS_DIR)):
            for file in files:
                if file.endswith(".json"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r") as f:
                        try:
                            tournament_data = json.load(f)
                            if "tournament_id" in tournament_data:
                                tournament_id = tournament_data["tournament_id"]
                                tournament = self.create_loaded_tournament(tournament_id, tournament_data)
                                tournaments.append(tournament)
                        except json.JSONDecodeError:
                            print(f"Erreur lors du chargement des données du fichier : {filepath}")

        if not tournaments:
            print("Aucun tournoi enregistré.")
        return tournaments

    def create_loaded_tournament(self, tournament_id, tournament_data):
        name = tournament_data.get("name", "Nom par défaut")
        location = tournament_data.get("location", "Location par défaut")
        start_date = datetime.strptime(tournament_data.get("start_date", "01/01/2023"), "%d/%m/%Y")
        end_date = datetime.strptime(tournament_data.get("end_date", "01/01/2023"), "%d/%m/%Y")
        number_of_rounds = tournament_data.get("number_of_rounds", 4)
        current_round = tournament_data.get("current_round", 0)
        players = self.load_players_for_tournament(tournament_data)

        tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds, players, current_round=current_round)
        return tournament

    def load_players_for_tournament(self, tournament_data):
        players_ids = tournament_data.get("players", [])
        players = [self.player_controller.get_player_by_id(player_id) for player_id in players_ids]
        return [player for player in players if player is not None]

    def load_rounds_for_tournament(self, tournament_data):
        rounds_data = tournament_data.get("rounds", [])
        rounds = [Round(**round_data) for round_data in rounds_data]
        return rounds

    def serialize_tournament(self, tournament):
        players_ids = [player.chess_id for player in tournament.players]
        rounds_data = [round.serialize() for round in tournament.rounds]  
        tournament_data = {
            "tournament_id": tournament.tournament_id,
            "name": tournament.name,
            "location": tournament.location,
            "start_date": tournament.start_date.strftime("%d/%m/%Y"),
            "end_date": tournament.end_date.strftime("%d/%m/%Y"),
            "number_of_rounds": tournament.number_of_rounds,
            "players": players_ids,
            "current_round": tournament.current_round,
            "rounds": rounds_data  
        }
        return tournament_data

    def get_unique_filepath(self, tournament): 
        tournament_id = tournament.tournament_id
        tournament_filename = f"{tournament_id}.json"
        return os.path.join(DATA_DIR, TOURNOIS_DIR, tournament_filename)


    def save_tournaments_to_file(self):
        for tournament in self.tournaments:
            filepath = self.get_unique_filepath(tournament)

            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    existing_data = json.load(file)
                    existing_data["rounds"] = [round.to_dict() for round in tournament.rounds]

                with open(filepath, "w") as file:
                    json.dump(existing_data, file, indent=4, default=datetime_to_string)
            else:
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                tournament_data = self.serialize_tournament(tournament)
                with open(filepath, "w") as file:
                    json.dump(tournament_data, file, indent=4, default=datetime_to_string)

