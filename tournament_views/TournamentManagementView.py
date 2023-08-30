# TournamentManagementView.py

import json
import os
from config import GESTION_TOURNOIS_DIR
from models.round import Round
from models.player import Player
from models.match import Match

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

        current_round = len(tournament.rounds) + 1
        if current_round > 4:
            print("Tous les rounds ont déjà été lancés pour ce tournoi.")
            input("Appuyez sur Entrée pour continuer...")
            return

        if current_round > 1 and not tournament.rounds[current_round - 2].results_recorded:
            print("Les résultats du round précédent doivent être enregistrés avant de lancer le prochain round.")
            input("Appuyez sur Entrée pour continuer...")
            return

        selected_players = self.select_players_for_first_round(tournament)
        
        if len(selected_players) < 2:
            print("Il n'y a pas suffisamment de joueurs inscrits pour lancer un round.")
            input("Appuyez sur Entrée pour continuer...")
            return

        if len(selected_players) % 2 != 0:
            print("Le nombre de joueurs doit être pair pour former des matchs.")
            input("Appuyez sur Entrée pour continuer...")
            return

        tournament.first_round_launched = True
        new_round = Round(current_round)
        tournament.rounds.append(new_round)
        tournament.rounds[current_round - 1].results_recorded = False

        first_round_matches = self.create_matches_for_round(selected_players)

        round_dir = os.path.join(GESTION_TOURNOIS_DIR, tournament.tournament_id, "rounds")
        os.makedirs(round_dir, exist_ok=True)
        round_file = os.path.join(round_dir, f"matchs_round_{current_round}.json")

        matches_data = [self.serialize_match_data(idx + 1, match) for idx, match in enumerate(first_round_matches)]
        with open(round_file, "w") as file:
            json.dump(matches_data, file, indent=4)

        print(f"Les matchs du round {current_round} ont été lancés et enregistrés.")
        input("Appuyez sur Entrée pour continuer...")
        tournament.first_round_results_recorded = True 

    def launch_next_round(self, tournament):
        clear_screen()
        print(f"Lancer le prochain round du tournoi '{tournament.tournament_id}' :")

        current_round = len(tournament.rounds) + 1
        if current_round > 4:
            print("Tous les rounds ont déjà été lancés pour ce tournoi.")
            input("Appuyez sur Entrée pour continuer...")
            return

        if current_round > 1 and not tournament.rounds[current_round - 2].results_recorded:
            print("Les résultats du round précédent doivent être enregistrés avant de lancer le prochain round.")
            input("Appuyez sur Entrée pour continuer...")
            return

        selected_players = self.create_matches_for_round(tournament.players)
        if len(selected_players) % 2 != 0:
            print("Le nombre de joueurs doit être pair pour former des matchs.")
            input("Appuyez sur Entrée pour continuer...")
            return

        new_round = Round(current_round)
        tournament.rounds.append(new_round)
        tournament.rounds[current_round - 1].results_recorded = False

        for player1, player2 in selected_players:
            match = Match(player1, player2)
            new_round.add_match(match)

        print(f"Les matches du round {current_round} ont été lancés et enregistrés.")
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
            match = (player1, player2)  # Create a tuple of players
            matches.append(match)
        
        return matches

    def select_players_for_first_round(self, tournament):
        print("Sélectionnez les joueurs pour le premier round (nombre pair) :")
        for idx, player in enumerate(tournament.players, start=1):
            print(f"{idx}. {player.first_name} {player.last_name}")

        selected_players = []
        while True:
            try:
                player_choice = input("Entrez le numéro du joueur à ajouter au round (ou 'q' pour quitter) : ")
                if player_choice.lower() == "q":
                    if len(selected_players) % 2 != 0:
                        print("Le nombre de joueurs sélectionnés est impair.")
                        print("1. Ajouter un joueur pour former une paire (match BYE)")
                        print("2. Retourner au sous-menu")
                        choice = input("Entrez votre choix : ")
                        if choice == "1":
                            player_idx = int(input("Entrez le numéro du joueur à ajouter : ")) - 1
                            selected_player = tournament.players[player_idx]
                            selected_players.append(selected_player)
                            if len(selected_players) % 2 == 0:
                                break
                        elif choice == "2":
                            break
                        else:
                            print("Choix invalide. Veuillez réessayer.")
                    else:
                        break

                player_idx = int(player_choice) - 1
                selected_player = tournament.players[player_idx]
                selected_players.append(selected_player)
            except (ValueError, IndexError):
                print("Choix invalide. Veuillez entrer un numéro valide.")

        return selected_players

    def record_match_results(self, tournament):
        clear_screen()
        print(f"Saisir les résultats des matchs pour le round en cours :")

        current_round = len(tournament.rounds)
        if not tournament.rounds[current_round - 1].matches:
            print("Aucun match n'a été créé pour ce round.")
            input("Appuyez sur Entrée pour continuer...")
            return

        for match in tournament.rounds[current_round - 1].matches:
            clear_screen()
            print(f"Match {match.match_number}:")
            print(f"Joueur 1: {match.player1.first_name} {match.player1.last_name}")
            print(f"Joueur 2: {match.player2.first_name} {match.player2.last_name}")
            
            while True:
                try:
                    score_player1 = int(input(f"Score pour {match.player1.first_name}: "))
                    score_player2 = int(input(f"Score pour {match.player2.first_name}: "))
                    match.set_result(score_player1, score_player2)
                    break
                except ValueError:
                    print("Veuillez entrer un score valide (nombre entier).")

        print("Les résultats des matchs ont été enregistrés.")
        input("Appuyez sur Entrée pour continuer...")

    def serialize_match_data(self, match_number, match_tuple):
        player1, player2 = match_tuple
        player1_name = f"{player1.first_name} {player1.last_name}" if player1 else "BYE"
        player2_name = f"{player2.first_name} {player2.last_name}" if player2 else "BYE"
        
        match_data = {
            "match_number": match_number,
            "player1": {
                "name": player1_name,
                "chess_id": player1.chess_id if player1 else ""
            },
            "player2": {
                "name": player2_name,
                "chess_id": player2.chess_id if player2 else ""
            }
        }
        return match_data
    

    def display_report(self, tournament):
        clear_screen()
        current_round = len(tournament.rounds)

        round_dir = os.path.join(os.path.abspath(GESTION_TOURNOIS_DIR), tournament.tournament_id, "rounds")

        print(f"Contenu du répertoire des rounds : {round_dir}\n")

        files_in_rounds = os.listdir(round_dir)
        if not files_in_rounds:
            print("Aucun fichier trouvé dans le répertoire des rounds.")
        else:
            for idx, filename in enumerate(files_in_rounds, start=1):
                print(f"{idx}. {filename}")

            choice = input("\nEntrez le numéro du fichier à afficher (ou 'q' pour quitter) : ")
            if choice.lower() == 'q':
                return
            
            try:
                file_idx = int(choice) - 1
                if 0 <= file_idx < len(files_in_rounds):
                    selected_file = files_in_rounds[file_idx]
                    file_path = os.path.join(round_dir, selected_file)
                    print(f"Affichage du contenu du fichier : {selected_file}\n")
                    
                    with open(file_path, "r") as file:
                        file_content = file.read()
                        print(file_content)
                else:
                    print("Choix invalide. Veuillez entrer un numéro valide.")
            except ValueError:
                print("Choix invalide. Veuillez entrer un numéro valide.")

        input("\nAppuyez sur Entrée pour continuer...")



    def tournament_sub_menu(self, tournament):
        while True:
            clear_screen()
            print(f"Gestion du tournoi '{tournament.tournament_id}':")
            if not tournament.first_round_results_recorded:
                print("1. Lancer le premier round")
            else:
                print("1. Saisie des résultats")
            print("2. Afficher le rapport")
            print("3. Retour au Menu principal")

            sub_choice = input("Entrez votre choix : ")

            if sub_choice == "1":
                if not tournament.first_round_results_recorded:
                    self.launch_first_round(tournament)
                else:
                    self.record_match_results(tournament)
            elif sub_choice == "2":
                self.display_report(tournament)
            elif sub_choice == "3":
                break
            else:
                print("Choix invalide. Veuillez réessayer.")
                input("Appuyez sur Entrée pour continuer...")


