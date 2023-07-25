# tournament_controller.py

import os
from datetime import datetime
import json
from models.tournament import Tournament
from config import TOURNOIS_DIR


class TournamentController:
    def __init__(self, player_controller):
        self.player_controller = player_controller
        self.tournaments = self.load_tournaments_from_file()

    def create_tournament(self, name, location, start_date_str, end_date_str, number_of_rounds, players_selected):
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        except ValueError:
            print("Format de date incorrect. Assurez-vous de saisir la date au format jj/mm/aaaa.")
            return

        tournament_id = self.generate_tournament_id()

        # Check if players exist in the player_controller
        players = []
        for player_id in players_selected:
            player = self.player_controller.get_player_by_id(player_id)
            if player:
                players.append(player)
            else:
                print(f"Joueur avec l'ID {player_id} introuvable dans le répertoire des joueurs. Le joueur ne sera pas ajouté au tournoi.")

        tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds, players)
        self.tournaments.append(tournament)
        self.save_tournaments_to_file(tournament)  # Pass the tournament object here

        return tournament

    def get_tournaments(self):
        return self.tournaments

    def save_tournaments_to_file(self, tournament):
        filepath = os.path.join(TOURNOIS_DIR, tournament.name, f"info_{tournament.name}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        tournament_data = self.serialize_tournament(tournament)
        with open(filepath, "w") as file:
            json.dump(tournament_data, file, indent=4, default=datetime_to_string)

    def load_tournaments_from_file(self):
        tournaments = []
        for root, _, files in os.walk(TOURNOIS_DIR):
            for file in files:
                if file.startswith("info_") and file.endswith(".json"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r") as f:
                        try:
                            tournament_data = json.load(f)
                            players = self.load_players_for_tournament(filepath)
                            tournament = Tournament(
                                tournament_data["tournament_id"],
                                tournament_data["name"],
                                tournament_data["location"],
                                datetime.strptime(tournament_data["start_date"], "%d/%m/%Y"),
                                datetime.strptime(tournament_data["end_date"], "%d/%m/%Y"),
                                tournament_data.get("number_of_rounds", 4),
                                players
                            )
                            tournaments.append(tournament)
                        except json.JSONDecodeError:
                            print(f"Erreur lors du chargement des données du fichier : {filepath}")

        if not tournaments:
            print("Aucun tournoi enregistré.")
        return tournaments

    def load_players_for_tournament(self, tournament_file):
        filepath = tournament_file.replace("info_", "players_")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                try:
                    players_ids = json.load(file)
                    players = [self.player_controller.get_player_by_id(player_id) for player_id in players_ids]
                    return [player for player in players if player is not None]
                except json.JSONDecodeError:
                    print(f"Erreur lors du chargement des joueurs pour le tournoi : {filepath}")

        return []

    def generate_tournament_id(self):
        tournament_count = len(self.tournaments)
        tournament_id = f"T{tournament_count + 1}"
        return tournament_id

    def serialize_tournament(self, tournament):
        players_ids = [player.chess_id for player in tournament.players]
        tournament_data = {
            "tournament_id": tournament.tournament_id,
            "name": tournament.name,
            "location": tournament.location,
            "start_date": tournament.start_date.strftime("%d/%m/%Y"),
            "end_date": tournament.end_date.strftime("%d/%m/%Y"),
            "number_of_rounds": tournament.number_of_rounds,
            "players": players_ids
        }
        return tournament_data

def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
import os
from datetime import datetime
import json
from models.tournament import Tournament
from config import TOURNOIS_DIR


class TournamentController:
    def __init__(self, player_controller):
        self.player_controller = player_controller
        self.tournaments = self.load_tournaments_from_file()

    def create_tournament(self, name, location, start_date_str, end_date_str, number_of_rounds, players_selected):
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        except ValueError:
            print("Format de date incorrect. Assurez-vous de saisir la date au format jj/mm/aaaa.")
            return

        tournament_id = self.generate_tournament_id()

        # Check if players exist in the player_controller
        players = []
        for player_id in players_selected:
            player = self.player_controller.get_player_by_id(player_id)
            if player:
                players.append(player)
            else:
                print(f"Joueur avec l'ID {player_id} introuvable dans le répertoire des joueurs. Le joueur ne sera pas ajouté au tournoi.")

        tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds, players)
        self.tournaments.append(tournament)
        self.save_tournaments_to_file(tournament)  # Pass the tournament object here

        return tournament

    def get_tournaments(self):
        return self.tournaments

    def save_tournaments_to_file(self, tournament):
        filepath = os.path.join(TOURNOIS_DIR, tournament.name, f"info_{tournament.name}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        tournament_data = self.serialize_tournament(tournament)
        with open(filepath, "w") as file:
            json.dump(tournament_data, file, indent=4, default=datetime_to_string)

    def load_tournaments_from_file(self):
        tournaments = []
        for root, _, files in os.walk(TOURNOIS_DIR):
            for file in files:
                if file.startswith("info_") and file.endswith(".json"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r") as f:
                        try:
                            tournament_data = json.load(f)
                            players = self.load_players_for_tournament(filepath)  # Load players from specific tournament file
                            tournament = Tournament(
                                tournament_data["tournament_id"],
                                tournament_data["name"],
                                tournament_data["location"],
                                datetime.strptime(tournament_data["start_date"], "%d/%m/%Y"),
                                datetime.strptime(tournament_data["end_date"], "%d/%m/%Y"),
                                tournament_data.get("number_of_rounds", 4),
                                players
                            )
                            tournaments.append(tournament)
                        except json.JSONDecodeError:
                            print(f"Erreur lors du chargement des données du fichier : {filepath}")

        if not tournaments:
            print("Aucun tournoi enregistré.")
        return tournaments

    def load_players_for_tournament(self, tournament_file):
        filepath = tournament_file.replace("info_", "players_")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                try:
                    players_ids = json.load(file)
                    players = [self.player_controller.get_player_by_id(player_id) for player_id in players_ids]
                    return [player for player in players if player is not None]
                except json.JSONDecodeError:
                    print(f"Erreur lors du chargement des joueurs pour le tournoi : {filepath}")

        return []


    def generate_tournament_id(self):
        tournament_count = len(self.tournaments)
        tournament_id = f"T{tournament_count + 1}"
        return tournament_id

    def serialize_tournament(self, tournament):
        players_ids = [player.chess_id for player in tournament.players]
        tournament_data = {
            "tournament_id": tournament.tournament_id,
            "name": tournament.name,
            "location": tournament.location,
            "start_date": tournament.start_date.strftime("%d/%m/%Y"),
            "end_date": tournament.end_date.strftime("%d/%m/%Y"),
            "number_of_rounds": tournament.number_of_rounds,
            "players": players_ids
        }
        return tournament_data

def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
