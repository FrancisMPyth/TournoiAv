# TournamentManagementView.py

import json
from config import GESTION_TOURNOIS_DIR

class TournamentManagementView:
    def __init__(self, tournament_controller):
        self.tournament_controller = tournament_controller

    def manage_tournament(self, tournament):
        print(f"Gestion du tournoi '{tournament.name}' :")
        print("1. Afficher les détails du tournoi")
        print("2. Enregistrer le tournoi")
        print("q. Quitter la gestion du tournoi")

        choice = input("Entrez votre choix : ")

        if choice == "1":
            self.display_tournament_details(tournament)
        elif choice == "2":
            self.save_tournament(tournament)
        elif choice.lower() == "q":
            return
        else:
            print("Choix invalide. Veuillez réessayer.")
            self.manage_tournament(tournament)

    def display_tournament_details(self, tournament):
        print(f"Identifiant : {tournament.tournament_id}")
        print(f"Nom : {tournament.name}")
        print(f"Lieu : {tournament.location}")
        print(f"Début : {tournament.start_date.strftime('%d/%m/%Y')}")
        print(f"Fin : {tournament.end_date.strftime('%d/%m/%Y')}")
        print(f"Nombre de rounds : {tournament.number_of_rounds}")
        print("Joueurs inscrits :")
        if tournament.players:
            for player in tournament.players:
                print(f" - {player.first_name} {player.last_name} (ID: {player.chess_id})")
        else:
            print(" - Aucun joueur inscrit.")

    def save_tournament(self, tournament):
        filepath = os.path.join(GESTION_TOURNOIS_DIR, f"Gestion_{tournament.name}.json")
        tournament_data = self.serialize_tournament(tournament)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(tournament_data, file, ensure_ascii=False, indent=4)
        print(f"Le tournoi '{tournament.name}' a été enregistré dans un fichier.")

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
