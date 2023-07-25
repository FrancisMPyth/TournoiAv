# player_controller.py

import os
from datetime import datetime
import json
from models.player import Player
from config import JOUEURS_DIR

class PlayerController:
    def __init__(self):
        self.players = []
        self.load_players_from_file()

    def add_player(self, first_name, last_name, date_of_birth, chess_id, national_chess_id):
        player = Player(first_name, last_name, date_of_birth, chess_id, national_chess_id)
        self.players.append(player)
        self.save_players_to_file()
        return player

    def select_player(self, player_id):
        for player in self.players:
            if player.chess_id == player_id:
                return player
        return None
    
    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.chess_id == player_id:
                return player
        return None

    def get_players(self):
        return self.players

    def save_players_to_file(self):
        filepath = os.path.join(JOUEURS_DIR, "joueurs.json")
        with open(filepath, "w") as file:
            players_data = []
            for player in self.players:
                player_data = {
                    "first_name": player.first_name,
                    "last_name": player.last_name,
                    "date_of_birth": player.date_of_birth.strftime("%d/%m/%Y"),
                    "chess_id": player.chess_id,
                    "national_chess_id": player.national_chess_id
                }
                players_data.append(player_data)
            json.dump(players_data, file, indent=4, default=self.player_json_serialize)

    def load_players_from_file(self):
        filepath = os.path.join(JOUEURS_DIR, "joueurs.json")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                try:
                    players_data = json.load(file)
                    for player_data in players_data:
                        first_name = player_data["first_name"]
                        last_name = player_data["last_name"]
                        date_of_birth = datetime.strptime(player_data["date_of_birth"], "%d/%m/%Y")
                        chess_id = player_data["chess_id"]
                        national_chess_id = player_data["national_chess_id"]
                        player = Player(first_name, last_name, date_of_birth, chess_id, national_chess_id)
                        self.players.append(player)
                except json.JSONDecodeError:
                    print("Erreur lors du chargement des données des joueurs. Le fichier peut être vide.")
        else:
            print("Le fichier des joueurs n'existe pas. Une nouvelle liste de joueurs sera créée.")

    # Fonction pour gérer la sérialisation des objets joueurs
    def player_json_serialize(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%d/%m/%Y")
        elif isinstance(obj, Player):
            return obj.__dict__  # Utiliser le dictionnaire représentant l'objet joueur
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
