# TournamentManagementView

import json
import os
from datetime import datetime
from config import GESTION_TOURNOIS_DIR
from models.round import Round
from models.tournament import Tournament

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class TournamentManagementView:
    def __init__(self, tournament_controller, player_controller):
        self.tournament_controller = tournament_controller
        self.player_controller = player_controller

    def create_tournament(self, tournament_id, name, location, start_date_str, end_date_str, number_of_rounds, selected_players):
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

        tournament = Tournament(tournament_id, name, location, start_date, end_date, number_of_rounds, selected_players, current_round=0, players=[])
        
        return tournament

    def manage_tournament(self, tournament):
        saved = False

        tournament.load_from_file()

        def manage_tournament(self, tournament):
            saved = False

            tournament.load_from_file()

            while True:
                clear_screen()
                print(f"Gestion du tournoi '{tournament.tournament_id}':")
                
                current_round = len(tournament.rounds) + 1
                
                if os.path.exists(os.path.join(GESTION_TOURNOIS_DIR, tournament.tournament_id, "rounds", f"matchs_round_{current_round}.json")):
                    print("1. Saisie des résultats")
                else:
                    print("1. Lancer le premier round")

                print("2. Afficher le rapport")
                print("3. Retour au Menu principal")

                sub_choice = input("Entrez votre choix : ")

                if sub_choice == "1":
                    if os.path.exists(os.path.join(GESTION_TOURNOIS_DIR, tournament.tournament_id, "rounds", f"matchs_round_{current_round}.json")):
                        current_round = self.record_match_results(tournament, current_round) 
                    else:
                        current_round = self.launch_first_round(tournament)
                elif sub_choice == "2":
                    self.display_report(tournament)
                elif sub_choice == "3":
                    if not saved:
                        self.tournament_controller.save_tournaments_to_file() 
                        saved = True
                    break
                else:
                    print("Choix invalide. Veuillez réessayer.")
                    input("Appuyez sur Entrée pour continuer...")

    def launch_first_round(self, tournament):
        print(f"Current Round in launch_first_round: {tournament.current_round}")

        if tournament.first_round_launched:
            print("Le premier round a déjà été lancé pour ce tournoi.")
            input("Appuyez sur Entrée pour continuer...")
            return tournament.current_round

        round_dir = os.path.join(GESTION_TOURNOIS_DIR, tournament.tournament_id, "rounds")

        if not os.path.exists(round_dir):
            os.makedirs(round_dir)

        round_files = os.listdir(round_dir)
        if round_files:
            round_numbers = [int(file.split("_")[2].split(".")[0]) for file in round_files]
            last_played_round = max(round_numbers)
            tournament.current_round = last_played_round + 1
        else:
            tournament.current_round = 1

        if tournament.current_round > tournament.number_of_rounds:
            print("Tous les rounds ont déjà été lancés pour ce tournoi.")
            input("Appuyez sur Entrée pour continuer...")
            return tournament.current_round

        if (
            tournament.current_round > 1
            and len(tournament.rounds) >= (tournament.current_round - 1)
            and not tournament.rounds[tournament.current_round - 2].is_completed()
        ):
            print("Les résultats du round précédent doivent être enregistrés avant de lancer le prochain round.")
            input("Appuyez sur Entrée pour continuer...")
            return tournament.current_round

        new_round = Round(tournament.current_round, start_time=datetime.now())

        tournament.rounds.append(new_round)

        if tournament.current_round > 1:
            tournament.rounds[tournament.current_round - 2].results_recorded = False

        selected_players = self.create_matches_for_round(tournament)

        round_file = os.path.join(round_dir, f"matchs_round_{tournament.current_round}.json")

        matches_data = [self.serialize_match_data(idx + 1, match, new_round.start_time) for idx, match in
                        enumerate(selected_players)]
        matches_data[0]["tournament_id"] = tournament.tournament_id

        with open(round_file, "w") as file:
            json.dump(matches_data, file, indent=4)

        tournament.current_round = new_round.round_number

        tournament.first_round_launched = True

        print(f"Le fichier du premier round a été créé : matchs_round_{tournament.current_round}.json")
        input("Appuyez sur Entrée pour continuer...")

        return tournament.current_round
    
    def create_matches_for_round(self, tournament):
        num_players = len(tournament.selected_players)
        if num_players < 2:
            print("Il n'y a pas suffisamment de joueurs pour créer des matchs.")
            return []

        import random
        random.shuffle(tournament.selected_players)
        matches = []
        for i in range(0, num_players - 1, 2):
            player1 = tournament.selected_players[i]
            player2 = tournament.selected_players[i + 1] if i + 1 < num_players else None
            match = (player1, player2)
            matches.append(match)

        return matches


    def select_players_for_first_round(self, tournament):
        print("Sélectionnez les joueurs pour le premier round (nombre pair) :")

        for idx, player in enumerate(tournament.selected_players, start=1):
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
                            selected_player = tournament.selected_players[player_idx]
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
                selected_player = tournament.selected_players[player_idx]
                selected_players.append(selected_player)
            except (ValueError, IndexError):
                print("Choix invalide. Veuillez entrer un numéro valide.")

        return selected_players


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

    def record_match_results(self, tournament, current_round):
        clear_screen()
        print(f"Saisir les résultats des matchs pour le round en cours :")

        print("Numéro du round en cours:", current_round)
        round_dir = os.path.join(GESTION_TOURNOIS_DIR, tournament.tournament_id, "rounds")
        round_file = os.path.join(round_dir, f"matchs_round_{current_round}.json")
        print("Chemin du fichier JSON:", round_file)

        if os.path.exists(round_file):
            with open(round_file, "r") as file:
                matches_data = json.load(file)

            for match_number, match_data in enumerate(matches_data, start=1):
                player1_name = match_data["player1"]["name"]
                player2_name = match_data["player2"]["name"]
                print(f"Match {match_number}:")
                print(f"Joueur 1: {player1_name}")
                print(f"Joueur 2: {player2_name}")

                while True:
                    try:
                        score_player1 = input(f"Résultat pour {player1_name} (P/G/N): ").upper()
                        score_player2 = input(f"Résultat pour {player2_name} (P/G/N): ").upper()

                        if score_player1 not in ["P", "G", "N"] or score_player2 not in ["P", "G", "N"]:
                            print("Veuillez entrer un résultat valide (P/G/N).")
                            continue

                        if score_player1 == "P":
                            player1_points = 0
                            player2_points = 1
                        elif score_player1 == "G":
                            player1_points = 1
                            player2_points = 0
                        else:
                            player1_points = 0.5
                            player2_points = 0.5

                        matches_data[match_number - 1]["player1"]["result"] = player1_points
                        matches_data[match_number - 1]["player2"]["result"] = player2_points

                        matches_data[match_number - 1]["Heure_fin"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        director_notes = input("Remarques de la direction (appuyez sur Entrée pour ignorer) : ")
                        if director_notes:
                            matches_data[match_number - 1]["director_notes"] = director_notes

                        print(f"Résultat enregistré pour {player1_name} : {player1_points}")
                        print(f"Résultat enregistré pour {player2_name} : {player2_points}")

                        break
                    except ValueError:
                        print("Veuillez entrer un résultat valide (P/G/N).")

            tournament.rounds[current_round - 1].end_time = datetime.now()

            with open(round_file, "w") as file:
                json.dump(matches_data, file, indent=4)

            print("Les résultats des matchs ont été enregistrés.")
        else:
            print("Aucun match n'a été créé pour ce round.")

        input("Appuyez sur Entrée pour continuer...")

        return current_round  

    def tournament_sub_menu(self, tournament):
        while True:
            clear_screen()
            current_round = len(tournament.rounds)

            print(f"Valeur de current_round: {current_round}")

            print(f"Gestion du tournoi '{tournament.tournament_id}':")

            if current_round >= 1 and current_round <= tournament.number_of_rounds:
                current_round_obj = tournament.rounds[current_round - 1]
                if not current_round_obj.results_recorded:
                    print("1. Saisie des résultats")
                else:
                    print("1. Remarques Direction")
            elif current_round == 0:
                print("1. Lancer le premier round")
            else:
                print("1. Lancer le prochain round")

            print("2. Afficher le rapport")
            print("3. Retour au Menu principal")

            sub_choice = input("Entrez votre choix : ")

            if sub_choice == "1":
                if current_round >= 1 and current_round <= tournament.number_of_rounds:
                    current_round_obj = tournament.rounds[current_round - 1]
                    if not current_round_obj.results_recorded:
                        current_round = self.record_match_results(tournament, current_round)
                    else:
                        self.record_director_notes(tournament, current_round)
                elif current_round == 0:
                    current_round = self.launch_first_round(tournament)
                else:
                    current_round = self.launch_next_round(tournament)
            elif sub_choice == "2":
                self.display_report(tournament)
            elif sub_choice == "3":
                break
            else:
                print("Choix invalide. Veuillez réessayer.")
                input("Appuyez sur Entrée pour continuer...")

        self.tournament_controller.save_tournaments_to_file()  

        return current_round



    def serialize_match_data(self, match_number, match_tuple, start_time):
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
            },
            "Heure_debut": start_time.strftime("%Y-%m-%d %H:%M:%S")  
        }
        return match_data
