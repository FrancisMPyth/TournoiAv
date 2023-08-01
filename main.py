# main.py


import os
import json
from datetime import datetime
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from tournament_views.PlayerListView import PlayerListView
from tournament_views.TournamentCreationView import TournamentCreationView
from tournament_views.TournamentListView import TournamentListView


def main():
    player_controller = PlayerController()
    tournament_controller = TournamentController(player_controller)

    player_list_view = PlayerListView()
    tournament_creation_view = TournamentCreationView()  # Pas d'arguments ici
    tournament_list_view = TournamentListView() 

    while True:
        print("Menu Principal:")
        print("1. Enregistrement des Joueurs")
        print("2. Afficher la liste des joueurs")
        print("3. Enregistrer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Gestion des Tournois")
        print("q. Quitter")

        choice = input("Entrez votre choix : ")

        if choice == "1":
            player_list_view.create_player(player_controller)
        elif choice == "2":
            player_list_view.display_player_list(player_controller)
        elif choice == "3":
            tournament_creation_view.create_tournament(tournament_controller, player_controller)
        elif choice == "4":
            tournament_list_view.display_tournaments(tournament_controller)
            input("Appuyez sur une touche pour continuer...")
        elif choice == "5":
            # Reste du code pour la gestion des tournois
            pass
        elif choice.lower() == "q":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
