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
            print(f"Gestion du tournoi '{tournament.name}' :")
            print("1. Afficher les détails du tournoi")
            print("2. Gérer les rounds du tournoi")
            print("3. Afficher le rapport du tournoi")
            print("q. Quitter la gestion du tournoi")

            choice = input("Entrez votre choix : ")

            if choice == "1":
                self.display_tournament_details(tournament)
            elif choice == "2":
                self.manage_rounds(tournament)
            elif choice == "3":
                self.display_tournament_report(tournament)
            elif choice.lower() == "q":
                break
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

    def manage_rounds(self, tournament):
        while True:
            clear_screen()
            print(f"Gestion des rounds du tournoi '{tournament.name}' :")
            print("1. Afficher les rounds existants")
            print("2. Créer un nouveau round")
            print("3. Saisir les résultats des matches")
            print("q. Quitter la gestion des rounds")

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

    def display_existing_rounds(self, tournament):
        clear_screen()
        print(f"Rounds existants pour le tournoi '{tournament.name}':")
        for idx, round_pairs in enumerate(tournament.rounds, 1):
            print(f"Round {idx}")
            for match_idx, pair in enumerate(round_pairs, 1):
                print(f"Match {match_idx}: {pair[0].first_name} {pair[0].last_name} vs. {pair[1].first_name} {pair[1].last_name}")
            print()
        input("Appuyez sur Entrée pour continuer...")

    def create_new_round(self, tournament):
        if tournament.number_of_rounds <= len(tournament.rounds):
            print("Le tournoi a déjà atteint le nombre maximal de rounds.")
            input("Appuyez sur Entrée pour continuer...")
            return

        clear_screen()
        print("Création d'un nouveau round...")
        players = tournament.players[:]
        pairs = []
        while len(players) >= 2:
            player1 = players.pop(0)
            player2 = self.get_opponent_for_player(player1, players, tournament)
            if player2:
                players.remove(player2)
                pairs.append((player1, player2))
        tournament.rounds.append(pairs)

        self.assign_round_identifiers(tournament.players)

        print("Nouveau round créé avec succès.")
        input("Appuyez sur Entrée pour continuer...")

        self.display_existing_rounds(tournament)

    def assign_round_identifiers(self, players):
        for i, player in enumerate(players, 1):
            player.chess_id = f"Joueur{i:03d}"

    def get_opponent_for_player(self, player, players, tournament):
        for potential_opponent in players:
            if not self.players_already_played(player, potential_opponent, tournament):
                return potential_opponent
        return None

    def players_already_played(self, player1, player2, tournament):
        for round_pairs in tournament.rounds:
            for pair in round_pairs:
                if player1 in pair and player2 in pair:
                    return True
        return False

    def enter_match_results(self, tournament):
        clear_screen()
        print("Saisir les résultats des matches pour un round spécifique...")
        input("Appuyez sur Entrée pour continuer...")

    def display_tournament_report(self, tournament):
        clear_screen()
        print("Afficher le rapport du tournoi...")
        input("Appuyez sur Entrée pour continuer...")

