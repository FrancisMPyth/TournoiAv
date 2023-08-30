# main.py

import os
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from tournament_views.PlayerListView import PlayerListView
from tournament_views.TournamentCreationView import TournamentCreationView
from tournament_views.TournamentListView import TournamentListView
from tournament_views.TournamentManagementView import TournamentManagementView

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    player_controller = PlayerController()
    tournament_controller = TournamentController(player_controller)

    player_list_view = PlayerListView()
    tournament_creation_view = TournamentCreationView(tournament_controller, player_controller)
    tournament_list_view = TournamentListView()
    tournament_management_view = TournamentManagementView(tournament_controller, player_controller)

    while True:
        clear_screen()
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
            tournament_list_view.display_tournaments(tournament_controller)
            tournament_id = input("Spécifiez l'identifiant du tournoi à gérer ('q' pour quitter) : ")
            if tournament_id.lower() == "q":
                continue
            tournament = None
            for t in tournament_controller.get_tournaments():
                if t.tournament_id == tournament_id:
                    tournament = t
                    break
            if tournament is not None:
                tournament_sub_menu(tournament_management_view, tournament)
        elif choice.lower() == "q":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

def tournament_sub_menu(tournament_management_view, tournament):
    while True:
        clear_screen()
        print(f"Gestion du tournoi '{tournament.tournament_id}':")
        print("1. Lancer le premier round")
        print("2. Saisir les résultats des matchs")
        print("3. Afficher les détails du tournoi")
        print("4. Retour au Menu principal")

        sub_choice = input("Entrez votre choix : ")

        if sub_choice == "1":
            if not tournament.first_round_results_recorded:
                tournament_management_view.launch_first_round(tournament)
            else:
                tournament_management_view.launch_next_round(tournament)
        elif sub_choice == "2":
            tournament_management_view.record_match_results(tournament)
        elif sub_choice == "3":
            tournament_management_view.display_tournament_details(tournament)
            input("Appuyez sur Entrée pour continuer...")
        elif sub_choice == "4":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
