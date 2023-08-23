# TournamentManagementView.py

import json
import os
from config import GESTION_TOURNOIS_DIR

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class TournamentManagementView:

    def __init__(self, tournament_controller, player_controller):
        self.tournament_controller = tournament_controller
        self.player_controller = player_controller

    def manage_tournament(self, tournament):
        while True:
            clear_screen()
            print(f"Gestion du tournoi '{tournament.tournament_id}':")
            if not tournament.first_round_results_recorded:
                print("1. Lancer le premier round")
            else:
                print("1. Lancer le deuxième round")
            print("2. Saisir les résultats des matchs")
            print("3. Retour au Menu principal")

            choice = input("Entrez votre choix : ")

            if choice == "1":
                if not tournament.first_round_results_recorded:
                    self.launch_first_round(tournament)
                else:
                    self.launch_next_round(tournament)
            elif choice == "2":
                self.record_match_results(tournament)
            elif choice == "3":
                return  
            else:
                print("Choix invalide. Veuillez réessayer.")
                input("Appuyez sur Entrée pour continuer...")


    def launch_first_round(self, tournament):
        clear_screen()
        print(f"Lancer le premier round du tournoi '{tournament.tournament_id}' :")

        if tournament.first_round_results_recorded:
            print("Le premier round a déjà été lancé pour ce tournoi.")
            input("Appuyez sur Entrée pour continuer...")
            return

        if len(tournament.players) < 2:
            print("Il n'y a pas suffisamment de joueurs inscrits pour lancer un round.")
            input("Appuyez sur Entrée pour continuer...")
            return

        selected_players = self.select_players_for_first_round(tournament)
        if len(selected_players) % 2 != 0:
            print("Le nombre de joueurs doit être pair pour former des matchs.")
            input("Appuyez sur Entrée pour continuer...")
            return

        # Votre logique pour lancer le premier round et enregistrer les matchs

        tournament.first_round_results_recorded = True

        print("Les matches du premier round ont été lancés et enregistrés.")
        input("Appuyez sur Entrée pour continuer...")
    
    def select_players_for_first_round(self, tournament):
        print("Sélectionnez les joueurs pour le premier round (nombre pair) :")
        for idx, player in enumerate(tournament.players, start=1):
            print(f"{idx}. {player.first_name} {player.last_name}")

        selected_players = []
        while True:
            try:
                player_choice = input("Entrez le numéro du joueur à ajouter au round (ou 'q' pour quitter) : ")
                if player_choice.lower() == "q":
                    break

                player_idx = int(player_choice) - 1
                selected_player = tournament.players[player_idx]
                selected_players.append(selected_player)
            except (ValueError, IndexError):
                print("Choix invalide. Veuillez entrer un numéro valide.")

        return [(selected_players[i], selected_players[i + 1]) for i in range(0, len(selected_players), 2)]

    def record_match_results(self, tournament):
        pass

    def display_tournament_details(self, tournament):
        clear_screen()
        print(f"Identifiant : {tournament.tournament_id}")
        print(f"Nom : {tournament.name}")
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

    def manage_rounds(self, tournament):
        while True:
            clear_screen()
            print(f"Gestion des matchs du tournoi '{tournament.name}':")
            print("1. Lancer le premier round")
            print("2. Saisir les résultats des matchs")
            print("3. Retour à la gestion du tournoi")

            choice = input("Entrez votre choix : ")

            if choice == "1":
                self.launch_next_round(tournament)
            elif choice == "2":
                self.record_match_results(tournament)
            elif choice == "3":
                break
            else:
                print("Choix invalide. Veuillez réessayer.")
                input("Appuyez sur Entrée pour continuer...")

    def launch_next_round(self, tournament):
        # Logique pour lancer le prochain round
        pass

    def record_match_results(self, tournament):
        # Logique pour saisir les résultats des matchs
        pass

        first_round_matches = self.create_matches_for_round(tournament.players)

        round_dir = os.path.join(GESTION_TOURNOIS_DIR, tournament.tournament_id, "round1")
        os.makedirs(round_dir, exist_ok=True)
        round_file = os.path.join(round_dir, "first_round_matches.json")

        matches_data = [self.serialize_match_data(idx + 1, match) for idx, match in enumerate(first_round_matches)]
        with open(round_file, "w") as file:
            json.dump(matches_data, file, indent=4)

        print("Les matches du premier round ont été lancés et enregistrés.")
        input("Appuyez sur Entrée pour continuer...")

    def create_matches_for_round(self, players):
            num_players = len(players)
            if num_players < 2:
                print("Il n'y a pas suffisamment de joueurs pour créer des matchs.")
                return []

            import random
            random.shuffle(players)  
            matches = []
            for i in range(0, num_players - 1, 2):
                player1 = players[i]
                player2 = players[i + 1] if i + 1 < num_players else None
                match = (player1, player2)
                matches.append(match)
            
            return matches

    def serialize_match_data(self, match_number, match):
        player1, player2 = match
        player1_name = f"{player1.first_name} {player1.last_name}"
        player2_name = f"{player2.first_name} {player2.last_name}" if player2 else "BYE"
        
        match_data = {
            "match_number": match_number,
            "player1": {
                "name": player1_name,
                "chess_id": player1.chess_id
            },
            "player2": {
                "name": player2_name,
                "chess_id": player2.chess_id if player2 else ""
            }
        }
        return match_data
