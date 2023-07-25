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
    tournament_creation_view = TournamentCreationView(tournament_controller, player_controller)  
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
            tournament_creation_view.create_tournament()
        elif choice == "4":
            tournament_list_view.display_tournaments(tournament_controller)
            input("Appuyez sur une touche pour continuer...")
        elif choice == "5":
            while True:
                print("\nGestion des Tournois:")
                print("1. Choix du Tournoi")
                print("2. Afficher les détails d'un tournoi")
                print("3. Enregistrer un tournoi dans un fichier")
                print("4. Retour au menu principal")

                sub_choice = input("Entrez votre choix : ")

                if sub_choice == "1":
                    tournament_list_view.display_tournaments(tournament_controller)
                    tournament_id = input("Spécifiez l'identifiant du tournoi ('q' pour quitter) : ")
                    if tournament_id.lower() == "q":
                        break
                    tournament = tournament_controller.select_tournament(tournament_id)
                    if tournament is not None:
                        tournament_list_view.display_players(tournament)  # Affichage des joueurs
                elif sub_choice == "2":
                    tournament_list_view.display_tournaments(tournament_controller)
                    tournament_id = input("Spécifiez l'identifiant du tournoi ('q' pour quitter) : ")
                    if tournament_id.lower() == "q":
                        break
                    tournament = tournament_controller.select_tournament(tournament_id)
                    if tournament is not None:
                        tournament_list_view.display_tournament_details(tournament)
                elif sub_choice == "3":
                    tournament_list_view.display_tournaments(tournament_controller)
                    tournament_id = input("Spécifiez l'identifiant du tournoi ('q' pour quitter) : ")
                    if tournament_id.lower() == "q":
                        break
                    tournament = tournament_controller.select_tournament(tournament_id)
                    if tournament is not None:
                        tournament_list_view.save_tournament_to_file(tournament)
                        print(f"Le tournoi '{tournament.name}' a été enregistré dans un fichier.")
                elif sub_choice == "4":
                    break
                else:
                    print("Choix invalide. Veuillez réessayer.")
        elif choice.lower() == "q":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
