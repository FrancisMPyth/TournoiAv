# TournamentCreationView.py

import os
import json
from datetime import datetime
from models.tournament import Tournament
from models.player import Player
from config import JOUEURS_DIR, TOURNOIS_DIR


class TournamentCreationView:
    def __init__(self, tournament_controller, player_controller):
        self.tournament_controller = tournament_controller
        self.player_controller = player_controller

    def create_tournament(self):
        print("\nEnregistrement d'un tournoi :")

        name = input("Nom du tournoi : ")
        location = input("Lieu : ")
        start_date_str = input("Date de début (format jj/mm/aaaa) : ")
        end_date_str = input("Date de fin (format jj/mm/aaaa) : ")
        number_of_rounds = int(input("Nombre de rounds : "))

        print("\nJoueurs disponibles :")
        self.display_players()
        players_selected = []
        while True:
            player_id = input("Entrez l'ID du joueur à ajouter au tournoi ('q' pour quitter) : ")
            if player_id.lower() == "q":
                break
            players_selected.append(player_id)

        tournament = self.tournament_controller.create_tournament(name, location, start_date_str, end_date_str, number_of_rounds, players_selected)
        if tournament:
            print(f"Le tournoi '{tournament.name}' a été créé avec succès !")

    def display_players(self):
        players = self.player_controller.get_players()
        for player in players:
            print(f"- {player.first_name} {player.last_name} (ID: {player.chess_id})")

    def save_players_to_file(self, tournament):
        filepath = os.path.join(TOURNOIS_DIR, tournament.name, f"players_{tournament.name}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        players_data = self.serialize_players(tournament.players)
        with open(filepath, "w") as file:
            json.dump(players_data, file, indent=4, default=datetime_to_string)

    def serialize_players(self, players):
        players_data = []
        for player in players:
            player_data = {
                "first_name": player.first_name,
                "last_name": player.last_name,
                "date_of_birth": player.date_of_birth.strftime("%d/%m/%Y"),
                "chess_id": player.chess_id,
                "national_chess_id": player.national_chess_id
            }
            players_data.append(player_data)
        return players_data

def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
