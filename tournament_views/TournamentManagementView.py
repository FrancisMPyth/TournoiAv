# TournamentManagementView.py

import json
import os
import random
from config import GESTION_TOURNOIS_DIR

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.chess_id = ""
        self.score = None

class Tournament:
    def __init__(self, name, number_of_rounds):
        self.name = name
        self.number_of_rounds = number_of_rounds
        self.players = []
        self.rounds = []

class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

class TournamentManagementView:
    def __init__(self, tournament_controller, player_controller):
        self.tournament_controller = tournament_controller
        self.player_controller = player_controller

    def manage_tournament(self, tournament):
        while True:
            clear_screen()
            print(f"Gestion du tournoi '{tournament.name}':")
            print("1. Lancement du Tournoi")
            print("2. Gérer les matchs du tournoi")
            print("3. Saisir les résultats des matchs")
            print("4. Afficher les détails du tournoi")
            print("5. Retour au Menu principal") 
            
            choice = input("Entrez votre choix : ")

            if choice == "1":
                self.launch_tournament(tournament)
            elif choice == "2":
                self.manage_rounds(tournament)
            elif choice == "3":
                self.record_match_results(tournament)
            elif choice == "4":
                self.display_tournament_details(tournament)
            elif choice == "5":
                break  # Quitter la gestion du tournoi
            else:
                print("Choix invalide. Veuillez réessayer.")
                input("Appuyez sur Entrée pour continuer...")

    def display_tournament_details(self, tournament):
        clear_screen()
        print(f"Identifiant : {tournament.tournament_id}")
        print(f"Nom : {tournament.name}")
        print(f"Lieu : {tournament.location}")
        print(f"Début : {tournament.start_date.strftime('%d/%m/%Y')}")
        print(f"Fin : {tournament.end_date.strftime('%d/%m/%Y')}")
        print(f"Nombre de rounds : {tournament.number_of_rounds}")
        print("Joueurs inscrits :")
        if tournament.players:
            for idx, player in enumerate(tournament.players, 1):
                print(f" - {player.first_name} {player.last_name} (ID: {player.chess_id})")
        else:
            print(" - Aucun joueur inscrit.")
        input("Appuyez sur Entrée pour continuer...")

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

    def select_round(self, tournament):
        round_count = len(tournament.rounds)
        while True:
            try:
                clear_screen()
                print(f"Sélectionner le round pour saisir les résultats des matchs pour le tournoi '{tournament.name}' :")
                for idx, round_pairs in enumerate(tournament.rounds, 1):
                    print(f"Round {idx}")
                selected_round = int(input(f"Entrez le numéro du match (1 à {round_count}) : "))
                if 1 <= selected_round <= round_count:
                    return selected_round
                else:
                    print("Numéro de match invalide. Veuillez réessayer.")
            except ValueError:
                print("Veuillez entrer un numéro valide.")

    def manage_rounds(self, tournament):
        while True:
            clear_screen()
            print(f"Gestion des matchs du tournoi '{tournament.name}' :")
            print("1. Afficher les matchs existants")
            print("2. Créer un nouveau match")
            print("3. Saisir les résultats des matchs")
            print("q. Quitter la gestion des matchs")

            choice = input("Entrez votre choix : ")

            if choice == "1":
                self.display_existing_rounds(tournament)
            elif choice == "2":
                self.create_new_round(tournament)
            elif choice == "3":
                self.enter_match_results(tournament)
            elif choice.lower() == "q":
                break
            else:
                print("Choix invalide. Veuillez réessayer.")
                input("Appuyez sur Entrée pour continuer...")

    def launch_tournament(self, tournament):
        clear_screen()
        print(f"Lancement du premier round du tournoi '{tournament.name}' :")
        
        if tournament.number_of_rounds == 0:
            print("Le tournoi n'a pas encore de rounds.")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        if len(tournament.rounds) > 0 and len(tournament.rounds[0]) > 0:
            print("Le premier round a déjà été lancé.")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        if len(tournament.players) < 2:
            print("Il n'y a pas suffisamment de joueurs inscrits pour lancer un round.")
            input("Appuyez sur Entrée pour continuer...")
            return

        first_round_matches = self.create_matches_for_round(tournament.players)
        
        for match_number, match in enumerate(first_round_matches, 1):
            match_data = self.serialize_match_data(match_number, match)
            match_dir = os.path.join(GESTION_TOURNOIS_DIR, tournament.name, f"round1")
            os.makedirs(match_dir, exist_ok=True)
            match_file = os.path.join(match_dir, f"match{match_number}.json")
            with open(match_file, "w") as file:
                json.dump(match_data, file, indent=4)

        print("Les matches du premier round ont été lancés et enregistrés.")
        input("Appuyez sur Entrée pour continuer...")

    def create_matches_for_round(self, players):
        random.shuffle(players)
        matches = [Match(players[i], players[i+1]) for i in range(0, len(players), 2)]
        return matches

    def serialize_match_data(self, match_number, match):
        match_data = {
            "match_number": match_number,
            "player1": {
                "first_name": match.player1.first_name,
                "last_name": match.player1.last_name,
                "chess_id": match.player1.chess_id
            },
            "player2": {
                "first_name": match.player2.first_name,
                "last_name": match.player2.last_name,
                "chess_id": match.player2.chess_id
            }
        }
        return match_data

    def record_match_results(self, tournament):
        clear_screen()
        print("Enregistrer les résultats des matches...")

        for round_matches in tournament.rounds:
            if self.are_results_recorded(round_matches):
                continue

            for match in round_matches:
                for player in match:
                    if player.score is None:
                        print(f"Match: {player.first_name} {player.last_name}")
                        score = input(f"Entrez le score pour {player.first_name} {player.last_name} : ")
                        player.score = float(score) if score else None

        input("Appuyez sur Entrée pour continuer...")

    def are_results_recorded(self, round_matches):
        for match in round_matches:
            for player in match:
                if player.score is None:
                    return False
        return True

# Reste du code inchangé
